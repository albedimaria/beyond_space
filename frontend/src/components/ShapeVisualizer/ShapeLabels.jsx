function ShapeLabels({ layout, percentuali }) {
    if (percentuali.length !== layout.points.length) return null;

    return layout.points.map(({ x, y }, i) => (
        <text
            key={`label-${i}`}
            x={x + 24}
            y={y - 10}
            fontSize="14"
            fill="#333"
        >
            {percentuali[i]}%
        </text>
    ));
}

export default ShapeLabels;
