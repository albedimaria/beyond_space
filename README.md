## overview

This repository implements a web‑based front end to a TorchScript RAVE model.
The goal is to let you **navigate and manipulate the model’s latent space**
using real audio as input:

- **Upload one or two audio files**; the backend encodes them into latent
  trajectories using the RAVE model.
- **Choose a mixing mode and a point on a 2D latent board** to define how the
  two latent trajectories are combined.
- **Control the number of latent steps** (`n_steps`) and noise/temperature to
  decide how densely the trajectory is sampled and how much stochasticity is
  injected.
- **Decode the resulting latent path back to audio** and download the generated
  `.wav` file.

Conceptually, you are not only cross‑fading between two waveforms: you are
interpolating between their encodings in latent space over a controllable number
of steps, which can produce structured morphs rather than simple fades.

---

## stack

- **backend**
  - Python 3.x
  - FastAPI
  - PyTorch (TorchScript model, e.g. `organ.ts`)
  - Audio: `soundfile`, `librosa`, `numpy`
- **frontend**
  - React
  - Vite

---

## getting started

### backend (FastAPI)

From the project root:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

By default the API will be available at `http://127.0.0.1:8000`.

Key endpoints:

- `POST /api/generate`  
  Accepts:
  - form fields: `mode`, `noise`, `n_steps`
  - optional files: `input_file1`, `input_file2`
  Runs the RAVE model and stores a `.wav` file under `results/<job_id>/`.

- `GET /api/download/{job_id}/{filename}`  
  Serves the generated `.wav` file for download.

Make sure a TorchScript model file (e.g. `organ.ts`) is present at the expected
path used in `app/main.py`.

### frontend (React/Vite)

From the project root:

```bash
cd frontend
npm install
npm run dev
```

The dev server will typically run at `http://localhost:5173/`.

---

## configuration

The frontend reads the backend URL from `import.meta.env.VITE_API_BASE`.
For a local setup where FastAPI listens on `http://127.0.0.1:8000`:

```bash
cd frontend
echo VITE_API_BASE=http://127.0.0.1:8000 > .env
```

or create `frontend/.env` manually:

```text
VITE_API_BASE=http://127.0.0.1:8000
```

If `VITE_API_BASE` is not set, the frontend falls back to `http://127.0.0.1:8000`.

---

## project layout

- `app/`
  - `main.py` – FastAPI application:
    - configures CORS for local dev
    - loads the TorchScript model on startup
    - exposes `/api/generate` and `/api/download/...`
- `utils/`
  - `gen_with_two_inputs.py` – helper functions for:
    - loading/resampling audio
    - encoding/decoding through the RAVE model
    - interpolating between two latent encodings
    - writing `.wav` output files
- `frontend/`
  - `src/core/Experience.jsx` – top‑level page and state orchestration
  - `src/components/ShapeVisualizer/*` – latent “board” layout and click handling
  - `src/components/FileUploader.jsx` – audio file upload (up to four files)
  - `src/components/ControlBar.jsx` / `SendPercentages.jsx` – mode selection,
    parameter sliders, and generate/download wiring
  - `vite.config.js`, `package.json` – Vite / npm configuration
- `requirements.txt` – Python dependencies for the backend and audio utilities.

---

## legacy / experimental code

In addition to the FastAPI + React/Vite path, the repo contains several
historical or experimental entrypoints that are **not** the main interface:

- `utils/app.py` – older Flask‑based UI
- `app.py` – Streamlit script
- `gui/` – various GUI prototypes/scripts

These can serve as references or playgrounds if you want to experiment with
alternative frontends, but the supported flow is:

1. run the FastAPI app from `app/main.py`
2. run the React/Vite frontend from `frontend/`

