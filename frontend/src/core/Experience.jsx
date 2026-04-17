import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import ShapeVisualizer from "../components/ShapeVisualizer/ShapeVisualizer.jsx";
import ControlBar from "../components/ControlBar.jsx";
import Toolbox from "../components/Toolbox.jsx";
import ModelPanel from "../components/ModelPanel.jsx";
import { fetchModels } from "../api.js";


function Experience() {
    const [files, setFiles] = useState([]);
    // mode defines how distances on the board are mapped into mixing percentages ("sum" | "inverse" | "gaussian")
    const [mode, setMode] = useState("sum");
    // single source of truth for board percentages and last click position
    const [percentages, setPercentages] = useState([]);
    const [lastClick, setLastClick] = useState(null); // {x, y} in SVG coords

    // UI sliders: temperature maps to backend "noise", steps maps to backend "n_steps"
    const [params, setParams] = useState({
        temperature: 1.00,
        steps: 5,
    });

    const [modelName, setModelName] = useState("organ_archive_b2048_r48000_z16");
    const [modelList, setModelList] = useState([]);

    useEffect(() => {
        fetchModels()
            .then(setModelList)
            .catch(() => {}); // silent — ModelSelector falls back to default
    }, []);

    return (
        <div style={{ textAlign: "center", marginTop: "16px", position: "relative", zIndex: 1 }}>
            <div className="watermark" aria-hidden="true">beyond space</div>

            <motion.div
                key={files.length}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5 }}
            >
                <ShapeVisualizer
                    files={files}
                    mode={mode}
                    percentages={percentages}
                    coords={lastClick}
                    onCompute={({ percentages, coords }) => {
                        setPercentages(percentages);
                        setLastClick(coords);
                    }}
                />
            </motion.div>

            {(() => {
                let message = "";
                if (files.length === 0) {
                    message = "upload two audio files to start mixing";
                } else if (files.length === 1) {
                    message = "upload at least one more file — up to 4 total";
                } else if (!lastClick || !percentages?.length) {
                    message = "click inside the square to choose how to blend your tracks";
                } else {
                    message = "when you are happy with the point, press \"generate mix\"";
                }
                return (
                    <div
                        style={{
                            marginTop: "6px",
                            marginBottom: "2px",
                            fontSize: "0.9rem",
                            opacity: 0.85,
                        }}
                    >
                        {message}
                    </div>
                );
            })()}

            <Toolbox params={params} onChange={setParams} />
            <ModelPanel
                modelName={modelName}
                setModelName={setModelName}
                modelList={modelList}
            />

            <ControlBar
                files={files}
                setFiles={setFiles}
                percentages={percentages}
                coords={lastClick}
                mode={mode}
                setMode={setMode}
                temperature={params.temperature}
                steps={params.steps}
                modelName={modelName}
            />
        </div>
    );
}

export default Experience;
