// components/ModeBar.jsx
export default function ModeBar({ mode, setMode }) {
    return (
        <div className="mode-bar">
            <select
                id="mode-select"
                value={mode}
                onChange={(e) => setMode(e.target.value)}
                aria-label="percentage mode"
            >
                <option value={""} disabled >mode</option>
                <option value="sum">farther ⇒ higher %</option>
                <option value="gaussian">smooth proximity</option>
                <option value="inverse"> farther ⇒ lower %</option>
            </select>
        </div>
    );
}
