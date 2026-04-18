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
            <defs>
                <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1a1035" strokeWidth="1" />
                </pattern>
            </defs>
            <rect width="500" height="500" fill="url(#grid)" />

            {layout && (
                <>
                    <ShapeLines layout={layout} />
                    <ShapeCircles layout={layout} files={files} />
                    <ShapeLabels layout={layout} percentages={percentages} />
                </>
            )}

            {/* subtle origin dot */}
            <circle cx={250} cy={250} r={1.5} fill="#2d2756" stroke="none" />

            {refPoint && (
                <>
                    <circle
                        cx={refPoint.x}
                        cy={refPoint.y}
                        r={10}
                        fill="none"
                        stroke="#7c3aed"
                        strokeWidth="1"
                        opacity="0.35"
                        className="refpoint-pulse"
                    />
                    <circle
                        cx={refPoint.x}
                        cy={refPoint.y}
                        r={4}
                        fill="none"
                        stroke="#7c3aed"
                        strokeWidth="1"
                    />
                    <circle
                        cx={refPoint.x}
                        cy={refPoint.y}
                        r={1.5}
                        fill="#7c3aed"
                        stroke="none"
                    />
                </>
            )}
        </svg>
    );
}

export default ShapeCanvas;
