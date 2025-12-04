import { useState, useMemo } from "react";

export default function Toolbox({ params, onChange }) {
    const [local, setLocal] = useState(params);

    // simple debounce so we don't spam parent
    const debounced = useMemo(() => {
        let t;
        return (next) => {
            clearTimeout(t);
            t = setTimeout(() => onChange(next), 150);
        };
    }, [onChange]);

    const update = (k, v) => {
        const next = { ...local, [k]: v };
        setLocal(next);
        debounced(next);
    };

    return (
        <aside className="toolbox" aria-label="experimental controls">
            <div className="toolbox-handle" tabIndex={0} title="Open controls" />
            <div className="toolbox-panel">
                <div className="toolbox-row">
                    <label htmlFor="temperature">temperature</label>
                    <output>{local.temperature.toFixed(2)}</output>
                </div>
                <input
                    id="temperature"
                    type="range"
                    min="0.10" max="1.00" step="0.01"
                    value={local.temperature}
                    onChange={(e) => update("temperature", parseFloat(e.target.value))}
                />

                <div className="toolbox-row">
                    <label htmlFor="steps">steps</label>
                    <output>{local.steps}</output>
                </div>
                <input
                    id="steps"
                    type="range"
                    min="1" max="12" step="1"
                    value={local.steps}
                    onChange={(e) => update("steps", parseInt(e.target.value, 10))}
                />
            </div>
        </aside>
    );
}
