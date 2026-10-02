# Commit-Critter

A pet that lives in this README. A bot visits every day at noon IST and feeds it
whatever I actually did on GitHub in the last 24 hours. No real work means no food.

```
       (o.o)
   @  ~~~~~~~>
```

| | |
|---|---|
| Mood | **happy** |
| Fullness | `████████░░` |
| Ate today | 1 |
| Age | 1 days (born 2026-10-02) |
| Lifetime food | 1 |
| Real-work streak | 1 days (best: 1) |

[Diary](diary.md) · [Trophies](trophies.md)
=======
# Commit Critter 🐌🦀🐱🫧

A tiny pet that lives in your GitHub README and eats your real GitHub activity.

Once a day, a GitHub Action visits your critter and feeds it whatever you actually did on GitHub in the last 24 hours: pushes, PRs, reviews, issues. Do real work and it thrives. Skip a few days and it gets hungry, and everyone visiting your profile can see it.

```text
     \(^o^)/
   @  ~~~~~~~>   *zooms at 0.03 km/h*
```

**Pebble** the snail · **ecstatic** · fullness `██████████` · ate 6 today · real-work streak 12d (best 12d) · age 40d

---

## Setup (2 minutes)

1. Open your **profile repo**, the one named after you (`github.com/<you>/<you>`). Any public repo works, but that's the one shown on your profile.
2. Create `.github/workflows/commit-critter.yml` with:

```yaml
name: Commit Critter
on:
  schedule:
    - cron: "30 6 * * *"   # once a day; pick a mid-day time in your timezone (UTC)
  workflow_dispatch:
permissions:
  contents: write
jobs:
  feed:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: Diacod-I/commit-critter@v1
        with:
          species: snail   # snail, crab, cat, or slime
```

3. On the **Actions** tab, click **Commit Critter → Run workflow** to hatch it.

That's it, with no tokens or secrets to set up. The critter appears at the bottom of your README. To put it somewhere else, add these two lines wherever you want it and it'll stay there:

```md
<!-- COMMIT-CRITTER:START -->
<!-- COMMIT-CRITTER:END -->
```

## The critters

| snail | crab | cat | slime |
|---|---|---|---|
| <pre>       (o.o)<br>   @  ~~~~~~~></pre> | <pre>(\/)  (°,,,,°)  (\/)</pre> | <pre> /\_/\<br>( o.o )<br> > ^ <</pre> | <pre>  .-"""-.<br> (  o o  )<br>  '-----'</pre> |

Each has five moods (ecstatic → happy → meh → hungry → starving) and its own diary voice.

## Options

| input | default | |
|---|---|---|
| `species` | `snail` | `snail`, `crab`, `cat`, `slime` |
| `pet-name` | per species | Pebble, Clawdia, Biscuit, Gloop |
| `readme` | `README.md` | which file to draw in |
| `github-user` | repo owner | whose activity feeds it |
| `author-name` / `author-email` | your profile | commit author; the default noreply address always counts toward your graph |
| `push` | `true` | `false` for a dry run |

## How it works

Each run makes **1–3 commits** as you:

1. **Feed:** reads your public events from the last 24h, updates `.critter/state.json`, and redraws the README.
2. **Diary:** appends an entry to `.critter/diary.md` in the critter's voice.
3. **Trophy:** only on milestone days (7, 30, 100 or 365 days of real work in a row) → `.critter/trophies.md`.

Activity in the critter's own repo is ignored, so it can't feed itself. If GitHub's API has a hiccup, the critter naps: it still commits, but it isn't rewarded or punished.

## FAQ

**Isn't this just a streak bot?**
Partly, and it says so: the commits keep your graph green. What's different is that the critter tells the truth. Your graph can be green while your snail is clearly starving in its shell. It's a small daily nudge to go do something real.

**Will the commits count on my contribution graph?**
Yes, if the repo is public (or you've enabled private contributions) and the commits land on the default branch. By default they're authored as `<id>+<login>@users.noreply.github.com`, which GitHub always links to your account.

**What counts as food?**
Public pushes, PRs, PR reviews, issues, issue comments, new branches/repos and releases. Private-repo activity doesn't show up in the public events API, so it isn't counted.

**Why does my scheduled run sometimes start late?**
GitHub delays scheduled workflows when it's busy, sometimes by 30+ minutes. That's why the example runs mid-day: so it never slips into the next date.

## Contributing

New critters are the easiest contribution: add an entry to `SPECIES` in `critter.py` with art and diary lines for all five moods, then run the tests:

```bash
python3 -m unittest discover -v tests
```

## License

MIT
