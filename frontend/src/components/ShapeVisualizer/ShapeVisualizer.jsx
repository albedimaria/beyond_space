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
        const perc = calculatePercentages(clickPoint, layout.points, {mode: "sum"});
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
            percentages={percentuali}
            onSvgClick={handleClick}
        />
    );
}

export default ShapeVisualizer;


