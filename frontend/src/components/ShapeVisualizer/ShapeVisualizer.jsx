import ShapeCanvas from "./ShapeCanvas";
import { layouts } from "./shapeLayouts";
import { useState } from "react";
import {calculatePercentages} from "../../utils/calculatePercentages.js";

function ShapeVisualizer({ files }) {
    const count = files.length;
    const layout = layouts[count];

    const [refPoint, setRefPoint] = useState(null);
    const [percentuali, setPercentuali] = useState([]);

    const handleClick = (clickPoint) => {
        const perc = calculatePercentages(clickPoint, layout.points, {mode: "inverse"});
        if (perc) {
            setRefPoint(clickPoint);
            setPercentuali(perc);
        } else {
            setRefPoint(null);
            setPercentuali([]);
        }
    };

    return (
        <ShapeCanvas
            layout={layout}
            files={files}
            percentuali={percentuali}
            onSvgClick={handleClick}
        />
    );
}

export default ShapeVisualizer;



/*
import { motion } from "framer-motion";
import { layouts, circleProps } from "./shapeLayouts.js";

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
                        >
                            <title>{files[i]?.name}</title>
                        </motion.circle>
                    ))}

                </>
            )}
        </svg>
    );
}

export default ShapeVisualizer;
*/
