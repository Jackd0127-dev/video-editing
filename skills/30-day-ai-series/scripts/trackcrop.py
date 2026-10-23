"""Keep the main person centred in a clip (third-party dance/walk clips shown inside a phone or card).

Usage: ffmpeg -i in.mp4 -vf fps=10 frames/f%04d.png && swift people.swift frames > boxes.txt
       python3 -I trackcrop.py boxes.txt in.mp4 out.mp4 ZOOM      (ZOOM 1.15-1.7; output keeps the input size)
Follows the largest person from the first frame, smooths over ~1.2 s, and crops with a fixed zoom.
Day 3 lesson: an untracked clip in a phone showed the dancer half out of frame ("I can barely see the character").
Assumes 720x1280 input at 10 fps samples; change W, H if yours differ.
"""
import subprocess, sys
txt, src, out, Z = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
W, H = 720, 1280
rows = []
for line in open(txt):
    p = line.split()[1:]
    rows.append([tuple(map(float, p[i:i + 4])) for i in range(0, len(p), 4)])
cur = max(rows[0], key=lambda b: b[3])
path = []
for boxes in rows:
    if boxes:
        c = (cur[0] + cur[2] / 2, cur[1] + cur[3] / 2)
        best = min(boxes, key=lambda b: abs(b[0] + b[2] / 2 - c[0]) + abs(b[1] + b[3] / 2 - c[1]) + 0.6 * abs(b[3] - cur[3]))
        if abs(best[0] + best[2] / 2 - c[0]) < 0.25:
            cur = best
    path.append((cur[0] + cur[2] / 2, cur[1] + cur[3] * 0.45))
k = 6  # smooth over ~1.2 s
sm = []
for i in range(len(path)):
    win = path[max(0, i - k):i + k + 1]
    sm.append((sum(p[0] for p in win) / len(win), sum(p[1] for p in win) / len(win)))
cw, ch = round(W / Z / 2) * 2, round(H / Z / 2) * 2
cmds = []
for i, (cx, cy) in enumerate(sm):
    x = min(max(cx * W - cw / 2, 0), W - cw)
    y = min(max(cy * H - ch / 2, 0), H - ch)
    cmds.append(f"{i / 10:.2f} crop x {x:.1f}, crop y {y:.1f};")
open(out + ".cmd", "w").write("\n".join(cmds))
x0 = cmds[0].split()[3].rstrip(",")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", f"sendcmd=f={out}.cmd,crop={cw}:{ch}:{x0}:0,scale={W}:{H}:flags=lanczos,setsar=1",
                "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart", out], check=True)
print(out, "zoom", Z, "x range", round(min(p[0] for p in sm), 2), round(max(p[0] for p in sm), 2))
