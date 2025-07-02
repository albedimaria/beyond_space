import streamlit as st
import torch
from tempfile import NamedTemporaryFile
from gen_with_two_inputs import get_rave_output, get_model_ratio_and_dim

# st.title("beyond space")
st.markdown("<h1 style='text-align: center;'>beyond space</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>rave latent space explorer generation</h3>", unsafe_allow_html=True)

# Define timeline with spheres and labels using HTML + CSS
timeline_html = """
<style>
.timeline-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
    margin: 40px 0;
}
.timeline-container::before {
    content: '';
    position: absolute;
    top: 15px;
    left: 5%;
    right: 5%;
    height: 2px;
    background: #bbb;
    z-index: 0;
}
.timeline-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    z-index: 1;
}
.timeline-step .circle {
    font-size: 30px;
    line-height: 30px;
}
.timeline-step .label {
    margin-top: 5px;
    font-size: 14px;
}
</style>

<div class="timeline-container">
    <div class="timeline-step">
        <div class="circle" id="sample1">⚪</div>
        <div class="label">Sample 1</div>
    </div>
    <div class="timeline-step">
        <div class="circle" id="sample2">⚪</div>
        <div class="label">Sample 2</div>
    </div>
    <div class="timeline-step">
        <div class="circle" id="sample3">⚪</div>
        <div class="label">sample 3</div>
    </div>
    <div class="timeline-step">
        <div class="circle" id="sample4">⚪</div>
        <div class="label">sample 4</div>
    </div>
    <div class="timeline-step">
        <div class="circle" id="sample5">⚪</div>
        <div class="label">sample 5</div>
    </div>
</div>
"""

st.markdown(timeline_html, unsafe_allow_html=True)

# Then create the slider below the spheres
slider_value = st.slider("select the index", min_value=0.0, max_value=1.0, value=0.5, step=0.01)

# Upload two audio files
uploaded_file1 = st.file_uploader("Upload first input WAV file", type=["wav"])
uploaded_file2 = st.file_uploader("Upload second input WAV file", type=["wav"])



# Process button
if st.button("Process"):
    if uploaded_file1 and uploaded_file2:

        # Inject JavaScript to update spheres dynamically
        update_script = """
        <script>
        document.getElementById('sample1').innerText = '🟢';
        document.getElementById('sample2').innerText = '🟢';
        document.getElementById('step1').innerText = '🟢';
        </script>
        """
        st.markdown(update_script, unsafe_allow_html=True)

        with NamedTemporaryFile(delete=False, suffix=".wav") as tmp1, NamedTemporaryFile(delete=False, suffix=".wav") as tmp2:
            tmp1.write(uploaded_file1.read())
            tmp2.write(uploaded_file2.read())
            tmp1.flush()
            tmp2.flush()

            update_script = """
            <script>
            document.getElementById('step2').innerText = '🟢';
            </script>
            """
            st.markdown(update_script, unsafe_allow_html=True)

            model_path = "organ.ts"
            model = torch.jit.load(model_path)
            downsampling_ratio, latent_dim = get_model_ratio_and_dim(model)

            update_script = """
            <script>
            document.getElementById('step3').innerText = '🟢';
            </script>
            """
            st.markdown(update_script, unsafe_allow_html=True)

            scale = [1.0] * latent_dim
            bias = [0.0] * latent_dim

            get_rave_output(
                model=model,
                mode="encode",
                duration=3.0,
                temperature=1.0,  # dummy value, unused in encode mode
                input_file1=tmp1.name,
                input_file2=tmp2.name,
                output_file="output.wav",
                downsampling_ratio=downsampling_ratio,
                scale=scale,
                bias=bias,
                noise_amount=0.0
            )

            st.success("Processing complete. Check generated output file.")

    else:
        st.warning("Please upload both input files.")
