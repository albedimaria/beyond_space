# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## What this project does

**beyond space** is a web app for navigating a [RAVE](https://github.com/acids-ircam/RAVE) model's latent space using real audio as input. Users upload one or two audio files, which the backend encodes into latent trajectories. A 2D interactive "board" in the UI lets users pick a blend point; the resulting latent interpolation is decoded back to audio and served for download.

The active stack is **FastAPI (Python) + React/Vite**. Several legacy entrypoints exist (`utils/app.py` Flask UI, `app/config.py` + `app/processing.py` Streamlit wiring, `gui/`) — these are not the supported path and should not be modified unless explicitly working on them.

---

## Environment variables

All backend vars have sensible defaults and are optional unless deploying remotely. See `.env.example` for a copy-paste template.

| Variable | Default | Description |
|---|---|---|
| `MODEL_PATH` | `organ.ts` | Path to the TorchScript RAVE model (local file) |
| `RESULTS_DIR` | `results` | Directory where generated `.wav` files are stored |
| `ALLOWED_ORIGINS` | `http://localhost:3000,...` | Comma-separated CORS origins |
| `HF_REPO_ID` | *(empty)* | HuggingFace Hub repo ID; if set and `MODEL_PATH` doesn't exist, the model is downloaded automatically |
| `HF_FILENAME` | `organ.ts` | Filename to download from the HF Hub repo |
| `VITE_API_BASE` | `http://127.0.0.1:8000` | Frontend only — set in `frontend/.env` |

---

## Running the project

### Backend

Requires a TorchScript model file at the project root (e.g. `organ.ts`).

```bash
# from project root
uvicorn app.main:app --reload
# API available at http://127.0.0.1:8000
```

### Frontend

```bash
cd frontend
npm install        # first time only
npm run dev        # dev server at http://localhost:5173
```

Configure the backend URL (defaults to `http://127.0.0.1:8000` if unset):

```bash
echo VITE_API_BASE=http://127.0.0.1:8000 > frontend/.env
```

### Frontend commands

```bash
npm run build      # production build
npm run lint       # ESLint
npm run preview    # preview production build
```

---

## Architecture

### Backend (`app/main.py`)

Single FastAPI file. Loads the TorchScript model once at startup (`torch.jit.load`) and holds it in a module-level `_model` global. Two endpoints:

- `POST /api/generate` — accepts `mode`, `noise`, `n_steps` form fields and up to two audio file uploads. Saves uploads under `results/<job_id>/`, calls `get_rave_output(...)` from `utils/gen_with_two_inputs.py`, moves the output `.wav` into the job folder, returns `{ job_id, file }`.
- `GET /api/download/{job_id}/{filename}` — serves the generated file.

### Core audio logic (`utils/gen_with_two_inputs.py`)

All RAVE operations live here:

- `encode_input_file` — loads audio (resampled to 48 kHz mono), encodes via `model.encode()`
- `generate_latent` — linear interpolation between two latent tensors at a given `index` (0–1)
- `decode` — calls `model.decode()` on a latent tensor
- `get_rave_output` — orchestrates encode → interpolate → decode → write `.wav`; the `mode` param is `"encode"` (two files) or `"prior"` (sample from model prior, partially implemented)
- `get_model_ratio_and_dim` — probes the model to determine downsampling ratio and latent dimensionality

**Note:** The `get_rave_output` signature in `utils/gen_with_two_inputs.py` has a different (older, more verbose) signature than what `app/main.py` actually calls. `app/main.py` passes only `model`, `mode`, `noise`, `n_steps`, `input_file1`, `input_file2` — no `duration`, `scale`, `bias`, `output_folder`, etc. These two signatures are **out of sync**; be careful when modifying either.

### Frontend state flow (`frontend/src/`)

`Experience.jsx` is the single top-level state container. It owns:
- `files` — uploaded `File` objects (up to 2)
- `mode` — blend weighting mode (`"sum"` | `"inverse"` | `"gaussian"`)
- `percentages` — integer array summing to 100, derived from click position
- `lastClick` — `{x, y}` in SVG coordinates
- `params` — `{ temperature, steps }` (map to backend `noise` and `n_steps`)

**Click → percentages:** `ShapeVisualizer` renders an SVG board via `ShapeCanvas`. On click it calls `calculatePercentages(clickPoint, layout.points, { mode })` (`utils/calculatePercentages.js`), which weights each layout point by distance using the selected mode and normalises to integers summing to 100. The result is lifted up to `Experience` via `onCompute`.

**Generate → download:** `SendPercentages` calls `generateAudio()` from `api.js` (a thin `fetch` wrapper), receives `{ job_id, file }`, and sets a download link to `${API_BASE}${result.file}`.

**Layout system:** `shapeLayouts.js` defines SVG-coordinate point sets keyed by file count (1, 2, …). `ShapeVisualizer` picks the matching layout based on `files.length`.

### Naming mismatch to be aware of

The UI slider labelled "temperature" is sent to the backend as `noise` (and maps to the `noise` parameter in `get_rave_output`). The UI slider labelled "steps" maps to `n_steps`. The frontend `mode` field is the blending-weight mode (`"sum"` / `"inverse"` / `"gaussian"`), **not** the RAVE model mode (`"encode"` / `"prior"`) — the RAVE mode is always hardcoded to `"encode"` in the current flow.
