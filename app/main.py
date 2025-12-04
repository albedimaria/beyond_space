# app/main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
import uuid, shutil, torch
from gen_with_two_inputs import get_rave_output, get_model_ratio_and_dim

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://127.0.0.1:3000","http://localhost:5173","http://127.0.0.1:5173"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

RESULTS_DIR = Path("results"); RESULTS_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = Path("organ.ts")
_model = None

@app.on_event("startup")
def _startup():
    global _model
    if _model is None:
        _model = torch.jit.load(str(MODEL_PATH), map_location="cpu")
        get_model_ratio_and_dim(_model)  # optional: warm-up/info

@app.get("/api/health")
def health():
    return {"ok": True}

@app.post("/api/generate")
async def generate_audio(
    mode: str = Form(...),
    noise: float = Form(1.0),          # ← exact name
    n_steps: int = Form(512),          # ← exact name
    input_file1: UploadFile = File(None),
    input_file2: UploadFile = File(None),
):
    job_id = str(uuid.uuid4())[:8]
    workdir = RESULTS_DIR / job_id
    workdir.mkdir(parents=True, exist_ok=True)

    saved = []
    for i, up in enumerate([input_file1, input_file2], start=1):
        if up is not None:
            dst = workdir / f"input{i}_{up.filename}"
            with dst.open("wb") as f:
                shutil.copyfileobj(up.file, f)
            saved.append(dst)

    in1 = str(saved[0]) if len(saved) >= 1 else None
    in2 = str(saved[1]) if len(saved) >= 2 else None

    try:
        out_path = get_rave_output(
            model=_model,
            mode=mode,
            noise=noise,          # ← pass-through
            n_steps=n_steps,      # ← pass-through
            input_file1=in1,
            input_file2=in2,
            # no output_folder here
        )
    except Exception as e:
        return JSONResponse({"error": f"{e}"}, status_code=500)

    # normalize to job folder
    out_path = Path(out_path) if out_path else None
    if not out_path or not out_path.exists():
        # fallback: pick any wav created in workdir
        wavs = list(workdir.glob("*.wav"))
        if not wavs:
            return JSONResponse({"error": "No output produced"}, status_code=500)
        out_path = wavs[0]
    elif out_path.parent != workdir:
        target = workdir / out_path.name
        try: shutil.move(str(out_path), str(target))
        except Exception: shutil.copy2(str(out_path), str(target))
        out_path = target

    return {"job_id": job_id, "file": f"/api/download/{job_id}/{out_path.name}"}

@app.get("/api/download/{job_id}/{filename}")
def download(job_id: str, filename: str):
    p = RESULTS_DIR / job_id / filename
    if not p.exists():
        return JSONResponse({"error": "file not found"}, status_code=404)
    return FileResponse(p, media_type="audio/wav", filename=filename)
