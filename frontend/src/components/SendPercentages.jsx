// components/SendPercentages.jsx
import { generateAudio } from "../api"; // keep if you use api.js
import Button from "./Button.jsx";

export default function SendPercentages({
                                            percentages,
                                            coords,
                                            files = [],
                                            mode,
                                            temperature,
                                            steps,
                                            label = "generate mix",
                                        }) {
    const handleSend = async () => {
        console.log("[SendPercentages] click");
        console.log("Tracks:", files.length, "Percentages:", percentages);

        try {
            await generateAudio({
                mode,
                temperature,
                steps,
                file1: files[0] || null,
                file2: files[1] || null,
                percentages,
                click: coords,
            });
            // nothing else — keep it minimal
        } catch (e) {
            // keep silent for now to avoid noise
            // console.log("request failed:", e);
        }
    };

    return (
        <div className="send-block">
            <Button onClick={handleSend}>{label}</Button>
        </div>
    );
}
