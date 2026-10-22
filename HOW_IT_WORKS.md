# 🔎 How It Works — Plain-Language Guide

This explains **every number and feature** on the Washington Wildfire Risk Map,
in everyday language. It's written so you can present the project and answer
"where did that number come from?" for anything on screen.

The golden rule throughout: **the map only knows what actually happened from
2008 to 2026.** Every "prediction" is just smart pattern-reading of that
history — not a crystal ball, and not fed by live weather or satellites.

---

## The big picture

We started with one giant file: about **30,500 real wildfire records** from the
Washington Department of Natural Resources, covering **2008 to 2026**. Each
record is one fire, and it tells us:

- **where** it was (latitude/longitude and county),
- **when** (date and month),
- **how big** (acres burned),
- **why** (cause — lightning, campfire, debris burning, etc.).

Everything on the map is built from those four facts, added up in different ways.

---

## The map colors (choropleth)

Each county is shaded from **green (low)** to **dark red (high)**. What the color
*means* depends on the "Color by" dropdown and the year slider:

- **All years + "Relative risk"** → how much this county burns compared to others.
- **A specific year** → how many **acres burned that year** (the map auto-switches
  to acres so bad fire years visibly light up).
- You can also color by total fires, forecast %, or acres manually.

A pale, nearly-transparent county means little or no fire for that view.

---

## The year slider (2008–2026)

Drag it (or press ▶ to auto-play) to move through time. As you do:

- County **colors** change to that year's acres burned.
- The **top stats bar** shows that year's fires, acres, damage, and worst-hit county.
- If the **Fire locations** layer is on, the dots jump to that year's fires.
- **Live fires** hide (they're today's fires — they don't belong in 2015).

---

## The three fire layers (and why they're different)

This trips people up, so here's the clear version:

| Layer | What it shows | Changes with the year slider? |
|---|---|---|
| **County colors** | Each county shaded by how much it burned | ✅ Yes |
| **Fire locations** | A dot for **every individual fire** in the chosen year | ✅ Yes |
| **Live fires (now)** | Wildfires burning in WA **right now**, from a live national feed | ❌ No — it's always "today" |

So **Fire locations** is the historical "where did fires actually happen,"
and **Live fires** is "what's on fire this minute." They're deliberately kept
separate, and live fires switch off when you look at a past year.

---

## The county detail card (click any county)

### "X% chance of ≥1 fire next year"

This is a **comparative likelihood score**, 0–100%. Here's the honest story:

The *literal* chance of at least one fire next year is basically 100% for almost
every WA county — fires are that common here. A number that says 100% everywhere
is useless. So instead we built a score that actually **spreads counties apart**
and lets you compare them. It blends three things:

1. **Consistency** — in how many of the recorded years did this county have fires?
2. **Intensity** — how active has it been lately, versus the busiest county?
3. **Momentum** — is its fire trend rising or falling?

Result: Stevens/Spokane land near 99%, Okanogan ~74%, King ~45%, Adams ~15%.
Higher = this county is a bigger, more consistent fire area than most.

> **If asked:** "It's a relative risk ranking, not a literal probability —
> because literal probability is ~100% everywhere and tells you nothing."

### Risk level (CRITICAL / HIGH / MEDIUM / LOW)

We rank all 39 counties by their average yearly fire count and split them into
tiers by **percentile**:

- **CRITICAL** — the top 15% (the ~6 worst counties)
- **HIGH** — the next 25%
- **MEDIUM** — the next 30%
- **LOW** — the bottom 30%

We use percentiles (not fixed cutoffs) so the labels spread sensibly instead of
everything collapsing into "LOW."

### The forecast trend (📈 rising / 📉 falling / ➡️ stable)

We draw a best-fit line through the county's year-by-year fire counts. If the
line slopes up over time, it's "rising"; down, "falling"; flat, "stable." The
"~N fires predicted" number is a blended estimate of next year's fire count from
the long-run average, the recent average, and that trend.

### Estimated response budget 💰

A **rough planning estimate** of what it might cost to respond to next year's
predicted fire activity. Three parts, each a low–high range:

- **🧯 Fire suppression** — predicted acres × a per-acre firefighting cost (~$800–$3,500/acre)
- **🚗 People / evacuation** — a per-fire mobilization cost **plus** a cost per
  person likely in an evacuation zone (based on county population and predicted acres)
- **🦌 Wildlife / habitat** — predicted acres × a per-acre habitat-protection cost (~$120–$500/acre)

> **If asked:** "These are ballpark figures from published western-US wildfire
> costs. It's a planning estimate to compare counties, not an official budget."

### Affected population

- **County population** — total residents (Census/OFM ~2023).
- **Est. people exposed** — a modeled estimate of how many residents could fall
  inside an evacuation footprint, scaled from the predicted acreage. (Not a
  precise count — a real one would need the exact fire's location.)

### Cause of fires

The actual breakdown of **why** this county's fires started, from the records —
lightning, debris burning, campfires, etc. — with percentages.

### When fires happen (by month) & Fires by year

Simple bar charts straight from the data: which months and which years this
county saw the most fires. Great for spotting the summer fire season.

### 🦌 Wildlife & habitat at risk

Washington's 39 counties are grouped into **5 ecological regions** (shrub-steppe,
dry eastern forest, Cascade forest, wet westside forest, Blue Mountains/Palouse).
For each region we list notable species and habitats with:

- a **conservation status** badge — 🛑 Endangered, ⚠️ Threatened, ● Sensitive
  (per WA/federal listings), and
- a **fire-impact note** — some species are badly harmed (sage-grouse lose
  breeding grounds for decades), while others actually **benefit** from
  low-intensity fire (elk love the regrowth; ponderosa pine survives it).

> **If asked:** "This is curated reference by ecological region from WA Fish &
> Wildlife facts — not live animal tracking, which doesn't exist publicly."

---

## The estimated damage number 💥

When you pick a year, we show estimated fire **damage** (property, timber, and
resource loss) as a dollar range: roughly **$5,000–$15,000 per acre burned**.
Like the budget, it's a ballpark from published figures — real losses swing
enormously depending on whether a fire hit homes, timber, or empty rangeland.

---

## The top stats bar

Four (or five when hovering) quick chips:

- **Default:** total fires, acres, estimated damage, and the highest-forecast county.
- **Pick a year:** the numbers become that year's, and the last chip switches to
  **the county that burned the most acres that year**.
- **Hover a county:** the whole bar instantly shows that county's name, fires,
  acres, damage, and risk.

---

## Why no Google Maps / API key?

We use **Leaflet**, a free open-source map library, with free map tiles. That
means no Google account, no billing, no API key, and it works offline once
loaded. Google's Street View panorama isn't included because it requires a paid
key — and this app is about county-level fire data, not standing on a street corner.

---

## One-sentence summary for your audience

> "This map reads 18 years of real Washington wildfire records and turns them
> into a picture of **where fires happen, how likely each county is to burn,
> who and what is at risk, and roughly what a response would cost** — with every
> estimate clearly labeled as an estimate."
