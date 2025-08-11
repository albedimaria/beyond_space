import { useState } from "react";
import { motion } from "framer-motion";
import FileUploader from "../components/FileUploader";
import ShapeVisualizer from "../components/ShapeVisualizer/ShapeVisualizer.jsx";
import SendPercentages from "../components/SendPercentages.jsx";
import ControlBar from "../components/ControlBar.jsx";
import Toolbox from "../components/Toolbox.jsx";


function Experience() {
    const [files, setFiles] = useState([]);
    const [mode, setMode] = useState("sum"); // "sum" | "inverse" | "gaussian"
    const [percentages, setPercentages] = useState([]);
    const [lastClick, setLastClick] = useState(null); // {x, y} in SVG coords

    // sliders state (default values)
    const [params, setParams] = useState({
        temperature: 1.00,
        randomness: 0.50,
        steps: 32,
    });

    return (
        <div style={{ textAlign: "center", marginTop: "40px" }}>
            <motion.h1
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
            >
                beyond space
            </motion.h1>

            <motion.div key={files.length} initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.5 }}>
                <ShapeVisualizer
                    files={files}
                    mode={mode}
                    onCompute={({ percentages, coords }) => {
                        setPercentages(percentages);
                        setLastClick(coords);
                    }}
                />
            </motion.div>

            <Toolbox params={params} onChange={setParams} />

            <ControlBar
                files={files}
                setFiles={setFiles}
                percentages={percentages}
                coords={lastClick}
                backendUrl="/api/percentages"
                mode={mode}
                setMode={setMode}
            />

        </div>
    );
}

export default Experience;
