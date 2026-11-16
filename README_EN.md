# LocalDate — a local date-plan generator skill for AI assistants

> Not "go see a movie". Instead: *"Saturday afternoon, go to the strawberry greenhouse in Fanzhu Village, Caolan Township — one basket each, pick whichever turns red, weigh it at the door, 70 RMB for a 4-jin box. Text her: 'Greenhouses open in December, one basket each, pick as much as you want.'"*

A **Skill** for AI assistants. Say "where should we go this weekend" and get 15 plans that are real, priced, navigable, and each ends with a message you can copy and send. Rank them once — it learns your taste.

**One-line install** (paste into your assistant, replacing the URL):

```
Download and install https://github.com/<your-name>/localdate as a local Skill,
then read city-packs/huainan/ and give me one round of date plans.
```

No pip, no API key, no env vars.

## Why not another date-ideas generator

Existing open-source projects (Perfect-Date, DateIdeas, Couple's Date Randomizer) are Western generic templates plus LLM improvisation. They hallucinate venues, have no seasonal-event layer, and never learn your taste. LocalDate adds exactly three things:

1. **City Pack** — a real POI database, every row tagged with a source. 800+ entries in the Huainan pack.
2. **Seasonal event layer** — swan season, red-leaf windows, lantern festivals, first-snow windows, strawberry season. "Miss it and wait a year."
3. **Ranking self-learning** — you reply with numbers (`3 4 6 7 8`); features update via Bradley-Terry / Elo, with time decay and a UCB exploration bonus. Rejections only lower scores; nothing is permanently banned.

## Output shape

Every plan carries four mandatory fields: **navigable address / price / time window / one sendable invitation line**. Missing any one counts as unfinished.

## Hard rules

1. No source, no entry; no search, no output.
2. Venue triad: name + address + price bracket.
3. Self-check opening status against the last three years of reviews/official notices — never push this back to the user.
4. At most one repeat per round; changing time window / core activity / ritual / season to the point it reads as a different plan counts as a variant, not a repeat.

## Docs

- [`QUICKSTART.md`](QUICKSTART.md) — 3 steps
- [`ALGORITHM.md`](ALGORITHM.md) — scoring model
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — how to add a city pack
- [`examples/huainan-round9.md`](examples/huainan-round9.md) — a full 15-plan round

MIT for code; CC BY-SA 4.0 for city-pack data.
