# app/main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
from huggingface_hub import hf_hub_download
import os, uuid, shutil, json, torch
import numpy as np
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

AVAILABLE_MODELS = [
    "organ_archive_b2048_r48000_z16",
    "organ_bach_b2048_sr48000_z16",
    "guitar_iil_b2048_r48000_z16",
    "voice_vocalset_b2048_r48000_z16",
    "voice_hifitts_b2048_r48000_z16",
    "birds_motherbird_b2048_r48000_z16",
    "birds_pluma_b2048_r48000_z16",
    "water_pondbrain_b2048_r48000_z16",
]

_model_cache = {}

def _get_model(model_name: str):
    """Return a cached TorchScript model, downloading and loading it on first use."""
    global _model_cache
    if model_name in _model_cache:
        return _model_cache[model_name]

    filename = f"{model_name}.ts"
    local_path = MODEL_PATH.parent / filename

    if not local_path.exists():
        if not HF_REPO_ID:
            raise RuntimeError(
                f"Model '{filename}' not found locally and HF_REPO_ID is not set."
            )
        print(f"Downloading model from HF Hub: {HF_REPO_ID}/{filename}")
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        local_path = Path(hf_hub_download(
            repo_id=HF_REPO_ID,
            filename=filename,
            cache_dir=str(CACHE_DIR),
        ))

    print(f"Loading model: {model_name}")
    model = torch.jit.load(str(local_path), map_location="cpu")
    _model_cache[model_name] = model
    print(f"Model loaded: {model_name}")
    return model


@app.on_event("startup")
def _startup():
    # Pre-load the default model so the first request is fast
    default_name = Path(HF_FILENAME).stem  # strip .ts
    if default_name not in AVAILABLE_MODELS:
        default_name = AVAILABLE_MODELS[0]

    print(f"Pre-loading default model: {default_name}")
    try:
        _get_model(default_name)
    except Exception as e:
        raise RuntimeError(f"Failed to load default model '{default_name}': {e}")

@app.get("/api/health")
def health():
    return {"ok": True}

@app.get("/api/models")
def list_models():
    return {"models": AVAILABLE_MODELS}

@app.post("/api/generate")
async def generate_audio(
    rave_mode: str = Form("encode"),
    noise: float = Form(1.0),
    n_steps: int = Form(512),
    weights: str = Form(""),
    model_name: str = Form("organ_archive_b2048_r48000_z16"),
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

    if model_name not in AVAILABLE_MODELS:
        return JSONResponse({"error": f"Unknown model '{model_name}'"}, status_code=400)

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
        model = _get_model(model_name)
        audio_np, sample_rate = generate_barycentric(
            audio_paths=audio_paths,
            weights=parsed_weights,
            model=model,
            n_steps=n_steps,
            noise=noise,
            rave_mode=rave_mode,
        )
    except Exception as e:
        return JSONResponse({"error": f"{e}"}, status_code=500)

    out_path = workdir / "output.wav"
    # write as 16-bit PCM — universally playable (float WAV is not supported by
    # most browsers and many common players)
    audio_np = np.clip(audio_np.astype(np.float32), -1.0, 1.0)
    sf.write(str(out_path), audio_np, sample_rate, subtype="PCM_16")

    return {"job_id": job_id, "file": f"/api/download/{job_id}/output.wav"}

@app.get("/api/download/{job_id}/{filename}")
def download(job_id: str, filename: str):
    p = RESULTS_DIR / job_id / filename
    if not p.exists():
        return JSONResponse({"error": "file not found"}, status_code=404)
    return FileResponse(p, media_type="audio/wav", filename=filename)
