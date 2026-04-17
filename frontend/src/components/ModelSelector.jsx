// components/ModelSelector.jsx
const SUFFIX_RE = /_b2048_(?:s?r)48000_z\d+$/;

function displayName(model) {
    return model.replace(SUFFIX_RE, "");
}

export default function ModelSelector({ modelName, setModelName, modelList }) {
    return (
        <div className="mode-bar">
            <select
                id="model-select"
                value={modelName}
                onChange={(e) => setModelName(e.target.value)}
                aria-label="model"
            >
                {modelList.length === 0 ? (
                    <option value={modelName}>{displayName(modelName)}</option>
                ) : (
                    modelList.map((m) => (
                        <option key={m} value={m}>{displayName(m)}</option>
                    ))
                )}
            </select>
        </div>
    );
}
