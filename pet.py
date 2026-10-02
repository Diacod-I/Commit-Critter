"""
A README pet that the bot feeds once a day, using your real GitHub activity as food.

  python pet.py feed     -> ages the pet, feeds it your last-24h activity, redraws README   (commit 1)
  python pet.py diary    -> appends the pet's diary entry for today                         (commit 2)
  python pet.py trophy   -> adds a trophy only on milestone days, otherwise does nothing    (commit 3, sometimes)

Each command writes its commit message to .msg for the workflow to use.
Stdlib only, so no pip install is needed.
"""
import datetime as dt
import json
import os
import random
import sys
import urllib.request
from pathlib import Path

STATE = Path("state.json")
NAME = os.environ.get("PET_NAME", "Snail")
USER = os.environ.get("GH_USER", "")
REPO = os.environ.get("GITHUB_REPOSITORY", "")
TODAY = dt.date.today().isoformat()

ART = {
    "ecstatic": r"""
     \(^o^)/
   @  ~~~~~~~>   *zooms at 0.03 km/h*
""",
    "happy": r"""
       (o.o)
   @  ~~~~~~~>
""",
    "meh": r"""
       (-_-)
   @  ~~~~~~~>   ...
""",
    "hungry": r"""
       (;_;)
   @  ~~~~~~~>   *stomach rumbles*
""",
    "starving": r"""
       (x_x)
   @  _______    *has retreated into shell*
""",
}

DIARY = {
    "ecstatic": ["Ate like royalty. Slimed a victory lap.", "My human shipped things. I am proud.", "Feast day. Lettuce for everyone."],
    "happy": ["A decent meal. Life is good.", "Got fed. Respect.", "Crunchy commits today."],
    "meh": ["Some crumbs. I'll survive.", "Saw a lone commit. Better than nothing."],
    "hungry": ["Nothing to eat today. I stared at the terminal.", "Is my human okay? No pushes."],
    "starving": ["Writing this from inside my shell.", "Day ? of no food. Considering a fork."],
}


def load():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"born": TODAY, "age": 0, "hunger": 3, "food_today": 0,
            "total_food": 0, "real_streak": 0, "best_streak": 0, "last_fed": None}


def save(s):
    STATE.write_text(json.dumps(s, indent=2) + "\n")


def msg(text):
    Path(".msg").write_text(text + "\n")


def real_activity():
    """Count your public GitHub events in the last 24h, ignoring this repo (so the bot can't feed itself)."""
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "readme-pet"}
    if os.environ.get("GH_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GH_TOKEN']}"
    req = urllib.request.Request(f"https://api.github.com/users/{USER}/events/public?per_page=100", headers=headers)
    events = json.load(urllib.request.urlopen(req, timeout=20))
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=24)
    counted = {"PushEvent", "PullRequestEvent", "PullRequestReviewEvent", "IssuesEvent",
               "IssueCommentEvent", "CreateEvent", "ReleaseEvent"}
    n = 0
    for e in events:
        t = dt.datetime.fromisoformat(e["created_at"].replace("Z", "+00:00"))
        if t >= cutoff and e["repo"]["name"] != REPO and e["type"] in counted:
            n += 1
    return n


def mood(s):
    h = s["hunger"]
    if s["food_today"] >= 5:
        return "ecstatic"
    return "happy" if h <= 2 else "meh" if h <= 4 else "hungry" if h <= 7 else "starving"


def render(s):
    m = mood(s)
    bar = "█" * (10 - s["hunger"]) + "░" * s["hunger"]
    Path("README.md").write_text(f"""# {NAME}

A snail that lives in this README. A bot visits every day at noon IST and feeds it
whatever I actually did on GitHub in the last 24 hours. No real work means no food.

```{ART[m]}```

| | |
|---|---|
| Mood | **{m}** |
| Fullness | `{bar}` |
| Ate today | {s['food_today']} |
| Age | {s['age']} days (born {s['born']}) |
| Lifetime food | {s['total_food']} |
| Real-work streak | {s['real_streak']} days (best: {s['best_streak']}) |

[Diary](diary.md) · [Trophies](trophies.md)
""")


def feed():
    s = load()
    if s["last_fed"] == TODAY:
        msg("")  # already fed today; makes the step a no-op
        return
    try:
        food = real_activity()
    except Exception as e:  # API down / rate-limited: still commit, don't punish or reward
        print(f"couldn't read activity: {e}")
        food = None
    s["age"] += 1
    s["last_fed"] = TODAY
    if food is None:
        s["food_today"] = 0
        save(s)
        render(s)
        msg(f"day {s['age']}: {NAME} couldn't find the kitchen (API hiccup), napped instead")
        return
    s["food_today"] = food
    s["total_food"] += food
    if food:
        s["hunger"] = max(0, s["hunger"] - min(food, 5))
        s["real_streak"] += 1
        s["best_streak"] = max(s["best_streak"], s["real_streak"])
    else:
        s["hunger"] = min(10, s["hunger"] + 2)
        s["real_streak"] = 0
    save(s)
    render(s)
    msg(f"day {s['age']}: {NAME} ate {food} thing{'s' * (food != 1)} ({mood(s)})")


def diary():
    s = load()
    p = Path("diary.md")
    text = p.read_text() if p.exists() else f"# {NAME}'s diary\n\n"
    if f"- {TODAY}" in text:
        msg("")
        return
    m = mood(s)
    text += f"- {TODAY} · day {s['age']} · {m} · {random.choice(DIARY[m])}\n"
    p.write_text(text)
    msg(f"diary: day {s['age']}")


def trophy():
    s = load()
    milestones = {7: "one week of real work", 30: "a month of real work", 100: "100 days of real work",
                  365: "a full year of real work"}
    got = milestones.get(s["real_streak"]) if s["food_today"] else None
    if not got and s["age"] and s["age"] % 100 == 0:
        got = f"{NAME} turned {s['age']} days old"
    p = Path("trophies.md")
    text = p.read_text() if p.exists() else "# Trophies\n\n"
    if not got or f"- {TODAY}" in text:
        msg("")
        return
    p.write_text(text + f"- {TODAY} · 🏆 {got}\n")
    msg(f"trophy: {got}")


if __name__ == "__main__":
    {"feed": feed, "diary": diary, "trophy": trophy}[sys.argv[1]]()
