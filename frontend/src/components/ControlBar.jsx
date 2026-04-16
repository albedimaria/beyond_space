// components/ControlBar.jsx
import FileUploader from "./FileUploader";
import SendPercentages from "./SendPercentages";
import ModeBar from "./ModeBar";

export default function ControlBar({
                                       files, setFiles,
                                       percentages, coords,
                                       mode, setMode,
                                       temperature, steps
                                   }) {
    return (
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
                    label="generate mix"
                />
            </div>
        </div>
    );
}