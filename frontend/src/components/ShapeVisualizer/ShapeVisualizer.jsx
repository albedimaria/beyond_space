import ShapeCanvas from "./ShapeCanvas";
import { layouts } from "./shapeLayouts";
import { calculatePercentages } from "../../utils/calculatePercentages.js";

function ShapeVisualizer({ files, mode, percentages, coords, onCompute }) {
    const count = files.length;
    const layout = layouts[count];

    const handleClick = (clickPoint) => {
        if (!layout) return;
        const perc = calculatePercentages(clickPoint, layout.points, { mode });
        if (perc && onCompute) {
            onCompute({ percentages: perc, coords: clickPoint });
        } else if (onCompute) {
            onCompute({ percentages: [], coords: null });
        }
    };

    return (
        <ShapeCanvas
            layout={layout}
            files={files}
            percentages={percentages}
            onSvgClick={handleClick}
            refPoint={coords}
        />
    );
}

export default ShapeVisualizer;

