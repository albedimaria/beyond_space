// components/ControlBar.jsx
import FileUploader from "./FileUploader";
import SendPercentages from "./SendPercentages";
import ModeBar from "./ModeBar";

export default function ControlBar({
                                       files, setFiles,
                                       percentages, coords,
                                       mode, setMode,
                                       temperature, steps,
                                       modelName,
                                   }) {
    return (
        <div className="control-bar-outer">
            <div className="control-bar">
                <FileUploader files={files} setFiles={setFiles} />
                <ModeBar mode={mode} setMode={setMode} />
                <div>
                    <SendPercentages
                        percentages={percentages}
                        coords={coords}
                        files={files}
                        temperature={temperature}
                        steps={steps}
                        modelName={modelName}
                        label="generate mix"
                    />
                </div>
            </div>
        </div>
    );
}