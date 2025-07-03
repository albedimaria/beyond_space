import streamlit as st
import torch
import sys
import os
from tempfile import NamedTemporaryFile

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
st.markdown("<h1 style='text-align: center;'>beyond space</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>rave latent space explorer generation</h3>", unsafe_allow_html=True)
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
                        index=idx
                    )

                    output_files.append(output)

                    # Update progress bar
                    progress_bar.progress((i + 1) / NUM_STEPS)

                # Display all outputs after processing
                with st.expander("All generated outputs", expanded=True):
                    for f in output_files:
                        st.audio(f)

                st.success(f"transition completed")

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

                # Call your backend function with slider index
                get_rave_output(
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
                    index=index
                )


        else:
            st.warning("Please upload both input files.")

