"""
Commit Critter: a tiny pet that lives in your README and eats your real GitHub activity.

  python critter.py whoami   -> prints commit author name + email (line 1, line 2)
  python critter.py feed     -> ages the pet, feeds it your last-24h activity, redraws README
  python critter.py diary    -> appends today's diary entry
  python critter.py trophy   -> adds a trophy on milestone days only
  python critter.py preview DIR -> writes every species/mood sprite to DIR (for the docs)

Each command except whoami writes its commit message to .critter-msg (empty = nothing to commit).
Configured through environment variables (set by action.yml). Stdlib only.
"""
import datetime as dt
import html
import json
import os
import random
import re
import sys
import urllib.request
from pathlib import Path

import sprites

# ---------------------------------------------------------------- config

ENV = os.environ.get
USER = ENV("CRITTER_USER") or ENV("GITHUB_REPOSITORY_OWNER", "")
REPO = ENV("GITHUB_REPOSITORY", "")
TOKEN = ENV("CRITTER_TOKEN", "")
README = Path(ENV("CRITTER_README") or "README.md")
HOME = Path(ENV("CRITTER_DIR") or ".critter")
ACTION_REPO = ENV("CRITTER_ACTION_REPO") or "Diacod-I/commit-critter"
TODAY = ENV("CRITTER_TODAY") or dt.datetime.now(dt.timezone.utc).date().isoformat()
MSG = Path(".critter-msg")
START, END = "<!-- COMMIT-CRITTER:START -->", "<!-- COMMIT-CRITTER:END -->"
NO_TROPHIES = "_No trophies yet. The first one comes after 7 days of real work in a row._\n"

# ---------------------------------------------------------------- species

MOODS = ["ecstatic", "happy", "meh", "hungry", "starving"]

SPECIES = {
    "snail": {
        "default_name": "Pebble",
        "diary": {
            "ecstatic": ["Ate like royalty. Slimed a victory lap.", "Feast day. Lettuce for everyone."],
            "happy":    ["A decent meal. Life is good.", "Crunchy commits today."],
            "meh":      ["Some crumbs. I'll survive.", "Saw a lone commit. Better than nothing."],
            "hungry":   ["Nothing to eat. I stared at the terminal.", "Is my human okay? No pushes."],
            "starving": ["Writing this from inside my shell.", "Considering a fork. Of my own life."],
        },
    },
    "crab": {
        "default_name": "Clawdia",
        "diary": {
            "ecstatic": ["Pinched a whole feast. Scuttled in circles.", "Sideways victory dance x3."],
            "happy":    ["Good haul today. Claws content.", "The tide brought commits."],
            "meh":      ["Slim pickings on the beach.", "One measly commit washed up."],
            "hungry":   ["The tide pool is empty.", "I am pinching the air in protest."],
            "starving": ["Moving into a smaller shell to save energy.", "Under the rock. Do not disturb."],
        },
    },
    "cat": {
        "default_name": "Biscuit",
        "diary": {
            "ecstatic": ["My human worked hard. I allowed one pet.", "Feast. Then a 14-hour nap."],
            "happy":    ["Adequate tribute received.", "Sat on the warm laptop. Commits were made."],
            "meh":      ["Tribute was small. I am judging.", "One commit. I expected more."],
            "hungry":   ["Pushed three things off the desk. No commits.", "Screamed at 4am. Nothing."],
            "starving": ["I have filed a complaint with management.", "Lying on the keyboard until you code."],
        },
    },
    "slime": {
        "default_name": "Gloop",
        "diary": {
            "ecstatic": ["Absorbed SO many commits. I am large now.", "Wobbled all day. Pure joy."],
            "happy":    ["Absorbed some commits. Squishy and content.", "Good day to be gelatinous."],
            "meh":      ["A small snack. I remain medium-sized.", "One commit. Barely a jiggle."],
            "hungry":   ["Shrinking slightly. Please code.", "Gurgling sadly."],
            "starving": ["I am mostly puddle now.", "Evaporating gently."],
        },
    },
}

# ---------------------------------------------------------------- helpers


def warn(text):
    print(f"::warning title=Commit Critter::{text}")


def species():
    s = (ENV("CRITTER_SPECIES") or "snail").strip().lower()
    if s not in SPECIES:
        warn(f"unknown species '{s}', using snail. Options: {', '.join(SPECIES)}")
        s = "snail"
    return s


def theme():
    t = (ENV("CRITTER_THEME") or "light").strip().lower()
    if t not in sprites.THEMES:
        warn(f"unknown theme '{t}', using light. Options: {', '.join(sprites.THEMES)}")
        t = "light"
    return t


