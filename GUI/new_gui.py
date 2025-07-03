import numpy as np
import sounddevice as sd
import streamlit as st
import torch
import soundfile as sf
import sys
import os
from tempfile import NamedTemporaryFile
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gen_with_two_inputs import get_rave_output, get_model_ratio_and_dim

# ==========================
# Model
# ==========================
# Load your model once
@st.cache_resource
def load_model(path):
    return torch.jit.load(path)

model = load_model("../organ.ts")

downsampling_ratio, latent_dim = get_model_ratio_and_dim(model)

NUM_STEPS = 10

# ==========================
# Title
# ==========================
st.markdown("<h1 style='text-align: center; font-style: italic;'>beyond space</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-style: italic;'>rave latent space explorer generation</h3>", unsafe_allow_html=True)
st.write("")
st.write("")
st.write("")


# ==========================
# Slider for index + timeline above
# ==========================
col1, col2, col3 = st.columns([0.2, 9.6, 0.2])  # Adjust ratios as needed

with col2:
    # ==========================
    # Slider with reduced width FIRST
    # ==========================
    slider_col1, slider_col2, slider_col3 = st.columns([1.5, 7, 1.5])  # Adjust ratios as needed

    with slider_col2:
        index = st.slider(
            label="drag",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.01,
            format="%.2f",
            help="",
            disabled=False
        )

    # ==========================
    # Now render timeline with LIVE index value
    # ==========================
    timeline_html = f"""
    <style>
    .timeline-container {{
        position: relative;
        width: 100%;
        height: 60px;
        margin: 20px 0;
    }}

    .timeline-line {{
        position: absolute;
        top: 50%;
        left: 2%;
        width: 96%;
        height: 2px;
        background: #bbb;
        z-index: 0;
    }}

    .timeline-sphere {{
        position: absolute;
        top: 50%;
        transform: translate(-50%, -50%);
        font-size: 30px;
        z-index: 1;
    }}

    .start-sphere {{
        left: 2%;
    }}

    .end-sphere {{
        left: 98%;
    }}

    .moving-sphere {{
        left: calc(2% + 96% * {index});
        font-size: 25px;
        color: white;
    }}
    </style>

    <div class="timeline-container">
        <div class="timeline-line"></div>
        <div class="timeline-sphere start-sphere">🟢</div>
        <div class="timeline-sphere moving-sphere">🔻</div>
        <div class="timeline-sphere end-sphere">🟢</div>
    </div>
    """

    st.markdown(timeline_html, unsafe_allow_html=True)

    st.write("")

# ==========================
# File uploaders
# ==========================
col_upload1, col_upload2 = st.columns(2)

with col_upload1:
    uploaded_file1 = st.file_uploader("Upload first input WAV file", type=["wav"])

with col_upload2:
    uploaded_file2 = st.file_uploader("Upload second input WAV file", type=["wav"])

# ==========================
# Process button ABOVE
# ==========================
st.markdown("<br>", unsafe_allow_html=True)  # optional spacing

