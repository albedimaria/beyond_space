
export function calculatePercentages(click, points, maxDistance = 1000) {
    const distances = points.map(p =>
        Math.hypot(p.x - click.x, p.y - click.y)
    );

    const total = distances.reduce((sum, d) => sum + d, 0);

    if (total === 0 || total > maxDistance) {
        return null; // click not valid
    }

    return distances.map(d => Math.round((d / total) * 100));
}