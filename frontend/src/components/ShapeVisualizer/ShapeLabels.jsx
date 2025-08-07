function ShapeLabels({ layout, percentuali }) {
    if (percentuali.length !== layout.points.length) return null;

    return layout.points.map(({ x, y }, i) => (
        <text
            key={`label-${i}`}
            x={x - 10}
            y={y + 38}
            fontSize="14"
            fill="white"
        >
            {percentuali[i]}%
        </text>
    ));
}

export default ShapeLabels;
