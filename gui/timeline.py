import streamlit as st

def render_timeline(slider_value: float):
    """render timeline with slider marker"""
    timeline_css = f"""
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
    .start-sphere {{ left: 2%; }}
    .end-sphere {{ left: 98%; }}
    .moving-sphere {{
        left: calc(2% + 96% * {slider_value});
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
    st.markdown(timeline_css, unsafe_allow_html=True)
