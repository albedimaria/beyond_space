import { motion } from "framer-motion";
import { nodeOuter, nodeInner } from "./shapeLayouts";

function ShapeCircles({ layout, files }) {
    return layout.points.map(({ x, y }, i) => (
        <motion.g
            key={`node-${i}`}
            initial={{ opacity: 0, scale: 0 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: i * 0.05 }}
        >
            <title>{files[i]?.name}</title>
            <circle cx={x} cy={y} {...nodeOuter} />
            <circle cx={x} cy={y} {...nodeInner} />
        </motion.g>
    ));
}

export default ShapeCircles;
