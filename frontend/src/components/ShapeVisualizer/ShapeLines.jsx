import { motion } from "framer-motion";

function ShapeLines({ layout }) {
    return layout.lines.map(([startIdx, endIdx], i) => {
        const { x: x1, y: y1 } = layout.points[startIdx];
        const { x: x2, y: y2 } = layout.points[endIdx];
        return (
            <motion.line
                key={`line-${i}`}
                x1={x1}
                y1={y1}
                x2={x2}
                y2={y2}
                stroke="#4e79a7"
                strokeWidth="2"
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ duration: 0.6, delay: i * 0.1 }}
            />
        );
    });
}

export default ShapeLines;
