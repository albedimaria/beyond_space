// components/ControlBar.jsx
import FileUploader from "./FileUploader";
import SendPercentages from "./SendPercentages";
import ModeBar from "./ModeBar";

export default function ControlBar({
                                       files, setFiles,
                                       percentages, coords,
                                       backendUrl,
                                       mode, setMode,
                                       temperature, steps
                                   }) {
    return (
        <div className="control-bar">
            {/* Upload button */}
            <FileUploader files={files} setFiles={setFiles} />

            {/* Mode dropdown */}
            <ModeBar mode={mode} setMode={setMode} />

            {/* Send button */}
            <div>
                <button
                    type="button"
                    className="upload-btn"
                    onClick={() => {
                        // delegate to your existing SendPercentages, or inline fetch here if you prefer
                        // keeping SendPercentages for separation of concerns
                        // (We render it hidden and call its handler via ref if you want; simpler: just use it directly below)
                    }}
                    style={{ display: "none" }}
                />
                <SendPercentages
                    percentages={percentages}
                    coords={coords}
                    files={files}
                    backendUrl={backendUrl}       // e.g. "http://127.0.0.1:8000"
                    mode={mode}
                    noise={temperature}           // UI → backend name
                    n_steps={steps}               // UI → backend name
                    label="generate mix"
                />
            </div>
        </div>
    );
}