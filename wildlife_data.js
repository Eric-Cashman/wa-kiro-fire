// ═══════════════════════════════════════════════════════════════════
//  WASHINGTON WILDLIFE & HABITAT — FIRE IMPACT REFERENCE
// ───────────────────────────────────────────────────────────────────
//  Curated reference content (NOT live tracking data). Species and
//  fire-impact notes are based on well-established WA Dept. of Fish &
//  Wildlife / ecology facts about which species occupy each ecological
//  region and how wildfire affects their habitat.
//
//  Each county maps to an ECOREGION. Each ecoregion lists notable
//  species/habitats with:
//    impact:  'harm'      – fire is a serious threat / habitat loss
//             'mixed'     – depends on severity; moderate risk
//             'benefit'   – fire-adapted; low/intensity fire helps
//    level:   short label shown as a badge
//    note:    one-line plain-language explanation
// ═══════════════════════════════════════════════════════════════════

const ECOREGIONS = {

  // ── Eastern shrub-steppe / Columbia Basin (dry, grass & sage) ──
  shrubsteppe: {
    label: 'Columbia Basin Shrub-Steppe',
    blurb: 'Dry sagebrush & grassland. Fires here are often large and fast; ' +
           'native sagebrush does NOT recover quickly, so repeated fire permanently degrades habitat.',
    species: [
      { name: 'Greater Sage-Grouse',     status: 'Endangered', impact: 'harm',    level: 'Severe', note: 'Depends on old sagebrush; fire destroys breeding leks and can take decades to recover. State-endangered.' },
      { name: 'Pygmy Rabbit',            status: 'Endangered', impact: 'harm',    level: 'Severe', note: 'Needs dense mature sagebrush for cover and food; fire wipes out colonies. Endangered in WA.' },
      { name: 'Mule Deer',               status: 'Stable',     impact: 'mixed',   level: 'Moderate', note: 'Lose winter browse to fire but can relocate; large burns reduce forage for years.' },
      { name: 'Sharp-tailed Grouse',     status: 'Threatened', impact: 'harm',    level: 'High',   note: 'Shrub-steppe specialist; loss of shrub cover removes winter habitat. State-threatened.' },
      { name: 'Sagebrush (habitat)',     status: 'Habitat',    impact: 'harm',    level: 'Severe', note: 'Big sagebrush is killed by fire and regrows slowly; invasive cheatgrass often takes over, fueling more fire.' },
    ],
  },

  // ── Okanogan / NE highlands (dry pine & mixed conifer, fire-adapted) ──
  dryforest: {
    label: 'Eastern Dry Conifer Forest',
    blurb: 'Ponderosa pine & dry mixed-conifer. Historically shaped by frequent low-intensity fire; ' +
           'low fire is natural here, but modern high-severity megafires are destructive.',
    species: [
      { name: 'Mule Deer',               status: 'Stable',     impact: 'benefit', level: 'Recovers', note: 'Low-intensity fire opens understory and boosts new browse; benefits deer over time.' },
      { name: 'Rocky Mountain Elk',      status: 'Stable',     impact: 'benefit', level: 'Recovers', note: 'Burned meadows regrow lush forage; elk often favor recent low-severity burns.' },
      { name: 'Northern Spotted Owl',    status: 'Threatened', impact: 'harm',    level: 'Severe', note: 'Needs old dense canopy; high-severity fire destroys nesting habitat. Federally threatened.' },
      { name: 'Ponderosa Pine (habitat)',status: 'Habitat',    impact: 'benefit', level: 'Adapted', note: 'Thick bark survives low fire; fire actually maintains healthy open pine stands.' },
      { name: 'Black Bear',              status: 'Stable',     impact: 'mixed',   level: 'Moderate', note: 'Displaced short-term by large fires but uses berry-rich regrowth afterward.' },
      { name: 'Western Gray Squirrel',   status: 'Endangered', impact: 'harm',    level: 'High',   note: 'Oak/pine specialist with shrinking range; severe fire removes nesting trees. Endangered in WA.' },
    ],
  },

  // ── Cascades (moist high-elevation conifer forest) ──
  cascades: {
    label: 'Cascade Mountains Forest',
    blurb: 'Moist mountain conifer forest and alpine. Natural fires are infrequent but high-severity; ' +
           'recovery is slow at elevation, and large burns reshape habitat for decades.',
    species: [
      { name: 'Canada Lynx',             status: 'Endangered', impact: 'harm',    level: 'Severe', note: 'Needs dense forest and snowshoe-hare prey; large burns fragment habitat. State-endangered.' },
      { name: 'Wolverine',               status: 'Threatened', impact: 'mixed',   level: 'Moderate', note: 'Wide-ranging; fire affects denning forest but less directly than lowland species. Federally threatened.' },
      { name: 'Northern Spotted Owl',    status: 'Threatened', impact: 'harm',    level: 'Severe', note: 'Old-growth dependent; stand-replacing fire eliminates nesting habitat.' },
      { name: 'Rocky Mountain Elk',      status: 'Stable',     impact: 'benefit', level: 'Recovers', note: 'Benefits from meadow regrowth after fire opens the canopy.' },
      { name: 'Mountain Goat',           status: 'Stable',     impact: 'mixed',   level: 'Low',    note: 'High rocky terrain is less flammable; smoke and forage loss are the main concerns.' },
      { name: 'Old-growth Forest',       status: 'Habitat',    impact: 'harm',    level: 'Severe', note: 'Centuries-old trees are irreplaceable on human timescales once lost to severe fire.' },
    ],
  },

  // ── Westside wet forest (Puget lowlands, coast, Olympics) ──
  westside: {
    label: 'Westside Wet Forest & Lowlands',
    blurb: 'Wet temperate forest (Douglas-fir, hemlock, cedar). Fire is rare here, but when drought hits, ' +
           'fires can be intense and ecosystems are poorly adapted to recover quickly.',
    species: [
      { name: 'Roosevelt Elk',           status: 'Stable',     impact: 'mixed',   level: 'Moderate', note: 'Rare fires open foraging areas but large burns displace herds temporarily.' },
      { name: 'Northern Spotted Owl',    status: 'Threatened', impact: 'harm',    level: 'Severe', note: 'Old-growth specialist; any stand-replacing fire is a major threat.' },
      { name: 'Marbled Murrelet',        status: 'Threatened', impact: 'harm',    level: 'Severe', note: 'Seabird that nests only in old-growth conifers; fire loss of big trees is critical. Threatened.' },
      { name: 'Black-tailed Deer',       status: 'Stable',     impact: 'mixed',   level: 'Moderate', note: 'Can use regrowth but dense wet forest offers little post-fire forage short-term.' },
      { name: 'Pacific Salmon (streams)',status: 'Threatened', impact: 'harm',    level: 'High',   note: 'Several WA runs are listed; post-fire erosion and ash smother spawning gravels and warm streams.' },
      { name: 'Old-growth Forest',       status: 'Habitat',    impact: 'harm',    level: 'Severe', note: 'Rare and slow-growing; fire loss here is effectively permanent habitat destruction.' },
    ],
  },

  // ── SE Blue Mountains / Palouse (grassland & dry forest mix) ──
  bluemountains: {
    label: 'Blue Mountains & Palouse',
    blurb: 'Rolling grassland (Palouse) grading into dry forest. Native prairie is largely gone; ' +
           'remaining patches and dry forest face frequent fire pressure.',
    species: [
      { name: 'Rocky Mountain Elk',      status: 'Stable',     impact: 'benefit', level: 'Recovers', note: 'Favors post-fire forage in the Blue Mountains foothills.' },
      { name: 'Mule Deer',               status: 'Stable',     impact: 'mixed',   level: 'Moderate', note: 'Winter range browse reduced by large fires; recovers in a few seasons.' },
      { name: 'Bighorn Sheep',           status: 'Sensitive',  impact: 'benefit', level: 'Recovers', note: 'Open burned slopes improve sightlines and grazing; generally fire-tolerant.' },
      { name: 'Columbian Sharp-tailed Grouse', status: 'Threatened', impact: 'harm', level: 'High', note: 'Needs shrubby draws for winter cover; loss to fire is serious for this declining bird. State-threatened.' },
      { name: 'Palouse Prairie (habitat)', status: 'Habitat',  impact: 'harm',  level: 'High',   note: 'One of WA\'s rarest ecosystems; invasive grasses after fire crowd out native bunchgrass.' },
    ],
  },
};

