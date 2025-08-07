import { motion } from "framer-motion";
import { circleProps } from "./shapeLayouts";

function ShapeCircles({ layout, files }) {
    return layout.points.map(({ x, y }, i) => (
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
    ));
}

export default ShapeCircles;
