import { motion } from "framer-motion";
import { layouts, circleProps } from "./shapeLayout.js";

function ShapeVisualizer({ files }) {

    const num_files = files.length;
    const layout = layouts[num_files];

    return (
        <svg width="500" height="500" className="shape-board">
            {layout && (
                <>


                    {layout.lines.map(([startIdx, endIdx], i) => {
                        const { x: x1, y: y1 } = layout.points[startIdx];
                        const { x: x2, y: y2 } = layout.points[endIdx];

                        return (
                            <motion.line
                                key={`line-${i}`}
                                x1={x1}
                                y1={y1}
                                x2={x2}
                                y2={y2}
                                stroke="#a552a7"
                                strokeWidth="2"
                                initial={{ pathLength: 0 }}
                                animate={{ pathLength: 1 }}
                                transition={{ duration: 0.6, delay: i * 0.1 }}
                            />
                        );
                    })}

                    {layout.points.map(({ x, y }, i) => (
                        <motion.circle
                            key={`circle-${i}`}
                            cx={x}
                            cy={y}
                            {...circleProps}
                            initial={{ opacity: 0, scale: 0 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ duration: 0.5, delay: i * 0.05 }}
                        />
                    ))}

                </>
            )}
        </svg>
    );
}

export default ShapeVisualizer;
