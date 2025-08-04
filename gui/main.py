import os, sys
from tempfile import NamedTemporaryFile
import streamlit as st

from processing import process_files
from timeline import render_timeline


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



# ==========================
# ui: page reader
# ==========================
st.markdown("<h1 style='text-align: center; font-style: italic;'>beyond space</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-style: italic;'>rave latent space explorer generation</h3>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)



# ==========================
# slider for index + timeline above
# ==========================
col1, col2, col3 = st.columns([0.2, 9.6, 0.2])
with col2:
    slider_col1, slider_col2, slider_col3 = st.columns([1.5, 7, 1.5])
    with slider_col2:
        slider_value = st.slider(
            label="drag",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.01,
            format="%.2f"
        )
    render_timeline(slider_value)

# ==========================
# file uploaders
# ==========================
col_upload1, col_upload2 = st.columns(2)
uploaded_file1 = col_upload1.file_uploader("upload first wav file", type=["wav"])
uploaded_file2 = col_upload2.file_uploader("upload second wav file", type=["wav"])


# ==========================
# ui: action buttons
# ==========================
st.markdown("<br>", unsafe_allow_html=True)

if uploaded_file1 and uploaded_file2:
    with NamedTemporaryFile(delete=False, suffix=".wav") as tmp1, \
         NamedTemporaryFile(delete=False, suffix=".wav") as tmp2:
        tmp1.write(uploaded_file1.read())
        tmp2.write(uploaded_file2.read())
        tmp1.flush()
        tmp2.flush()

        if col_upload1.button("automatic processing"):
            outputs, session_folder = process_files(tmp1.name, tmp2.name, automatic=True)
            st.success("transition completed")
            with st.expander("all generated outputs", expanded=True):
                for f in outputs:
                    if os.path.exists(f):
                        st.audio(f)

        if col_upload2.button("manual processing"):
            outputs, session_folder = process_files(tmp1.name, tmp2.name, index=slider_value, automatic=False)
            st.success("generation completed")
            with st.expander("all generated outputs", expanded=True):
                for f in outputs:
                    if os.path.exists(f):
                        st.audio(f)