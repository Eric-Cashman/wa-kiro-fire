#!/usr/bin/env python3
"""
Build the compact JSON files the webpage loads:

  wa_counties.geojson  - Washington county boundary polygons (from US counties file)
  fire_stats.json      - per-county aggregates, per-year counts, cause breakdown,
                         and a forecast (next-year fire likelihood + trend).
  fire_points.json     - individual fire locations keyed by year, for the
                         year-aware "Fire locations" map dot layer.

Run:  python3 build_data.py
"""

import json
import math
from collections import defaultdict

SRC_FIRE     = "DNR_Fire_Statistics_2008-Present.geojson"
SRC_US       = "us_counties.json"
OUT_COUNTIES = "wa_counties.geojson"
OUT_STATS    = "fire_stats.json"
OUT_POINTS   = "fire_points.json"

WA_STATE_FIPS = "53"

# Keep only fires from this year onward (dataset is "2008–present").
MIN_KEEP_YEAR = 2008

MONTHS = ['JANUARY','FEBRUARY','MARCH','APRIL','MAY','JUNE',
          'JULY','AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER']

# Washington county populations — ~2023 Census/OFM estimates (public figures).
# Used to show "people in the area at risk" and to scale the evacuation budget.
COUNTY_POPULATION = {
    "KING": 2269675, "PIERCE": 921130, "SNOHOMISH": 827957, "SPOKANE": 539339,
    "CLARK": 516779, "THURSTON": 294793, "KITSAP": 275611, "YAKIMA": 256728,
    "WHATCOM": 226847, "BENTON": 212791, "SKAGIT": 129523, "COWLITZ": 110730,
    "GRANT": 99123, "FRANKLIN": 98678, "ISLAND": 86857, "LEWIS": 82149,
    "CHELAN": 79889, "GRAYS HARBOR": 76350, "CLALLAM": 77805, "WALLA WALLA": 63066,
    "MASON": 67326, "OKANOGAN": 42777, "DOUGLAS": 43429, "STEVENS": 46849,
    "WHITMAN": 47804, "KITTITAS": 45762, "JEFFERSON": 33108,
    "ADAMS": 20613, "PACIFIC": 24063, "KLICKITAT": 23150, "SAN JUAN": 17788,
    "PEND OREILLE": 13767, "FERRY": 7406, "LINCOLN": 11399, "ASOTIN": 22285,
    "SKAMANIA": 12310, "WAHKIAKUM": 4475, "COLUMBIA": 3952, "GARFIELD": 2296,
}


# ────────────────────────────────────────────────────────────────────
# 1. Washington county boundaries
# ────────────────────────────────────────────────────────────────────
def build_counties():
    print("Reading US counties …")
    with open(SRC_US) as f:
        us = json.load(f)

    wa_feats = []
    for ft in us["features"]:
        if ft["properties"].get("STATE") == WA_STATE_FIPS:
            name = ft["properties"]["NAME"].upper()
            # normalise to match fire data labels (ST. -> none appear; keep as-is)
            ft["properties"] = {
                "NAME": name,
                "FIPS": ft["properties"]["GEO_ID"][-5:],
            }
            wa_feats.append(ft)

    out = {"type": "FeatureCollection", "features": wa_feats}
    with open(OUT_COUNTIES, "w") as f:
        json.dump(out, f)
    print(f"  wrote {OUT_COUNTIES}  ({len(wa_feats)} counties)")
    return {ft["properties"]["NAME"] for ft in wa_feats}


# ────────────────────────────────────────────────────────────────────
# 2. Fire aggregation + forecast model
# ────────────────────────────────────────────────────────────────────
def linreg_slope(years, counts):
    """Ordinary least squares slope of counts vs. year (fires per year)."""
    n = len(years)
    if n < 2:
        return 0.0
    mx = sum(years) / n
    my = sum(counts) / n
    num = sum((years[i] - mx) * (counts[i] - my) for i in range(n))
    den = sum((years[i] - mx) ** 2 for i in range(n))
    return num / den if den else 0.0