def size():
    z = (ENV("CRITTER_SIZE") or "medium").strip().lower()
    if z not in sprites.SIZES:
        warn(f"unknown size '{z}', using medium. Options: {', '.join(sprites.SIZES)}")
        z = "medium"
    return z


def display_width():
    """The card's width in the README: the `width` input (pixels or a %), else the size's default."""
    w = (ENV("CRITTER_WIDTH") or "").strip()
    if w and not re.fullmatch(r"\d+%?", w):
        warn(f"width '{w}' should be a number of pixels like 176, or a percentage like 50%; ignoring it")
        w = ""
    return w or DISPLAY_WIDTH[size()]


def float_side():
    f = (ENV("CRITTER_FLOAT") or "none").strip().lower()
    if f not in ("none", "left", "right"):
        warn(f"unknown float '{f}', not floating. Options: none, left, right")
        f = "none"
    return f


def pet_name():
    return (ENV("CRITTER_NAME") or "").strip() or SPECIES[species()]["default_name"]


def api(path):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "commit-critter"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(f"https://api.github.com{path}", headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def msg(text):
    MSG.write_text(text + "\n" if text else "")


def load():
    p = HOME / "state.json"
    if p.exists():
        return json.loads(p.read_text())
    return {"born": TODAY, "age": 0, "hunger": 3, "food_today": 0, "total_food": 0,
            "real_streak": 0, "best_streak": 0, "last_fed": None}


def save(s):
    HOME.mkdir(exist_ok=True)
    (HOME / "state.json").write_text(json.dumps(s, indent=2) + "\n")


def mood(s):
    if s["food_today"] >= 5:
        return "ecstatic"
    h = s["hunger"]
    return "happy" if h <= 2 else "meh" if h <= 4 else "hungry" if h <= 7 else "starving"


def real_activity():
    """Count public events in the last 24h, ignoring this repo so the critter can't feed itself."""
    events = api(f"/users/{USER}/events/public?per_page=100")
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=24)
    counted = {"PushEvent", "PullRequestEvent", "PullRequestReviewEvent", "IssuesEvent",
               "IssueCommentEvent", "CreateEvent", "ReleaseEvent"}
    return sum(
        1 for e in events
        if e["type"] in counted and e["repo"]["name"] != REPO
        and dt.datetime.fromisoformat(e["created_at"].replace("Z", "+00:00")) >= cutoff
    )


# ---------------------------------------------------------------- rendering


def describe(s):
    """The whole card in words: the SVG's title and the README alt text."""
    return (f"{pet_name()} the {species()}, feeling {mood(s)}. Fullness {10 - s['hunger']}/10, "
            f"ate {s['food_today']} today, real-work streak {s['real_streak']}d "
            f"(best {s['best_streak']}d), age {s['age']}d.")


# README width for each card size: whole screen pixels per art pixel keep it crisp; full spans the README.
DISPLAY_WIDTH = {"small": "264", "medium": "576", "full": "100%"}


def block(s):
    home = HOME.as_posix()
    img = f'src="{home}/critter.svg" width="{display_width()}" alt="{html.escape(describe(s))}"'
    side = float_side()
    if side != "none":
        # Floated beside the README's text: a caption line would land next to the card, so the
        # card itself links to the diary and says where it comes from on hover.
        tip = f"{pet_name()}'s diary · fed daily with my real GitHub activity by Commit Critter"
        return f"""{START}
<a href="{home}/diary.md"><img align="{side}" {img} title="{html.escape(tip)}"></a>
{END}"""
    return f"""{START}
<img {img}>

<sub>[diary]({home}/diary.md) · [trophies]({home}/trophies.md) · fed daily with my real GitHub activity by [Commit Critter](https://github.com/{ACTION_REPO}). No work, no food.</sub>
{END}"""


def history(s):
    """Food per day, oldest first. Critters fed before history was kept only know their last day."""
    return s.get("history") or ([s["food_today"]] if s["age"] else [])


def render(s):
    HOME.mkdir(exist_ok=True)
    stats = {"name": pet_name(), "species": species(), "hunger": s["hunger"], "food_today": s["food_today"],
             "streak": s["real_streak"], "best": s["best_streak"], "age": s["age"], "total": s["total_food"],
             "history": history(s)}
    (HOME / "critter.svg").write_text(
        sprites.svg(species(), mood(s), title=describe(s), stats=stats, theme=theme(), size=size()))
    trophies = HOME / "trophies.md"
    if not trophies.exists():  # the README links here from day one
        trophies.write_text("# Trophies\n\n" + NO_TROPHIES)
    text = README.read_text() if README.exists() else ""
    new = block(s)
    if START in text and END in text:
        text = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: new, text, flags=re.S)
    else:
        text = text.rstrip() + ("\n\n" if text.strip() else "") + new + "\n"
    README.write_text(text)


