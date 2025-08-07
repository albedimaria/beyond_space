/**
 * Calculates integer percentages for points based on distance from a click.
 * Supports "sum", "inverse", and "gaussian" weighting modes, always summing to 100%.
 */


export function calculatePercentages(click, points, opts = {}) {
    const {
        mode = "sum",      // "sum" = current behavior (farther => higher %)
        sigma = 120,       // used in "gaussian" mode
        epsilon = 1e-6     // prevents division by zero
    } = opts;

    const distances = points.map(p => Math.hypot(p.x - click.x, p.y - click.y));

    let weights;
    if (mode === "inverse") {
        // favor closer points: 1 / d
        weights = distances.map(d => 1 / (d + epsilon));
    } else if (mode === "gaussian") {
        // favor closer points: exp(-(d^2)/(2*sigma^2))
        const denom = 2 * sigma * sigma;
        weights = distances.map(d => Math.exp(-(d * d) / denom));
    } else {
        // "sum": same as current version, no bound, just normalization by the sum
        weights = distances;
    }

    const total = weights.reduce((s, w) => s + w, 0);

    // Fallback: if total ~ 0 (click exactly on a point and mode is inverse/gaussian),
    // distribute evenly.
    if (!isFinite(total) || total <= epsilon) {
        const eq = Math.round(100 / Math.max(points.length, 1));
        const last = 100 - eq * (points.length - 1);
        return points.map((_, i) => (i === points.length - 1 ? last : eq));
    }

    // Normalize to percentages summing to 100 (rounded)
    const raw = weights.map(w => (w / total) * 100);

    // correction for rounding errors
    const rounded = raw.map(x => Math.floor(x));
    let diff = 100 - rounded.reduce((a, b) => a + b, 0);

    // distribute remaining points to values with highest fractional part
    const frac = raw.map((x, i) => ({ i, f: x - Math.floor(x) }))
        .sort((a, b) => b.f - a.f);
    for (let k = 0; k < diff; k++) rounded[frac[k].i] += 1;

    return rounded;
}
