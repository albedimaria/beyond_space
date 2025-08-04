import os
import datetime
import streamlit as st

from utils.gen_with_two_inputs import get_rave_output
from app_def.config import MODEL, NUM_STEPS, DURATION, TEMPERATURE, downsampling_ratio, latent_dim

def create_session_folder(base_dir="audio_outputs"):
    """create session folder with timestamp"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    session_folder = os.path.join(base_dir, f"session_{timestamp}")
    os.makedirs(session_folder, exist_ok=True)
    return session_folder

def generate_outputs(input1, input2, session_folder, indices):
    """generate audio audio_outputs for given indices"""
    output_files = []
    for idx in indices:
        output = get_rave_output(
            model=MODEL,
            mode="encode",
            duration=DURATION,
            temperature=TEMPERATURE,
            input_file1=input1,
            input_file2=input2,
            output_file="output.wav",
            downsampling_ratio=downsampling_ratio,
            scale=[1.0] * latent_dim,
            bias=[0.0] * latent_dim,
            noise_amount=0.0,
            index=idx,
            output_folder=session_folder,
        )
        output_files.append(output)
    return output_files

def process_files(input1, input2, index=None, automatic=False):
    """wrapper for generate_outputs with streamlit feedback"""
    session_folder = create_session_folder()

    if automatic:
        indices = [i / (NUM_STEPS - 1) for i in range(NUM_STEPS)]
        progress_bar = st.progress(0)
        outputs = generate_outputs(input1, input2, session_folder, indices)
        for i in range(len(outputs)):
            progress_bar.progress((i + 1) / NUM_STEPS)
    else:
        outputs = generate_outputs(input1, input2, session_folder, [index])

    return outputs, session_folder