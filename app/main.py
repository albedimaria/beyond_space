from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
import uuid
import shutil

# TODO: import your actual inference utilities
# from app.processing import get_rave_output, get_model_ratio_and_dim

app = FastAPI()

# CORS (adjust origins for your dev host/port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "https://*.codesandbox.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Simple health check
@app.get("/api/health")
def health():
    return {"ok": True}

@app.post("/api/generate")
async def generate_audio(
    mode: str = Form(...),                 # e.g., "interpolate" | "encode" | "decode"
    temperature: float = Form(1.0),
    randomness: float = Form(0.5),
    steps: int = Form(512),
    input_file1: UploadFile = File(None),
    input_file2: UploadFile = File(None),
):
    # create a working dir per job
    job_id = str(uuid.uuid4())[:8]
    workdir = RESULTS_DIR / job_id
    workdir.mkdir(parents=True, exist_ok=True)

    # save inputs if provided
    saved_paths = []
    for i, up in enumerate([input_file1, input_file2], start=1):
        if up is not None:
            dst = workdir / f"input{i}_{up.filename}"
            with dst.open("wb") as f:
                shutil.copyfileobj(up.file, f)
            saved_paths.append(str(dst))

    # ---- CALL YOUR MODEL PIPELINE HERE ----
    # downsampling_ratio, latent_dim = get_model_ratio_and_dim(model)
    # out_path = get_rave_output(
    #     model=model,
    #     mode=mode,
    #     temperature=temperature,
    #     randomness=randomness,
    #     steps=steps,
    #     input_file1=saved_paths[0] if len(saved_paths) >= 1 else None,
    #     input_file2=saved_paths[1] if len(saved_paths) >= 2 else None,
    #     output_folder=str(workdir),
    # )

    # TEMP: produce a dummy wav so frontend flow works immediately
    out_path = workdir / "output.wav"
    with out_path.open("wb") as f:
        f.write(b"RIFF\0\0\0\0WAVEfmt ")  # minimal header stub for testing flow

    return JSONResponse({
        "job_id": job_id,
        "file": f"/api/download/{job_id}/output.wav"
    })

@app.get("/api/download/{job_id}/{filename}")
def download(job_id: str, filename: str):
    path = RESULTS_DIR / job_id / filename
    if not path.exists():
        return JSONResponse({"error": "file not found"}, status_code=404)
    return FileResponse(path)