def build_stats(wa_names):
    print("Reading fire data (this is the big one) …")
    with open(SRC_FIRE) as f:
        fire = json.load(f)

    counties = {}
    years_seen = set()

    def blank(name):
        return {
            "name": name,
            "count": 0,
            "acres": 0.0,
            "byYear": defaultdict(int),       # year -> fire count
            "acresByYear": defaultdict(float),
            "months": defaultdict(int),       # MONTH -> count
            "gcauses": defaultdict(int),      # general cause -> count
            "lat": 0.0, "lon": 0.0, "_n": 0,
        }

    for ft in fire["features"]:
        p = ft["properties"]
        name = (p.get("COUNTY_LABEL_NM") or "NO DATA").strip().upper()
        if name in ("NO DATA", ""):
            continue

        # Keep only 2008–present (drop legacy 2000–2007 records).
        dt = p.get("DSCVR_DT")
        yr = int(dt[:4]) if dt else None
        if yr is not None and yr < MIN_KEEP_YEAR:
            continue

        if name not in counties:
            counties[name] = blank(name)
        c = counties[name]

        acres = p.get("ACRES_BURNED") or 0.0
        c["count"] += 1
        c["acres"] += acres

        if yr is not None:
            c["byYear"][yr] += 1
            c["acresByYear"][yr] += acres
            years_seen.add(yr)

        mo = (p.get("DSCVR_MONTH") or "").strip().upper()
        if mo in MONTHS:
            c["months"][mo] += 1

        gc = p.get("FIREGCAUSE_LABEL_NM") or "Unknown"
        c["gcauses"][gc] += 1

        lat = p.get("LAT_COORD"); lon = p.get("LON_COORD")
        if lat and lon:
            c["lat"] += lat; c["lon"] += lon; c["_n"] += 1

    min_year = min(years_seen)
    max_year = max(years_seen)
    all_years = list(range(min_year, max_year + 1))
    n_years = len(all_years)
    print(f"  years {min_year}–{max_year}  ({n_years} yrs), {len(counties)} counties with data")

    # max average annual count across counties -> normalises the risk %
    # also track max recent-3yr average -> normalises the forecast probability
    max_avg = 0.0
    max_recent = 0.0
    for c in counties.values():
        avg = c["count"] / n_years
        if avg > max_avg:
            max_avg = avg
        ry = [c["byYear"].get(y, 0) for y in all_years][-3:]
        ravg = sum(ry) / len(ry) if ry else 0
        if ravg > max_recent:
            max_recent = ravg

    out_counties = {}
    for name, c in counties.items():
        n = c["_n"] or 1
        lat = c["lat"] / n
        lon = c["lon"] / n

        # yearly series over the full span (zero-fill missing years)
        yearly = [c["byYear"].get(y, 0) for y in all_years]
        avg_annual = c["count"] / n_years

        # ── FORECAST MODEL ──────────────────────────────────────────
        # (1) baseline rate = average fires/yr
        # (2) trend = OLS slope over the recorded years
        # (3) recent weighting: average of last 3 yrs vs. long-run avg
        slope = linreg_slope(all_years, yearly)
        recent = yearly[-3:] if len(yearly) >= 3 else yearly
        recent_avg = sum(recent) / len(recent)

        # predicted next-year count = blend of long-run avg, recent avg, trend
        predicted = max(0.0, 0.5 * recent_avg + 0.5 * avg_annual + slope)

        # ── FIRE LIKELIHOOD NEXT YEAR (differentiated 0–100%) ───────
        # NOT "chance of any fire" (that's ~100% everywhere in WA and
        # therefore useless). Instead a comparative likelihood score so
        # counties actually spread out. Blend of:
        #   consistency – fraction of recorded years that had >=1 fire
        #   intensity   – this county's recent activity vs. the busiest
        #   momentum    – small boost/penalty from the trend direction
        years_with_fire = sum(1 for v in yearly if v > 0)
        consistency = years_with_fire / n_years               # 0..1
        intensity   = (recent_avg / max_recent) if max_recent else 0  # 0..1
        intensity   = min(1.0, intensity)
        # momentum: up to +/-10 points scaled by trend slope
        momentum = max(-0.10, min(0.10, slope / 20.0))

        likelihood = 0.55 * consistency + 0.45 * intensity + momentum
        prob_any = round(max(0.0, min(0.99, likelihood)) * 100, 1)

        # relative risk score 0-100 (share of the busiest county's avg rate)
        # relative risk score 0-100 (share of the busiest county's avg rate).
        # kept as a numeric indicator; the categorical risk_level below is
        # assigned later by PERCENTILE rank so the labels spread across all
        # counties instead of collapsing to LOW.
        risk_pct = round(min(100, (avg_annual / max_avg) * 100)) if max_avg else 0
        risk_level = "LOW"  # placeholder; set in the ranking pass after the loop

        # trend direction
        if   slope > 0.5:  trend = "rising"
        elif slope < -0.5: trend = "falling"
        else:              trend = "stable"

        # ── BUDGET / RESCUE COST MODEL ──────────────────────────────
        # Rough PLANNING estimate (NOT an official budget) of what it
        # could cost to respond to next year's predicted fire activity.
        # Three components, each given a low–high range:
        #
        #   suppression  = predicted acres * per-acre suppression cost
        #   evacuation   = predicted fires * avg people-response cost
        #   wildlife     = predicted acres * habitat-protection cost
        #
        # Per-acre / per-incident coefficients are ballpark figures drawn
        # from published ranges for western US wildfire response.
        avg_acres_per_fire = (c["acres"] / c["count"]) if c["count"] else 0
        predicted_acres = predicted * avg_acres_per_fire

        # suppression: ~$800–$3,500 per acre (varies hugely by terrain/access)
        supp_lo = predicted_acres * 800
        supp_hi = predicted_acres * 3500

        # evacuation / people rescue:
        #   base per-incident mobilization (~$15k–$60k each) PLUS a
        #   population-exposure term. We estimate the share of county
        #   residents plausibly in an evacuation footprint from the
        #   predicted acreage, then ~$50–$180 per potentially-affected
        #   person (alerts, sheltering, transport, services).
        population = COUNTY_POPULATION.get(name, 0)
        # exposure fraction: scales with predicted acres, capped at 8% of county
        exposure_frac = min(0.08, predicted_acres / 2_000_000)
        people_exposed = round(population * exposure_frac)
        evac_lo = predicted * 15000 + people_exposed * 50
        evac_hi = predicted * 60000 + people_exposed * 180

        # wildlife / habitat protection: ~$120–$500 per acre
        # (rehab, erosion control, habitat restoration, animal rescue)
        wild_lo = predicted_acres * 120
        wild_hi = predicted_acres * 500

        total_lo = supp_lo + evac_lo + wild_lo
        total_hi = supp_hi + evac_hi + wild_hi

        budget = {
            "predictedAcres": round(predicted_acres),
            "totalLow":  round(total_lo),
            "totalHigh": round(total_hi),
            "suppression": {"low": round(supp_lo), "high": round(supp_hi)},
            "evacuation":  {"low": round(evac_lo), "high": round(evac_hi)},
            "wildlife":    {"low": round(wild_lo), "high": round(wild_hi)},
            "peopleExposed": people_exposed,
        }

        # peak months (top 3)
        month_counts = {m: c["months"].get(m, 0) for m in MONTHS}
        peak_months = sorted(month_counts.items(), key=lambda x: -x[1])
        peak_months = [m for m, v in peak_months if v > 0][:3]

        # causes sorted
        causes = sorted(c["gcauses"].items(), key=lambda x: -x[1])
        top_cause = causes[0][0] if causes else "Unknown"

        out_counties[name] = {
            "name": name,
            "count": c["count"],
            "acres": round(c["acres"]),
            "population": COUNTY_POPULATION.get(name, 0),
            "lat": round(lat, 5),
            "lon": round(lon, 5),
            "avgAnnual": round(avg_annual, 1),
            "yearly": dict(zip(all_years, yearly)),
            "acresByYear": {y: round(c["acresByYear"].get(y, 0)) for y in all_years},
            "months": month_counts,
            "peakMonths": peak_months,
            "causes": [[k, v] for k, v in causes],
            "topCause": top_cause,
            "riskPct": risk_pct,
            "riskLevel": risk_level,
            # forecast
            "forecast": {
                "predictedCount": round(predicted, 1),
                "probAny": prob_any,          # % chance of >=1 fire next year
                "trend": trend,
                "slope": round(slope, 2),
                "recentAvg": round(recent_avg, 1),
                "budget": budget,
            },
        }

    # ── RISK LEVEL by PERCENTILE RANK ───────────────────────────────
    # Rank all counties by average annual fires, then split into tiers
    # so the labels are spread sensibly instead of collapsing to LOW:
    #   top 15%  -> CRITICAL
    #   next 25% -> HIGH        (to 40th percentile from top)
    #   next 30% -> MEDIUM      (to 70th percentile from top)
    #   rest     -> LOW
    ranked = sorted(out_counties.values(), key=lambda c: c["avgAnnual"], reverse=True)
    total = len(ranked)
    for i, c in enumerate(ranked):
        pct_from_top = i / total  # 0 = busiest
        if   pct_from_top < 0.15: c["riskLevel"] = "CRITICAL"
        elif pct_from_top < 0.40: c["riskLevel"] = "HIGH"
        elif pct_from_top < 0.70: c["riskLevel"] = "MEDIUM"
        else:                     c["riskLevel"] = "LOW"

    stats = {
        "meta": {
            "minYear": min_year,
            "maxYear": max_year,
            "years": all_years,
            "totalFires": sum(c["count"] for c in counties.values()),
            "totalAcres": round(sum(c["acres"] for c in counties.values())),
        },
        "counties": out_counties,
    }

    with open(OUT_STATS, "w") as f:
        json.dump(stats, f)
    print(f"  wrote {OUT_STATS}")

    # sanity: counties in fire data not matched to a boundary
    unmatched = set(out_counties) - wa_names
    if unmatched:
        print(f"  NOTE: fire counties with no boundary match: {sorted(unmatched)}")


