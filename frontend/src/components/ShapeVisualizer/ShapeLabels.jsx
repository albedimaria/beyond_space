function ShapeLabels({ layout, percentages }) {
    if (percentages.length !== layout.points.length) return null;

    return layout.points.map(({ x, y }, i) => (
        <text
            key={`label-${i}`}
            x={x - 10}
            y={y + 26}
            fontSize="11"
            fill="#94a3b8"
            fontFamily="Inter, system-ui, sans-serif"
        >
            {percentages[i]}%
        </text>
    ));
}

export default ShapeLabels;
