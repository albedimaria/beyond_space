const API_BASE = import.meta?.env?.VITE_API_BASE || "http://127.0.0.1:8000";

export async function generateAudio({ mode, temperature, steps, file1, file2 }) {
  const form = new FormData();
  form.append("mode", String(mode));
  form.append("temperature", String(temperature));
  form.append("steps", String(steps));
  if (file1) form.append("input_file1", file1);
  if (file2) form.append("input_file2", file2);

  const res = await fetch(`${API_BASE}/api/generate`, { method: "POST", body: form });
  if (!res.ok) throw new Error(await res.text().catch(() => `HTTP ${res.status}`));
  return res.json(); // { job_id, file }
}

export { API_BASE };
