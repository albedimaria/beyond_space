// components/ControlBar.jsx
import FileUploader from "./FileUploader";
import SendPercentages from "./SendPercentages";
import ModeBar from "./ModeBar";
import ModelSelector from "./ModelSelector";

export default function ControlBar({
                                       files, setFiles,
                                       percentages, coords,
                                       mode, setMode,
                                       temperature, steps,
                                       modelName, setModelName, modelList,
                                   }) {
    return (
        <div className="control-bar-outer">
            <div className="control-bar">
                <FileUploader files={files} setFiles={setFiles} />
                <ModeBar mode={mode} setMode={setMode} />
                <ModelSelector
                    modelName={modelName}
                    setModelName={setModelName}
                    modelList={modelList}
                />
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