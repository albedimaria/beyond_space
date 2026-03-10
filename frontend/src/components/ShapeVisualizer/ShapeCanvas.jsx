import ShapeLines from "./ShapeLines";
import ShapeCircles from "./ShapeCircles";
import ShapeLabels from "./ShapeLabels";

function ShapeCanvas({ layout, files, percentages, onSvgClick, refPoint }) {
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
                    <ShapeLabels layout={layout} percentages={percentages} />
                </>
            )}

            {/* small center dot as a subtle origin */}
            <circle
                cx={250}
                cy={250}
                r={2}
                fill="white"
                stroke="none"
            />

            {refPoint && (
                <circle
                    cx={refPoint.x}
                    cy={refPoint.y}
                    r={5}
                    fill="none"
                    stroke="#ffffff"
                    strokeWidth="1.5"
                />
            )}
        </svg>
    );
}

export default ShapeCanvas;
