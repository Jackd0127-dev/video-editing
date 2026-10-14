// Original dependency-free poses distilled from the approved editorial edit.
// Time inputs are seconds; the host owns rendering, fonts, clips and masks.
export const clamp01 = value => Math.max(0, Math.min(1, value));
export const mix = (a, b, p) => a + (b - a) * p;
export const smoothstep = value => {
  const u = clamp01(value);
  return u * u * (3 - 2 * u);
};
export const smootherstep = value => {
  const u = clamp01(value);
  return u * u * u * (u * (u * 6 - 15) + 10);
};
export const easeOutQuart = value => 1 - (1 - clamp01(value)) ** 4;

export function progress(time, onset, duration, curve = smootherstep) {
  if (!Number.isFinite(duration) || duration <= 0) {
    throw new RangeError('Duration must be positive and finite');
  }
  return curve((time - onset) / duration);
}

export function wordReveal(time, onset, {duration = 0.58, mode = 'rise', travelPx = 15} = {}) {
  if (mode !== 'rise' && mode !== 'wipe') throw new RangeError('Unknown reveal mode');
  const p = progress(time, onset, duration);
  return {
    visible: time >= onset,
    progress: p,
    translateYPct: mode === 'rise' ? 112 * (1 - p) : 0,
    translateXPx: mode === 'wipe' ? -travelPx * (1 - p) : 0,
    clipRightPct: mode === 'wipe' ? 100 * (1 - p) : 0,
  };
}

export function phraseSlot(time, onset, height, duration = 0.62) {
  const p = progress(time, onset, duration);
  return {previousY: -height * p, nextY: height * (1 - p)};
}

export function rectangleTransition(time, onset, from, to, duration = 0.62) {
  if (from.length !== 5 || to.length !== 5) throw new RangeError('Use [x,y,width,height,radius]');
  const p = progress(time, onset, duration, smoothstep);
  return from.map((value, index) => mix(value, to[index], p));
}

export function orbitPose(time, index, count, {
  cx = 0.5, cy = 0.615, rx = 0.398, ry = 0.211,
  speed = -0.84, phase = -Math.PI / 2, baseScale = 0.84, depthScale = 0.07, tilt = 6,
} = {}) {
  if (!Number.isInteger(count) || count < 1) throw new RangeError('Count must be a positive integer');
  const angle = phase + index * 2 * Math.PI / count + time * speed;
  const depth = Math.sin(angle);
  return {x: cx + rx * Math.cos(angle), y: cy + ry * Math.sin(angle), depth,
    scale: baseScale + depthScale * depth, rotationDegrees: tilt * Math.cos(angle)};
}
