# app/main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
from huggingface_hub import hf_hub_download
import os, uuid, shutil, json, torch
import soundfile as sf
from utils.gen_with_two_inputs import generate_barycentric, get_rave_output, get_model_ratio_and_dim

ALLOWED_ORIGINS = os.environ.get(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173,https://*.hf.space,https://*.vercel.app"
).split(",")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

RESULTS_DIR = Path(os.environ.get("RESULTS_DIR", "results")); RESULTS_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = Path(os.environ.get("MODEL_PATH", "organ.ts"))
HF_REPO_ID = os.environ.get("HF_REPO_ID", "")
HF_FILENAME = os.environ.get("HF_FILENAME", "organ.ts")
CACHE_DIR = Path(os.environ.get("MODEL_CACHE_DIR", "/data/models"))
_model = None

@app.on_event("startup")
def _startup():
    global _model, MODEL_PATH

    # step a: check local path
    print(f"MODEL_PATH resolved to: {MODEL_PATH}")
    print(f"Model file exists: {MODEL_PATH.exists()}")

    # step b: download from HF Hub if needed
    if not MODEL_PATH.exists():
        if not HF_REPO_ID:
            raise RuntimeError(
                f"Model file not found at '{MODEL_PATH}' and HF_REPO_ID is not set. "
                "Provide a local model or set HF_REPO_ID."
            )
        print(f"Downloading model from HF Hub: {HF_REPO_ID}/{HF_FILENAME}")
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        downloaded = hf_hub_download(
            repo_id=HF_REPO_ID,
            filename=HF_FILENAME,
            cache_dir=str(CACHE_DIR),
        )
        MODEL_PATH = Path(downloaded)
        print(f"MODEL_PATH resolved to: {MODEL_PATH}")
        print(f"Model file exists: {MODEL_PATH.exists()}")

    # step c: guard before load
    if not MODEL_PATH.exists():
        raise RuntimeError(
            f"Model file still not found at '{MODEL_PATH}' after download attempt."
        )

    # step d: load
    print("Loading model...")
    if _model is None:
        _model = torch.jit.load(str(MODEL_PATH), map_location="cpu")
        get_model_ratio_and_dim(_model)  # optional: warm-up/info
    print("Model loaded successfully.")

@app.get("/api/health")
def health():
    return {"ok": True}

@app.post("/api/generate")
async def generate_audio(
    rave_mode: str = Form("encode"),
    noise: float = Form(1.0),
    n_steps: int = Form(512),
    weights: str = Form(""),
    input_file1: UploadFile = File(None),
    input_file2: UploadFile = File(None),
    input_file3: UploadFile = File(None),
    input_file4: UploadFile = File(None),
):
    job_id = str(uuid.uuid4())[:8]
    workdir = RESULTS_DIR / job_id
    workdir.mkdir(parents=True, exist_ok=True)

    # save all uploaded files and collect their paths
    audio_paths = []
    for i, up in enumerate([input_file1, input_file2, input_file3, input_file4], start=1):
        if up is not None:
            dst = workdir / f"input{i}_{up.filename}"
            with dst.open("wb") as f:
                shutil.copyfileobj(up.file, f)
            audio_paths.append(str(dst))

    if not audio_paths:
        return JSONResponse({"error": "No input files provided"}, status_code=400)

    # parse weights; fall back to equal weights if missing or mismatched
    parsed_weights = None
    if weights:
        try:
            parsed_weights = json.loads(weights)
        except (json.JSONDecodeError, ValueError):
            parsed_weights = None
    if parsed_weights is None or len(parsed_weights) != len(audio_paths):
        parsed_weights = [1.0 / len(audio_paths)] * len(audio_paths)

    try:
        audio_np, sample_rate = generate_barycentric(
            audio_paths=audio_paths,
            weights=parsed_weights,
            model=_model,
            n_steps=n_steps,
            noise=noise,
            rave_mode=rave_mode,
        )
    except Exception as e:
        return JSONResponse({"error": f"{e}"}, status_code=500)

    out_path = workdir / "output.wav"
    sf.write(str(out_path), audio_np, sample_rate)

    return {"job_id": job_id, "file": f"/api/download/{job_id}/output.wav"}

@app.get("/api/download/{job_id}/{filename}")
def download(job_id: str, filename: str):
    p = RESULTS_DIR / job_id / filename
    if not p.exists():
        return JSONResponse({"error": "file not found"}, status_code=404)
    return FileResponse(p, media_type="audio/wav", filename=filename)
