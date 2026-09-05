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

---

## 15. Lessons from the 2026-09-05 menu-and-price pass

This pass was not a verification pass. The task was "list signature dishes and drink
prices". It nonetheless produced **five hard scheduling errors** that two prior
verification passes had missed. That is the finding worth keeping.

### 15.1 Pricing work finds closures that verification work misses

To get a dish price you must open the operator's own menu page. Opening-hours text
sits on that same page. So a price scan reads the primary source for **every** venue,
whereas a hours-check tends to spot-check only venues that look suspicious.

Errors found this way, none of which the two earlier verification passes caught:
Spa Anise (closed Mon/Tue **and** shuts 17:00, scheduled for 17:00 Tue), Muse
(scheduled for Tuesday dinner; dinner is Wed–Sat), Dragon's Den (scheduled for
Sunday; closed Sun/Mon/Tue), Coffs Fishermen's Co-op (scheduled for 19:00; shuts
17:00), Moonshadow Splash & Slide (scheduled in September; runs Nov–Apr only).

**Rule:** run the price/menu scan **before** declaring the itinerary verified, and
treat it as the real opening-hours audit. It is cheaper and more complete than a
dedicated hours pass, because the price requirement forces primary-source contact.

### 15.2 Check the opening day of the venue you chose, not only the ones you rejected

§14.2 requires re-running the weekday check on date shift. It was run — and still
missed Muse, because the reasoning had been written as:

> "Muse is right for Tuesday **because** EXP. and Hunters Quarter don't do Tuesday
> dinner — operating-day beats rating."

Both premises were verified. The conclusion was never checked: **Muse does not do
Tuesday dinner either.** The "operating-day beats rating" trade-off is sound; the
failure was auditing the losers of the comparison and exempting the winner.

**Rule:** whenever a stop is justified by a rival's closure, that justification makes
the chosen venue's own opening day **more** load-bearing, not less. Verify the winner
first, and record the source (operator page, not aggregator) next to it.

### 15.3 A subagent's opening hours are a claim, not a fact

The replacement for Spa Anise was Ubika, chosen partly because the research agent
reported "Fri/Sat 9:00–20:00" — the only Hunter spa that could serve an evening slot.
Cross-checking the operator's own site found **Mon–Sat 9:00–17:00, Sun 10:00–16:00**,
confirmed independently by Google Maps. The agent's figure came from the host resort's
page, which was stale.

Had it not been re-checked, a 15:40 booking would have been placed against a 17:00
close — replacing one closure error with an identical new one, inside the very fix
meant to remove it.

**Rule:** any hours figure that **decides** a scheduling choice must be confirmed
against the operator's own page before it lands in the plan. Delegated research is
for breadth; the load-bearing number gets verified by hand.

### 15.4 Report the rating you found, even when it undermines your own recommendation

The same agent reported "Ubika: no aggregate rating found". Live Google Maps shows
**4.3 / 105** — below both gates. Spa Anise, the venue being replaced, shows **4.6 /
10**. Neither clears the screen; the original page had ranked Spa Anise as the
region's best on no data at all.

The honest output is not to quietly promote the 4.3, nor to hide it behind "operating
day beats rating". It is to state that **Tuesday has no qualifying spa in the Hunter**,
name the 4.3 as the price of going anyway, and offer dropping the stop as a real
option.

**Rule:** "not found" from a research agent is a prompt to look yourself, not a
licence to treat the venue as unrated. A gap in the data is not neutral — it usually
hides the number that would have changed the recommendation.

### 15.5 Closure has more than two states

Karrikin was reported to us as "closed down", and live Google Maps says
**permanently closed**. The operator's own site says they are **travelling and return
March 2027**, and that friends are running the same room as **Lela's** meanwhile.

For the 17 Sep booking all three framings give the same answer — you cannot eat there.
They give different *navigation* answers: "permanently closed" implies an empty
shopfront, when in fact the address is a working restaurant under another name.