with col_upload1:
    if st.button("automatic processing"):
        if uploaded_file1 and uploaded_file2:
            with NamedTemporaryFile(delete=False, suffix=".wav") as tmp1, \
                 NamedTemporaryFile(delete=False, suffix=".wav") as tmp2:
                tmp1.write(uploaded_file1.read())
                tmp2.write(uploaded_file2.read())
                tmp1.flush()
                tmp2.flush()
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                session_folder = os.path.join("outputs", f"session_{timestamp}")
                os.makedirs("outputs", exist_ok=True)
                os.makedirs(session_folder, exist_ok=True)
                # Define sweep range
                indices = [i / (NUM_STEPS - 1) for i in range(NUM_STEPS)]
                progress_bar = st.progress(0)
                output_files = []
                # Loop over indices
                for i, idx in enumerate(indices):
                    output = get_rave_output(
                        model=model,
                        mode="encode",
                        duration=3.0,
                        temperature=1.0,
                        input_file1=tmp1.name,
                        input_file2=tmp2.name,
                        output_file="output.wav",
                        downsampling_ratio=downsampling_ratio,
                        scale=[1.0] * latent_dim,
                        bias=[0.0] * latent_dim,
                        noise_amount=0.0,
                        index=idx,
                        output_folder=session_folder
                    )
                    output_files.append(output)
                    # Update progress bar
                    progress_bar.progress((i + 1) / NUM_STEPS)
                
                # Create master file by combining segments
                master_audio_segments = []
                segment_duration = None
                sample_rate = None
                
                for i, audio_file in enumerate(output_files):
                    try:
                        if os.path.exists(audio_file):
                            # Load the audio file
                            audio_data, sr = sf.read(audio_file)
                            
                            # Set sample rate from first file
                            if sample_rate is None:
                                sample_rate = sr
                            
                            # Calculate segment length (1/10th of the audio)
                            if segment_duration is None:
                                segment_duration = len(audio_data) // NUM_STEPS
                            
                            # Extract the i-th segment (1/10th) from the i-th audio file
                            start_idx = i * segment_duration
                            end_idx = min((i + 1) * segment_duration, len(audio_data))
                            
                            segment = audio_data[start_idx:end_idx]
                            master_audio_segments.append(segment)
                            
                        else:
                            print(f"File not found: {audio_file}")
                    except Exception as e:
                        print(f"Error processing {audio_file}: {e}")
                
                # Combine all segments into master file
                if master_audio_segments:
                    master_audio = np.concatenate(master_audio_segments)
                    master_file_path = os.path.join(session_folder, "master_transition.wav")
                    sd.play(audio_data, sample_rate)
                    sd.wait()
                    
                    # Save master file
                    sf.write(master_file_path, master_audio, sample_rate)
                    print(f"Master file created: {master_file_path}")
                
                # Display all outputs after processing
                with st.expander("all generated outputs", expanded=True):
                    for f in output_files:
                        # Play the audio file
                        try:
                            if os.path.exists(f):
                                # Load and play the audio
                                audio_data, sample_rate = sf.read(f)
                                print(f"Playing: {f}")
                                #sd.play(audio_data, sample_rate)
                                #sd.wait()  # Wait for playback to finish
                                #print(f"Finished playing: {f}")
                            else:
                                print(f"File not found: {f}")
                        except Exception as e:
                            print(f"Error playing {f}: {e}")
                       
                        # Display in Streamlit
                        st.audio(f)
                        print(f)
                
                # Display master file
                if master_audio_segments:
                    st.subheader("Master Transition File")
                    st.audio(master_file_path)
                    
                    # Play master file
                    try:
                        master_data, master_sr = sf.read(master_file_path)
                        print(f"Playing master file: {master_file_path}")
                        sd.play(master_data, master_sr)
                        sd.wait()
                        print("Finished playing master file")
                    except Exception as e:
                        print(f"Error playing master file: {e}")
                
                st.success(f"transition completed with master file")
        else:
            st.warning("please upload both input files.")


with col_upload2:
    if st.button("manual processing"):

        if uploaded_file1 and uploaded_file2:

            with NamedTemporaryFile(delete=False, suffix=".wav") as tmp1, \
                 NamedTemporaryFile(delete=False, suffix=".wav") as tmp2:

                tmp1.write(uploaded_file1.read())
                tmp2.write(uploaded_file2.read())
                tmp1.flush()
                tmp2.flush()

                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                session_folder = os.path.join("outputs", f"session_{timestamp}")
                os.makedirs("outputs", exist_ok=True)
                os.makedirs(session_folder, exist_ok=True)

                # Call your backend function with slider index
                output = get_rave_output(
                    model=model,
                    mode="encode",
                    duration=3.0,
                    temperature=1.0,
                    input_file1=tmp1.name,
                    input_file2=tmp2.name,
                    output_file="output.wav",
                    downsampling_ratio=downsampling_ratio,
                    scale=[1.0] * latent_dim,
                    bias=[0.0] * latent_dim,
                    noise_amount=0.0,
                    index=index,
                    output_folder=session_folder
                )

                # Display all outputs after processing
                with st.expander("all generated outputs", expanded=True):
                    st.audio(output)

                st.success(f"generation completed")


        else:
            st.warning("Please upload both input files.")

