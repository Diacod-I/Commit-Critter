# Commit Critter 🐌🦀🐱🫧

A tiny pet that lives in your GitHub README and eats your real GitHub activity.

Once a day, a GitHub Action visits your critter and feeds it whatever you actually did on GitHub in the last 24 hours: pushes, PRs, reviews, issues. Do real work and it thrives. Skip a few days and it gets hungry, and everyone visiting your profile can see it.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/card-dark.svg">
  <img src="assets/card.svg" width="576" alt="Pebble the snail, feeling ecstatic. Fullness 10/10, ate 6 today, real-work streak 12d (best 12d), age 40d.">
</picture>

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
          # theme: dark    # light (default) or dark
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
| <img src="assets/snail-happy.svg" width="200" alt="snail"> | <img src="assets/crab-happy.svg" width="200" alt="crab"> | <img src="assets/cat-happy.svg" width="200" alt="cat"> | <img src="assets/slime-happy.svg" width="200" alt="slime"> |

Each has five moods and its own diary voice. The critter and its stats are drawn as one animated SVG card saved to `.critter/critter.svg`, so it bobs, blinks and sulks right in your README:

| ecstatic | happy | meh | hungry | starving |
|---|---|---|---|---|
| <img src="assets/cat-ecstatic.svg" width="160" alt="ecstatic"> | <img src="assets/cat-happy.svg" width="160" alt="happy"> | <img src="assets/cat-meh.svg" width="160" alt="meh"> | <img src="assets/cat-hungry.svg" width="160" alt="hungry"> | <img src="assets/cat-starving.svg" width="160" alt="starving"> |

## Options

| input | default | |
|---|---|---|
| `species` | `snail` | `snail`, `crab`, `cat`, `slime` |
| `theme` | `light` | `light` or `dark` card colours; `dark` sits well next to dark stat widgets |
| `pet-name` | per species | Pebble, Clawdia, Biscuit, Gloop |
| `readme` | `README.md` | which file to draw in |
| `github-user` | repo owner | whose activity feeds it |
| `author-name` / `author-email` | your profile | commit author; the default noreply address always counts toward your graph |
| `push` | `true` | `false` for a dry run |

## How it works

Each run makes **1–3 commits** as you:

1. **Feed:** reads your public events from the last 24h, updates `.critter/state.json`, redraws the sprite in `.critter/critter.svg`, and updates the README.
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

New critters are the easiest contribution: draw a body grid in `sprites.py` (fill colours only; the outline, face and mood effects are added for you), add diary lines for all five moods to `SPECIES` in `critter.py`, then regenerate the previews and run the tests:

```bash
python3 critter.py preview assets
python3 -m unittest discover -v tests
```

## License

MIT