// ── County → ecoregion mapping (all 39 WA counties) ──
const COUNTY_ECOREGION = {
  // Columbia Basin shrub-steppe
  ADAMS:'shrubsteppe', BENTON:'shrubsteppe', FRANKLIN:'shrubsteppe',
  GRANT:'shrubsteppe', LINCOLN:'shrubsteppe', DOUGLAS:'shrubsteppe',

  // Eastern dry conifer forest / highlands
  OKANOGAN:'dryforest', FERRY:'dryforest', STEVENS:'dryforest',
  'PEND OREILLE':'dryforest', SPOKANE:'dryforest', CHELAN:'dryforest',
  KITTITAS:'dryforest', YAKIMA:'dryforest', KLICKITAT:'dryforest',

  // Blue Mountains & Palouse (SE)
  WHITMAN:'bluemountains', GARFIELD:'bluemountains', COLUMBIA:'bluemountains',
  'WALLA WALLA':'bluemountains', ASOTIN:'bluemountains',

  // Cascade mountains forest
  SKAMANIA:'cascades', SNOHOMISH:'cascades', KING:'cascades',
  PIERCE:'cascades', WHATCOM:'cascades', SKAGIT:'cascades',

  // Westside wet forest & lowlands
  CLALLAM:'westside', JEFFERSON:'westside', MASON:'westside',
  'GRAYS HARBOR':'westside', PACIFIC:'westside', WAHKIAKUM:'westside',
  COWLITZ:'westside', LEWIS:'westside', THURSTON:'westside',
  CLARK:'westside', KITSAP:'westside', ISLAND:'westside', 'SAN JUAN':'westside',
};

function getCountyWildlife(countyName) {
  const key = COUNTY_ECOREGION[countyName];
  return key ? ECOREGIONS[key] : null;
}