**Rule:** record closure as {permanent, hiatus-with-return-date, replaced-in-place,
relocated}, sourced from the operator where possible (extends §14.6). The distinction
changes what the traveller finds when they arrive.

### 15.6 Corrections must reach the summary tables too

§14.7 says corrections must land in the day entry, not just a banner. This pass found
the same failure one level down: after fixing the day cards, the **footer summary
tables still carried the retracted figures** (The Cottage 4.7/735, BeachWood 4.6/548
mislabelled as Google, Royal Hotel's unverifiable 4.6/235) and still recommended
Dragon's Den and Muse on days they are shut.

**Rule:** a correction is complete when a text search for the retracted string returns
only occurrences inside an explicit "this was wrong" sentence. Grep before shipping.

---

## 16. Lessons from the 2026-09-05 route-shape rewrite

The plan went 9 days → 8 → 7, and inland → coastal → true loop, driven entirely by user
pushback. Four rules came out of it.

### 16.1 Repetition is a property of the route's shape, not of its stops

The user said "D5/D6/D7 feel repetitive — lighthouses, coastal views." Counting: Yamba
Lighthouse, Tacking Point, Bennetts Head, Sugarloaf Point, Smoky Cape, Pat Morton,
Fingal Head. **Seven days, six lighthouses/headlands.** §6 already forbade repeating an
experience type, and it had been applied stop-by-stop — each one individually cleared
the rating screen and each was "the best thing in its town."

The cause was structural: the itinerary ran **down a coastal corridor and back up the
same corridor**. On that shape, every overnight town is a coastal town, so every town's
best free attraction is a headland. No amount of per-stop screening fixes that.

**Rule:** when the same category keeps recurring, stop swapping individual stops and
look at the route's topology. An out-and-back on one corridor will always repeat; a
loop that returns on a different corridor will not. Fix the shape, and the duplicate
stops disappear on their own.

### 16.2 Two "best walks" can be duplicates of each other

Tomaree Head (Google 4.9/1,512, Grade 5, 400 steps) and Girraween's The Pyramid
(AllTrails 4.8/1,118, Grade 4, bare granite) were being weighed as if independent. They
are the same experience: climb hard, get a big view. Keeping both while cutting days is
incoherent.

Recognising that turned an apparent loss into a trade: dropping Nelson Bay removed a
duplicate **and** two days **and** two lighthouses, and made room for the Pyramid, which
sits on the way home from the north. **Geography decided it** — Nelson Bay to Girraween
is 7h+, so the two were mutually exclusive regardless of preference.

**Rule:** before defending a stop on its rating, ask what category it occupies and
whether another stop already fills it. When two candidates are the same category,
let the route geometry pick the winner, not the score.

### 16.3 Cutting days changes which weekday every later stop falls on

Each length change (9→8→7) re-dated every stop after the cut. That silently invalidated
the opening-hours work already done, and each pass surfaced new closures:
Port Macquarie's two best restaurants are closed Sun–Mon (D4 became Sunday);
Varias is Tue–Sat (D5 became Monday); Glen Innes' only good lunch closes at 14:00
against a 12:45–13:15 arrival; Harbour Town's late night is Thursday only.

**Rule:** treat a change in trip length as a full invalidation of every weekday-dependent
fact downstream of it, exactly as §14.2 treats a date shift. Re-run the opening-day
check as a batch after every re-length — never patch it stop by stop.

### 16.4 A cheap waypoint can rescue a long transfer day

The unavoidable 5h38 transfer (Port Macquarie → Girraween) was made tolerable by two
stops that cost almost nothing: **Glen Innes' Standing Stones added 5 minutes** to the
route (it is directly on the Gwydir Highway) and **Raspberry Lookout added ~0** (sealed
spur off the same highway). Measured, not assumed — the naive assumption was that both
were detours.

**Rule:** on any transfer leg over ~4 hours, re-measure the route *with candidate
waypoints inserted* rather than measuring the detour separately. Waypoints that lie on
the corridor often cost single-digit minutes, and they are the difference between a
transfer day and a touring day.
