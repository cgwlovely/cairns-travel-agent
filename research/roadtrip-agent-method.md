# Road-trip Agent Method

This file captures the reusable decision logic developed from the NSW 17–25 Sep 2026 road trip. The goal is to make the planner behave like an optimisation agent rather than a town-by-town checklist generator.

## 1. Start from experience quality, not a fixed itinerary

Scan both plausible route corridors independently before choosing direction. Candidate types:

- natural attractions / lookouts / parks / beaches / waterfalls;
- restaurants / cafes / wineries;
- spa / sauna / massage;
- paid activities such as kayak, SUP, wildlife cruise, whale watching and tours;
- accommodation when the property itself adds meaningful experience value.

Do not assume existing overnight towns deserve to remain.

## 2. Rating + review-volume screen

Use ratings as a screening signal, not truth.

- Destination anchor: prefer ~4.8–4.9+ with roughly 200+ reviews.
- Also retain 4.6–4.7 when review volume is unusually large (~1,000+).
- 4.8+ with <100 reviews can support a meal/spa/backup but should rarely create a new overnight stop.
- A 4.6 with 2,000 reviews may be more reliable than a 4.9 with 25 reviews.

Mental score:

`quality + review confidence + uniqueness + route fit - detour cost`

## 3. Distinguish anchors from supporting stops

An anchor can justify a dedicated half-day, detour or overnight cluster.

A supporting stop improves an existing day but should not create a new day by itself.

Examples:
- anchor: Dorrigo rainforest cluster, Tomaree, The Pyramid;
- support: high-rated cafe, spa backup, 20-minute lookout.

## 4. Apply detour penalty

- ≤15 min: very low penalty;
- 15–45 min: acceptable for strong A/S-tier stop;
- 45–90 min: normally requires an S-tier anchor or strong cluster;
- >90 min: only when it materially changes trip quality.

## 5. Cluster strong points

Prefer one coherent cluster to multiple weak isolated stops.

Example:

`Components Cafe + Dorrigo Rainforest Centre + Skywalk + nearby falls`

This is stronger than four mediocre stops spread over a day.

## 6. Remove duplicated experiences

Do not repeat the same paid activity or scenery type just because each item scores well.

For NSW 2026:
- Sawtell kayak beats weaker Forster kayak options;
- The Pyramid and Bald Rock are both granite-dome experiences, so Bald Rock was removed after duplication review.

## 7. Restaurant agent rule

Never write only “eat nearby”. For each planned meal:

1. scan the exact arrival area;
2. prefer 4.6+ with meaningful review volume;
3. in small towns, compare high-rating small samples against 4.4–4.6 large samples;
4. verify opening day/hours for the actual weekday;
5. record exact name, address, price range and fallback;
6. reject a famous restaurant if it is closed on that itinerary day.

The NSW scan caught a real scheduling error this way: Little Beach Boathouse was assigned to Monday even though it is closed, so Monday dinner moved to Sirena Seaside.

## 8. Accommodation hard gate

Accommodation is not optimised on rating/price until it passes basic privacy requirements.

Hard filters:

1. private room for two adults;
2. private bathroom / ensuite preferred and must be verified at room level before payment;
3. exclude hostel / YHA / backpacker / dormitory;
4. exclude shared-bathroom rooms;
5. self-drive trips: free or on-site parking strongly preferred;
6. if no qualifying inventory exists in the planned town, expand to nearby towns/cities within roughly 20–40 minutes instead of lowering the standard;
7. property type returned by a booking engine does not replace exact room-level bathroom verification.

This rule overrides low price. A cheap room with shared facilities is not a valid recommendation for this user profile.

## 9. Choose overnight towns after the activity graph

An overnight node should do at least one of:

- hold an A/S-tier cluster;
- break a long drive below the continuous-driving ceiling;
- materially improve accommodation quality/price for the next anchor.

A town can be a functional overnight without being a sightseeing destination.

## 10. Let trip length shrink

Do not begin with “make this 10 days”.

Instead:

1. count genuine anchor-days;
2. add necessary transfer/recovery days;
3. remove any day justified mainly by weak or duplicated activities.

## 11. Driving rule

Default target: ≤3h continuous driving. About 3.5h is the planning ceiling before a meaningful stop.

Long total-driving days may still be acceptable if deliberately split into 1–2h legs with proper food/rest stops.

## 12. Booking order

Use this sequence:

`quality scan → route graph → duplication check → exact weekday opening check → overnight nodes → accommodation hard gate → live prices → hour-by-hour itinerary`

