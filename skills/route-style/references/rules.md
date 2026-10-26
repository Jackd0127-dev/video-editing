# Route rules

## Route-specific
- **One route per video.** Its stations are the steps he names, in his order. The same map (same geometry) comes back every time; never redraw a different layout mid-video.
- **The hook draws the plan.** On his "here's exactly what I'd do" line the grey track runs up the screen and each station lands as the line reaches it (causal). The lime fill is not shown yet: the lime is progress.
- **Progress is earned.** The lime train only moves when he names the next step; stations light when the train arrives (lime ring, burst ring, pluck). Never fill ahead of the train.
- **The HUD mirrors the map** over his footage (top band, above the shelf, y≈118–214). It appears after the hook and moves (with a small pulse + pluck) when he names a step. If he names it while a page covers him, the HUD moves just after the page leaves so the viewer sees it.
- **The payoff is the last station.** On his payoff word the train arrives, the station label flips to his word ("BUILDING"), big ring burst + confirmation sound. The first station's label can flip to his "before" word ("CHATTING") on the same page.
- **Rhythm:** at most ~6 s of pages in a row; at least 1 s of his face between pages, or they hand off by dissolving. Steps he says on camera get the HUD, not another page.
- **No invented copy.** Page titles use his words ("£5,000 course", "follow for more"). Illustrative card contents (example ideas, sample notifications) are fine; slogans he never said are not ("follow the route" was replaced).
- **Selectors are page-scoped.** Never tween a shared class (`.phone`): one page's exit swept another page's phone off screen. Give every animated element an id.

## Shared hard rules (from Jack's notes; full list in `skills/30-day-ai-series/references/rules.md`)
- Hook opens on his face with a quick zoom (1.35 → 1 in 0.5 s); never open on a page.
- Never grade, filter, crop, letterbox or cut him out; HLG → SDR with `sdr.sh`, render `--sdr`.
- Captions never cover his face (bottom edge y = 590, above his hair); hook captions are exactly what he says.
- Causal animation; connections happen once; real cursor clicks that land exactly on the button (measure it).
- Real logos for named products; real assets over mock-ups.
- Crossfade (0.42 s) back to his face; pages hand to pages by dissolving; never flash a new take before a page.
- No clipped words; no doubled sounds at joins; no music unless he asks; no red.
- Every video ships as 2 versions (`tools/TRIAL-REELS.md`).
