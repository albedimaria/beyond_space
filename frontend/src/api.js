const API_BASE = import.meta?.env?.VITE_API_BASE || "http://127.0.0.1:8000";

export async function generateAudio({ files, weights, noise, n_steps, rave_mode = "encode", model_name = "organ_archive_b2048_r48000_z16" }) {
  const form = new FormData();
  form.append("rave_mode", String(rave_mode));
  form.append("noise", String(noise));
  form.append("n_steps", String(n_steps));
  form.append("model_name", String(model_name));
  form.append("weights", JSON.stringify(weights.map(w => w / 100)));
  files.forEach((f, i) => form.append(`input_file${i + 1}`, f));

  const res = await fetch(`${API_BASE}/api/generate`, { method: "POST", body: form });
  if (!res.ok) throw new Error(await res.text().catch(() => `HTTP ${res.status}`));
  return res.json(); // { job_id, file }
}

export async function fetchModels() {
  const res = await fetch(`${API_BASE}/api/models`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const data = await res.json();
  return data.models;
}

export { API_BASE };