Do not let a cheap hotel create a destination that otherwise has no worthwhile experience.

## 13. Volatile data revalidation

Recheck 48–72h before departure:

- national-park/road access;
- weather-sensitive hikes;
- marine weather and cruise status;
- kayak/spa/tour availability;
- restaurant opening changes;
- exact room type, private bathroom and cancellation terms;
- final live hotel prices.

Stable route logic and volatile booking data should remain separate in the agent's reasoning.

---

## 14. Lessons from the 2026-09-05 independent verification pass

Added after an independent re-scan of the 17–25 Sep plan (eight route segments, Google ≥4.7 & ≥200 screen, live Booking re-check on the true dates). Each item below is a rule the original method *had* but did not survive contact with the data, or a rule it was missing.

### 14.1 The §7 worked example violates §2 — fix it

§7 cites "Monday dinner moved to Sirena Seaside" as a success. Sirena has **OpenTable 4.5 / 37 reviews**, which fails the §2 screen (~200+ reviews) by two orders of magnitude. The correct Monday answer on that segment is **Atmos** (Shoal Bay Country Club): **Google 4.7 / 2,034**, verified open Mon–Thu 17:00–23:00.

**Rule:** catching a closure is only half the job. The replacement must clear the same screen the original had to clear — otherwise a hard failure (closed) has been traded for a soft one (unverified).

### 14.2 Re-run the weekday check whenever dates move

§7 step 4 already requires verifying opening hours for the actual weekday, but Stonefruit was still scheduled for a **Wednesday** while the same paragraph noted "Thu–Sat only". Official hours: **Wednesday Closed**.

**Rule:** the weekday-opening check is invalidated by any date shift, and must be re-run as a batch — not spot-checked. Treat "the page already says the right hours somewhere" as *not* checked.

### 14.3 Never mix rating platforms inside one screen

Four "top picks" in the plan were selected on TripAdvisor scores while their Google scores were below the stated gate (Cafe TREEO TA 4.6 vs Split Cafe Google 4.7/606; Spice Monkey TA 4.5 vs Dragon's Den Google 4.8/491; Muse TA 4.7 vs Google 4.6/763; Stonefruit TA 4.8/23 vs Google 4.8/257).

**Rule:** pick one platform as the gate, record every other platform separately, and never let a score from platform B satisfy a threshold defined on platform A. Where platforms disagree sharply (Atmos: Google 4.7/2,034 vs TA 4.0/103), report both — the disagreement is information, not noise.

### 14.4 Regional rating ceiling: a hard 4.7 gate empties whole segments

Across Woolgoolga, Bellingen, Yamba, Harrington, Old Bar and Taree, the best restaurants cap at **Google 4.6**. Applying a hard 4.7 gate returns an empty set and pushes the planner toward tiny-sample 4.8s — exactly the failure in 14.1.

**Rule:** below a certain town size, switch from "threshold" to "local best + explicit label". State plainly that no venue in the town clears the gate rather than promoting an unqualified one. Same finding for spa: across the whole route only one spa clears the gate (Figtree Dayspa, Google 4.9/258).

### 14.5 Inventory scarcity is a gate, not a price line

§8 gates accommodation on privacy and §12 puts live prices last. But on the true dates **Yamba 17 Sep was 95% sold out** (best compliant room: 1 left) and **Bellingen 18 Sep was 89% sold out with zero compliant inventory** — the plan's own hard filter had no legal move in that town.

**Rule:** run the availability scan on the **exact dates** at graph time, not at booking time. Scarcity changes the route (Bellingen → Coffs), and a route decision made after the rooms are gone is not a decision. Also: re-scan whenever the trip dates shift — prices and availability from a different date set are not evidence.

### 14.6 Verify the venue is still where the plan says it is

The Koala Hospital plan pointed at the visitor operation that ran during the rebuild (Guulabaa, +40 min round trip) while the **Lord Street site reopened 2026-09-07**. Similar live-status finds: Dorrigo Skywalk open but inside a demolition countdown (Arc project) with the Lyrebird Link ramp closed to 2028; Yamba Kayak's "temporarily closed" flag stale (it is operating).

**Rule:** for any venue that has recently moved, rebuilt or been flagged closed, confirm the **current address and status from the operator**, not from an aggregator snapshot. Aggregator status flags lag reality in both directions.

### 14.7 Where corrections must land

A correction banner at the top of a page does not protect a reader who navigates to the day card and follows it. Fixes must be written **into the day entry itself**, with the original struck through and the reason attached, so the plan is safe to follow linearly.
