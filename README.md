# 🔥 Washington State Wildfire Risk Map

An interactive web map that shows where wildfires happen across Washington
State, how likely each county is to burn, and what's at stake — for the public
and for firefighters.

Built from **~30,500 real fire records (2008–2026)** published by the
Washington Department of Natural Resources (DNR).

![type: static web app](https://img.shields.io/badge/type-static%20web%20app-blue)
![map: Leaflet](https://img.shields.io/badge/map-Leaflet%20(no%20API%20key)-green)
![data: WA%20DNR](https://img.shields.io/badge/data-WA%20DNR%20%2B%20NIFC-orange)

---

## What it does

- 🗺️ **County map** colored by fire risk, with **Street** and **Satellite** views.
- 🔎 **Search** any of Washington's 39 counties.
- 📊 **Click a county** for a detailed card: forecast, risk level, causes,
  monthly/yearly fire patterns, estimated response budget, affected population,
  and at-risk wildlife.
- 🎚️ **Year slider (2008–2026)** — scrub through time and watch the map change.
- 📍 **Fire locations layer** — see every individual fire for a selected year,
  as dots that move as you change the year.
- 🚒 **Live fires (now)** — real-time active wildfires in WA from the national feed.
- 🖱️ **Hover a county** — the top stats bar updates to that county instantly.

---

## How to run it

This is a **static site** — no build server, no account, no API key. You just
need to serve the folder over `http://` (browsers block loading the data files
from a bare `file://` path).

```bash
cd wa-fire-kiro
python3 -m http.server 8000
```

Then open **http://localhost:8000** in your browser.

> **Tip:** if you've opened it before and something looks stale, hard-refresh
> with **Cmd+Shift+R** (Mac) / **Ctrl+Shift+R** (Windows).

---

## Rebuilding the data

The map doesn't read the giant 35 MB source file directly — a small Python
script pre-chews it into compact files the browser loads quickly.

Run this whenever the source data changes:

```bash
python3 build_data.py
```

It reads `DNR_Fire_Statistics_2008-Present.geojson` and writes:

| Output file | What it holds |
|---|---|
| `fire_stats.json` | Per-county totals, yearly numbers, causes, forecast, budget (~58 KB) |
| `fire_points.json` | Every individual fire location, grouped by year (~2.3 MB, loads only when needed) |
| `wa_counties.geojson` | Washington county boundary shapes for the colored map |

> The script needs a US counties boundary file named `us_counties.json` in the
> folder to build `wa_counties.geojson`. It's a one-time public download:
> ```bash
> curl -sL "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json" -o us_counties.json
> ```

---

## What's in the folder

```
wa-fire-kiro/
├── index.html                               ← the whole app (map + UI + logic)
├── wildlife_data.js                         ← curated wildlife / habitat reference
├── build_data.py                            ← turns raw data into the files below
│
├── DNR_Fire_Statistics_2008-Present.geojson ← raw source data (35 MB)
├── fire_stats.json                          ← per-county aggregates + forecast
├── fire_points.json                         ← individual fire locations by year
├── wa_counties.geojson                      ← county boundary shapes
│
├── README.md                                ← you are here
└── HOW_IT_WORKS.md                          ← plain-language explainer of every number
```

---

## Where the data comes from

- **Historical fires:** [WA DNR Fire Statistics 2008–Present](https://geo.wa.gov/datasets/wadnr::dnr-fire-statistics-2008-present/explore)
- **Live active fires:** [NIFC / WFIGS Current Wildland Fire Incident Locations](https://www.nifc.gov/) (queried live from their public map service)
- **County boundaries:** US Census county shapes (public domain)
- **Populations:** US Census / WA OFM estimates (~2023)

---

## Important honesty note

Some numbers on this map are **estimates and forecasts**, not official figures:
the next-year fire likelihood, the response budget, the damage estimate, and
the "people exposed" count are all **planning estimates** derived from the
historical record. They're meant to help compare counties and start a
conversation — not to serve as official emergency-management figures.

See **[HOW_IT_WORKS.md](HOW_IT_WORKS.md)** for exactly how each number is
calculated.

---

## Tech, briefly

- **Leaflet** for the map (free, open-source, no API key)
- Plain **HTML / CSS / JavaScript** — no framework, no build tools
- **Python 3** (standard library only) for the one-time data prep
- Map tiles from OpenStreetMap (Street) and Esri (Satellite)
