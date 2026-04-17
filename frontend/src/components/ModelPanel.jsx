// components/ModelPanel.jsx
// Mirrors Toolbox — fixed to the right edge, slides in on hover/focus.

const SUFFIX_RE = /_b2048_(?:s?r)48000_z\d+$/;

function displayName(model) {
    return model.replace(SUFFIX_RE, "");
}

export default function ModelPanel({ modelName, setModelName, modelList }) {
    return (
        <aside className="toolbox model-panel" aria-label="model selector">
            <div className="toolbox-panel">
                <div className="toolbox-row">
                    <label>model</label>
                    <span className="toolbox-output">{displayName(modelName)}</span>
                </div>
                <ul className="toolbox-model-list">
                    {modelList.map((m) => (
                        <li
                            key={m}
                            className={m === modelName ? "active" : ""}
                            onClick={() => setModelName(m)}
                        >
                            {displayName(m)}
                        </li>
                    ))}
                </ul>
            </div>
            <div className="toolbox-handle" tabIndex={0} title="Select model" />
        </aside>
    );
}
