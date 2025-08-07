import ShapeLines from "./ShapeLines";
import ShapeCircles from "./ShapeCircles";
import ShapeLabels from "./ShapeLabels";

function ShapeCanvas({ layout, files, percentuali, onSvgClick }) {
    const handleSvgClick = (e) => {
        if (!layout) return;
        const rect = e.currentTarget.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const clickY = e.clientY - rect.top;
        onSvgClick({ x: clickX, y: clickY });
    };

    return (
        <svg
            width="500"
            height="500"
            className="shape-board"
            onClick={handleSvgClick}
            style={{ cursor: "crosshair" }}
        >
            {layout && (
                <>
                    <ShapeLines layout={layout} />
                    <ShapeCircles layout={layout} files={files} />
                    <ShapeLabels layout={layout} percentuali={percentuali} />
                </>
            )}
        </svg>
    );
}

export default ShapeCanvas;
