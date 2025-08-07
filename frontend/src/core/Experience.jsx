import { useState } from "react";
import { motion } from "framer-motion";
import FileUploader from "../components/FileUploader";
import ShapeVisualizer from "../components/ShapeVisualizer/ShapeVisualizer.jsx";

function Experience() {
    const [files, setFiles] = useState([]);

    return (
        <div style={{ textAlign: "center", marginTop: "40px" }}>
            <motion.h1
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
            >
                Beyond Space Uploader
            </motion.h1>

            <motion.div
                key={files.length}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5 }}
            >
                <ShapeVisualizer files={files} />
            </motion.div>

            <FileUploader files={files} setFiles={setFiles} />

        </div>
    );
}

export default Experience;
