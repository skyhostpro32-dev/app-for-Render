import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import io
import cv2
from rembg import remove
import streamlit.components.v1 as components

# =========================
# ✅ PAGE CONFIG
# =========================
favicon = Image.open("favicon.png")

st.set_page_config(
    page_title="AI Image Studio",
    page_icon=favicon,
    layout="wide"
)

# =========================
# 🌐 TOP NAVBAR
# =========================
st.markdown("""
<style>
.navbar {
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:15px 30px;
    background: linear-gradient(90deg,#a4508b,#5f0a87);
    border-radius:10px;
    margin-bottom:20px;
}
.nav-title {
    color:white;
    font-size:22px;
    font-weight:bold;
}
</style>

<div class="navbar">
    <div class="nav-title">🎨 AI Image Studio</div>
</div>
""", unsafe_allow_html=True)

# =========================
# 🎯 TOP CONTROLS
# =========================
col1, col2 = st.columns([2,3])

with col1:
    uploaded_file = st.file_uploader("📤 Upload Image", type=["png","jpg","jpeg"])

with col2:
    tool = st.selectbox(
        "🧰 Select Tool",
        [
            "🎨 Background Change",
            "✨ Enhance Image",
            "🧍 Auto Person Remove",
            "🌄 Background Removal",
            "✨ Blur Object Tool",
            "🖌 Manual Object Eraser"
        ]
    )

# =========================
# 🏠 LANDING PAGE (NO IMAGE)
# =========================
if uploaded_file is None:

    st.markdown("""
    <h1 style='text-align:center;'>Create Stunning Images with AI</h1>
    <p style='text-align:center; color:gray; font-size:18px;'>
    Remove objects, enhance photos, and edit like a pro in seconds.
    </p>
    """, unsafe_allow_html=True)

    st.image("logo.png", width=200)

    colA, colB, colC = st.columns(3)

    with colA:
        st.markdown("🎨 **Background Edit**<br>Fast<br><small>AI Powered</small>", unsafe_allow_html=True)

    with colB:
        st.markdown("✨ **Enhancement**<br>HD Quality<br><small>+Sharpness</small>", unsafe_allow_html=True)

    with colC:
        st.markdown("🧍 **Object Removal**<br>Smart<br><small>Auto Detect</small>", unsafe_allow_html=True)

    st.info("👆 Upload image to start editing")

# =========================
# NORMAL TOOLS
# =========================
if uploaded_file and tool not in ["✨ Blur Object Tool", "🖌 Manual Object Eraser"]:

    image = Image.open(uploaded_file).convert("RGB")
    image.thumbnail((600, 600))
    st.image(image)

    if tool == "🎨 Background Change":
        color_hex = st.color_picker("Pick Background Color", "#00ffaa")
        color = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))

        if st.button("Apply"):
            arr = np.array(image)
            mask = np.mean(arr, axis=2) > 200
            arr[mask] = color
            result = Image.fromarray(arr)

            st.image(result)
            buf = io.BytesIO()
            result.save(buf, format="PNG")
            st.download_button("Download", buf.getvalue())

    elif tool == "✨ Enhance Image":
        strength = st.slider("Sharpness", 1, 5, 2)

        if st.button("Enhance"):
            result = image
            for _ in range(strength):
                result = result.filter(ImageFilter.SHARPEN)

            st.image(result)
            buf = io.BytesIO()
            result.save(buf, format="PNG")
            st.download_button("Download", buf.getvalue())

    elif tool == "🧍 Auto Person Remove":
        if st.button("Remove"):
            mask_img = remove(image)
            mask = np.array(mask_img)

            alpha = mask[:, :, 3] if mask.shape[2] == 4 else cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY)
            _, binary = cv2.threshold(alpha, 10, 255, cv2.THRESH_BINARY)

            result = cv2.inpaint(np.array(image), binary, 3, cv2.INPAINT_TELEA)

            st.image(result)
            st.download_button("Download", cv2.imencode(".png", result)[1].tobytes())

    elif tool == "🌄 Background Removal":
        if st.button("Remove BG"):
            out = remove(image.convert("RGBA"))

            st.image(out)
            buf = io.BytesIO()
            out.save(buf, format="PNG")
            st.download_button("Download", buf.getvalue())

# =========================
# BLUR TOOL
# =========================
elif tool == "✨ Blur Object Tool":

    st.subheader("✨ Blur Object Tool")

    components.html("""YOUR EXISTING BLUR TOOL CODE HERE""", height=750)

# =========================
# MANUAL ERASER
# =========================
elif tool == "🖌 Manual Object Eraser":

    st.subheader("🖌 Smart Object Eraser")

    components.html("""YOUR EXISTING ERASER CODE HERE""", height=800)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("🚀 AI Image Studio | Built for creators")