# ────────────────────────────────────────────────────────────────────
# 3. Individual fire points keyed by year (for the dot layer)
# ────────────────────────────────────────────────────────────────────
def build_points():
    print("Extracting individual fire points per year …")
    with open(SRC_FIRE) as f:
        fire = json.load(f)

    by_year = defaultdict(list)
    for ft in fire["features"]:
        p = ft["properties"]
        g = ft.get("geometry") or {}
        coords = g.get("coordinates")
        if not coords:
            continue
        dt = p.get("DSCVR_DT")
        if not dt:
            continue
        yr = int(dt[:4])
        if yr < MIN_KEEP_YEAR:
            continue

        lon, lat = round(coords[0], 5), round(coords[1], 5)
        acres = round(p.get("ACRES_BURNED") or 0, 2)
        name = p.get("INCIDENT_NM") or "Unnamed"
        county = (p.get("COUNTY_LABEL_NM") or "").strip().title()
        cause = p.get("FIREGCAUSE_LABEL_NM") or "Unknown"
        month = (p.get("DSCVR_MONTH") or "").strip().title()

        # compact array form keeps the file small:
        # [lat, lon, acres, name, county, cause, month]
        by_year[yr].append([lat, lon, acres, name, county, cause, month])

    out = {str(y): by_year[y] for y in sorted(by_year)}
    with open(OUT_POINTS, "w") as f:
        json.dump(out, f)
    total = sum(len(v) for v in by_year.values())
    print(f"  wrote {OUT_POINTS}  ({total} points across {len(by_year)} years)")


if __name__ == "__main__":
    wa_names = build_counties()
    build_stats(wa_names)
    build_points()
    print("Done.")
