// components/SendPercentages.jsx
import { useState } from "react";
import { generateAudio, API_BASE } from "../api";
import Button from "./Button.jsx";

export default function SendPercentages({
                                            percentages,
                                            coords,
                                            files = [],
                                            temperature,
                                            steps,
                                            modelName = "organ_archive_b2048_r48000_z16",
                                            label = "generate mix",
                                        }) {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [downloadUrl, setDownloadUrl] = useState(null);

    const hasFiles = files.length >= 2;

    const handleSend = async () => {
        if (!hasFiles || isLoading) return;

        console.log("[SendPercentages] click");
        console.log("Tracks:", files.length, "Percentages:", percentages);

        setIsLoading(true);
        setError(null);
        setDownloadUrl(null);

        try {
            const result = await generateAudio({
                files,
                weights: percentages,
                noise: temperature,
                n_steps: steps,
                model_name: modelName,
            });

            if (result && result.file) {
                setDownloadUrl(`${API_BASE}${result.file}`);
            }
        } catch (e) {
            console.error("request failed:", e);
            setError("Something went wrong while generating audio. Please try again.");
        } finally {
            setIsLoading(false);
        }
    };

    const isDisabled = !hasFiles || isLoading;

    return (
        <>
            <Button onClick={handleSend} disabled={isDisabled}>
                {label}
            </Button>
            <div className="send-status">
                {isLoading && (
                    <div className="send-progress-bar" />
                )}
                {!isLoading && error && (
                    <span className="send-status-label" style={{ color: "#ffb3b3" }}>
                        {error}
                    </span>
                )}
                {!isLoading && !error && downloadUrl && (
                    <a className="upload-btn send-download-link" href={downloadUrl} download>
                        download mix
                    </a>
                )}
            </div>
        </>
    );
}
