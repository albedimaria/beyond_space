import os
import torch
import streamlit as st
from utils.gen_with_two_inputs import get_model_ratio_and_dim

# ==========================
# configuration
# ==========================
NUM_STEPS = st.sidebar.slider(
    "number of interpolation steps",
    min_value=2,
    max_value=20,
    value=10,
    step=1
)

DURATION = st.sidebar.slider(
    "clip duration (seconds)",
    min_value=1,
    max_value=10,
    value=3
)

TEMPERATURE = st.sidebar.slider(
    "temperature",
    min_value=0.1,
    max_value=2.0,
    value=1.0,
    step=0.1
)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../organ.ts")

# ==========================
# model loading
# ==========================

@st.cache_resource
def load_model(path: str):
    return torch.jit.load(path)

MODEL = load_model(MODEL_PATH)

downsampling_ratio, latent_dim = get_model_ratio_and_dim(MODEL)
