import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import io
import cv2
from rembg import remove
import streamlit.components.v1 as components

# =========================
# CONFIG + FAVICON
# =========================
try:
    favicon = Image.open("favicon.png")
except:
    favicon = "✨"

st.set_page_config(
    page_title="AI Image Studio",
    page_icon=favicon,
    layout="wide"
)

# =========================
# SESSION STATE
# =========================
if "tool" not in st.session_state:
    st.session_state.tool = "🎨 Background Change"

# =========================
# HIDE STREAMLIT UI
# =========================
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =========================
# NAVBAR
# =========================
st.markdown("""
<style>
.navbar {
    display:flex;
    justify-content:space-between;
    padding:15px 30px;
    background: linear-gradient(90deg,#8E2DE2,#C471ED);
    border-radius:12px;
}
.nav-title {color:white;font-size:22px;font-weight:bold;}
</style>

<div class="navbar">
<div class="nav-title">🎨 AI Image Studio</div>
</div>
""", unsafe_allow_html=True)

# =========================
# HERO
# =========================
st.markdown("""
<h1 style='text-align:center;'>Create Stunning Images with AI</h1>
<p style='text-align:center;color:gray;'>
Remove objects, enhance images, and edit like a pro
</p>
""", unsafe_allow_html=True)

# LOGO
col1, col2, col3 = st.columns([1,2,1])
with col2:
    try:
        st.image("logo.png", width=180)
    except:
        pass

# =========================
# TOOL CARDS (CLICKABLE)
# =========================
st.markdown("## 🚀 All Tools")

cols = st.columns(3)

tools = [
    "🎨 Background Change",
    "✨ Enhance Image",
    "🧍 Auto Person Remove",
    "🌄 Background Removal",
    "✨ Blur Object Tool",
    "🖌 Manual Object Eraser"
]

for i, t in enumerate(tools):
    with cols[i % 3]:
        if st.button(t):
            st.session_state.tool = t
            st.rerun()

# =========================
# SIDEBAR
# =========================
st.sidebar.title("⚡ Tools Panel")

uploaded_file = st.sidebar.file_uploader(
    "Upload Image", type=["png", "jpg", "jpeg"]
)

tool = st.sidebar.radio(
    "Select Tool",
    tools,
    index=tools.index(st.session_state.tool)
)

# =========================
# IMAGE LOAD
# =========================
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    image.thumbnail((600, 600))

    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Before")

    # =========================
    # BACKGROUND CHANGE
    # =========================
    if tool == "🎨 Background Change":
        color_hex = st.sidebar.color_picker("Pick Color", "#00ffaa")
        color = tuple(int(color_hex[i:i+2], 16) for i in (1,3,5))

        if st.sidebar.button("Apply"):
            with st.spinner("Processing..."):
                arr = np.array(image)
                mask = np.mean(arr, axis=2) > 200
                arr[mask] = color
                result = Image.fromarray(arr)

            with col2:
                st.image(result, caption="After")
            st.download_button("Download", io.BytesIO(result.tobytes()))

    # =========================
    # ENHANCE
    # =========================
    elif tool == "✨ Enhance Image":
        if st.sidebar.button("Enhance"):
            with st.spinner("Enhancing..."):
                result = image.filter(ImageFilter.SHARPEN)

            with col2:
                st.image(result)

    # =========================
    # PERSON REMOVE
    # =========================
    elif tool == "🧍 Auto Person Remove":
        if st.sidebar.button("Remove"):
            with st.spinner("Removing..."):
                mask_img = remove(image)
                mask = np.array(mask_img)
                alpha = mask[:,:,3]
                _, binary = cv2.threshold(alpha,10,255,cv2.THRESH_BINARY)
                result = cv2.inpaint(np.array(image), binary, 3, cv2.INPAINT_TELEA)

            with col2:
                st.image(result)

    # =========================
    # BG REMOVE
    # =========================
    elif tool == "🌄 Background Removal":
        if st.sidebar.button("Remove BG"):
            with st.spinner("Removing background..."):
                out = remove(image.convert("RGBA"))

            with col2:
                st.image(out)

# =========================
# HTML TOOLS (UNCHANGED)
# =========================
elif tool == "✨ Blur Object Tool":
    st.subheader("Blur Tool")
    components.html("<h3>Keep your existing blur code here</h3>", height=500)

elif tool == "🖌 Manual Object Eraser":
    st.subheader("Eraser Tool")
    components.html("<h3>Keep your existing eraser code here</h3>", height=500)

else:
    st.info("Upload an image to start")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("© 2026 AI Image Studio")
