# Arena rules

## What makes it Arena
- **Characters, never icons.** Any "1 agent" or "100 agents" is animated pixel agents, not logos, dots or counters. A crowd mixes personalities (different props and eyes) so it never reads as one clone.
- **They do the thing he says.** On "battle" they fight. On "bracket" they drop into slots. On "knock out" the loser flinches, gets KO eyes and poofs. Show it; don't label it.
- **The field thins through the agents.** No big "100 LEFT / 8 LEFT / ×10" text pages (Jack: "terrible"). At most one small count chip.
- **"1 left" is the crown moment.** The winner walks over, the crown lifts onto its head, it jumps with pixel sparkles and holds.
- **VS is agent vs agent** with weapons or props (sword vs gun, wizard vs chef) and a short fight ending in a knockout.
- **Scale is a camera move.** 1,000 or a million is a zoom-out from a handful of animated agents over a tiled field until it's an ocean, with the count running. Never just a big number.
- **The hero word gets a sheet.** The named thing ("Arena") is one strong page with the bracket full of agents and the crown waiting in the middle.

## Jack's notes on this style (29 Oct 2026)
- Pages must arrive smoothly: fades and eased, staggered motion. A prompt that splits into 100 agents is one continuous move, with no jump-cut page swaps or pop-ins.
- The prompt moment is real: type into the real Claude box character by character, then `/arena` types after the task, lights up coral with a halo pulse, and an agent reacts.
- Don't dwell on the problem. A struck-out "try again ×3" graphic was rejected; one agent getting a bad answer and getting fed up replaced it.
- Audit every screen before showing him. Any page that's only type and a number needs characters doing something.

## Page budget
The reference V1 is the richest version of this look, at about 58 % pages. Since then Jack's standing rule is **the video is mostly him with captions**, so a new Arena edit starts from these limits:
- His face and captions are on screen for more than half of the video.
- A page shows one thing for a few seconds, usually ≤4 s. Longer only while something is visibly happening (the battle, the zoom-out).
- If a beat can run as a chest-band overlay (`ov_*`), it does. Pages are for the hero word, the battle, the crown, the scale and the result.

## Sound
- **No sound effects on fights, slashes, shots, hits, knockouts or clashes.** Action stays silent unless he asks for sound.
- **Never the same effect again and again.** The generator's assembly step keeps one effect per family every 3 s; don't work around it.
- Delivered renders of the reference video predate this rule and still have fight sounds. The generator here does not.
- No music unless he asks for it on that video (real, smooth, licensed track, very low: about 20 dB under his voice). Never a synthesized bed.

## Shared hard rules
- Footage untouched: Apple HDR→SDR, no grade, no filter, no fake background.
- Hook opens on his face with a quick zoom slam on V1. V2's cold open is the only exception.
- Captions never cover his face and stay out of the top 22 % of the frame. Hook captions match what he says.
- Never clip a word; cut every stutter and gap; no doubled words at joins.
- Something changes every ~1–1.5 s; no layout holds over ~2.5 s without motion.
- Animations are causal: something happens because something reached it.
- Any Claude UI is a real capture. The Claude logo keeps its real colour and shape. The pixel agents are characters, not a redrawn logo.
- Page → face crossfades; page → page dissolves; no face flash under 1 s between pages.
- Made-up agent numbers and records are illustrative: don't present them as real results.
- One edit by default (a second only when he asks), −14 LUFS, delivered to the video's `Exports/` with a caption.
