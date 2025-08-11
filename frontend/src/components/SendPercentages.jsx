// components/SendPercentages.jsx
import { useState } from "react";
import Button from "./Button.jsx";

/**
 * Expects:
 * - percentages: number[] (sum=100), aligned with files order
 * - coords: { x: number, y: number } click position in SVG space
 * - files: File[] (optional: to send names)
 * - backendUrl: string
 */
export default function SendPercentages({ percentages, coords, files = [], backendUrl }) {
    const [pending, setPending] = useState(false);
    const [error, setError] = useState("");

    const canSend =
        Array.isArray(percentages) &&
        percentages.length > 0 &&
        percentages.every(n => Number.isFinite(n)) &&
        coords &&
        Number.isFinite(coords.x) &&
        Number.isFinite(coords.y) &&
        !pending;

    const handleSend = async () => {
        if (!canSend) return;
        setPending(true);
        setError("");

        try {
            const payload = {
                percentages,
                click: coords,
                files: files.map(f => ({ name: f.name, size: f.size, type: f.type })),
                timestamp: new Date().toISOString(),
            };

            const res = await fetch(backendUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });

            if (!res.ok) {
                const txt = await res.text().catch(() => "");
                throw new Error(txt || `HTTP ${res.status}`);
            }
            // Optionally: toast/signal success
        } catch (e) {
            setError(e.message || "Failed to send data");
        } finally {
            setPending(false);
        }
    };

    return (
        <div className="send-block">
            <Button onClick={handleSend} disabled={!canSend}>
                {pending ? "sending…" : "send percentages"}
            </Button>
            {error && <div className="error-text" role="alert">{error}</div>}
        </div>
    );
}