# ---------------------------------------------------------------- commands


def whoami():
    name = (ENV("CRITTER_AUTHOR_NAME") or "").strip()
    email = (ENV("CRITTER_AUTHOR_EMAIL") or "").strip()
    if not (name and email):
        try:
            u = api(f"/users/{USER}")
            name = name or u.get("name") or u["login"]
            # The id+login noreply address is always linked to the account, so commits count.
            email = email or f"{u['id']}+{u['login']}@users.noreply.github.com"
        except Exception as e:
            warn(f"couldn't look up @{USER} ({e}); commits may not count toward your graph. "
                 "Set author-name and author-email inputs.")
            name = name or USER or "commit-critter"
            email = email or "41898282+github-actions[bot]@users.noreply.github.com"
    print(name)
    print(email)


def feed():
    s = load()
    if s["last_fed"] == TODAY:
        return msg("")
    try:
        food = real_activity()
    except Exception as e:  # API trouble: still commit, don't reward or punish
        warn(f"couldn't read activity: {e}")
        food = None
    s["history"] = (history(s) + [food or 0])[-7:]  # before age changes, so day 0 adds no fake entry
    s["age"] += 1
    s["last_fed"] = TODAY
    name = pet_name()
    if food is None:
        s["food_today"] = 0
        save(s); render(s)
        return msg(f"🐾 day {s['age']}: {name} couldn't find the kitchen (API hiccup), napped instead")
    s["food_today"] = food
    s["total_food"] += food
    if food:
        s["hunger"] = max(0, s["hunger"] - min(food, 5))
        s["real_streak"] += 1
        s["best_streak"] = max(s["best_streak"], s["real_streak"])
    else:
        s["hunger"] = min(10, s["hunger"] + 2)
        s["real_streak"] = 0
    save(s); render(s)
    msg(f"🐾 day {s['age']}: {name} ate {food} thing{'s' * (food != 1)} ({mood(s)})")


def diary():
    s = load()
    p = HOME / "diary.md"
    text = p.read_text() if p.exists() else f"# {pet_name()}'s diary\n\n"
    if f"- {TODAY}" in text:
        return msg("")
    m = mood(s)
    HOME.mkdir(exist_ok=True)
    p.write_text(text + f"- {TODAY} · day {s['age']} · {m} · {random.choice(SPECIES[species()]['diary'][m])}\n")
    msg(f"📔 diary: day {s['age']}")


def trophy():
    s = load()
    milestones = {7: "one week of real work", 30: "a month of real work",
                  100: "100 days of real work", 365: "a full year of real work"}
    got = milestones.get(s["real_streak"]) if s["food_today"] else None
    if not got and s["age"] and s["age"] % 100 == 0:
        got = f"{pet_name()} turned {s['age']} days old"
    p = HOME / "trophies.md"
    text = p.read_text() if p.exists() else "# Trophies\n\n"
    if not got or f"- {TODAY}" in text:
        return msg("")
    HOME.mkdir(exist_ok=True)
    p.write_text(text.replace(NO_TROPHIES, "") + f"- {TODAY} · 🏆 {got}\n")
    msg(f"🏆 trophy: {got}")


def preview():
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    demo = {"name": "Pebble", "species": "snail", "hunger": 0, "food_today": 6, "streak": 12, "best": 12,
            "age": 40, "total": 163, "history": [3, 0, 5, 2, 4, 1, 6]}
    for th in sprites.THEMES:
        suffix = "" if th == "light" else f"-{th}"
        for sp in SPECIES:
            for m in MOODS:
                (out / f"{sp}-{m}{suffix}.svg").write_text(sprites.svg(sp, m, title=f"{sp}, {m}", theme=th))
        for z in sprites.SIZES:
            name = "card" + ("" if z == "medium" else f"-{z}") + suffix
            (out / f"{name}.svg").write_text(
                sprites.svg("snail", "ecstatic", title="Pebble the snail, ecstatic", stats=demo, theme=th, size=z))


if __name__ == "__main__":
    {"whoami": whoami, "feed": feed, "diary": diary, "trophy": trophy, "preview": preview}[sys.argv[1]]()
