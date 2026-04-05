import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import io
import cv2
from rembg import remove
import streamlit.components.v1 as components

# =========================
# PAGE CONFIG
# =========================
favicon = Image.open("favicon.png")

st.set_page_config(
    page_title="AI Image Dashboard",
    page_icon=favicon,
    layout="wide"
)

# =========================
# NAVBAR CSS
# =========================
st.markdown("""
<style>

/* REMOVE SIDEBAR */
section[data-testid="stSidebar"] {
    display: none;
}

/* NAVBAR */
.navbar {
    background: linear-gradient(90deg, #2196F3, #64B5F6);
    padding: 12px 30px;
    border-radius: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* TITLE */
.nav-title {
    color: white;
    font-size: 20px;
    font-weight: bold;
}

/* BUTTON STYLE */
.nav-btn button {
    background: transparent !important;
    border: none !important;
    color: white !important;
    font-size: 16px;
}

.nav-btn button:hover {
    text-decoration: underline;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "tool" not in st.session_state:
    st.session_state.tool = "🎨 Background Change"

# =========================
# NAVBAR
# =========================
col1, col2 = st.columns([3,2])

with col1:
    st.markdown("<div class='nav-title'>🎨 AI Image Dashboard</div>", unsafe_allow_html=True)

with col2:
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("Home"):
            st.session_state.tool = None

    with c2:
        if st.button("Tools"):
            st.session_state.tool = "🎨 Background Change"

    with c3:
        uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"])

# =========================
# HOME PAGE
# =========================
if st.session_state.tool is None:
    st.title("✨ AI Image Dashboard")
    st.info("👆 Upload image & click Tools")

# =========================
# TOOLS SECTION
# =========================
else:

    st.title("🧰 Tools")

    tool = st.selectbox(
        "Select Tool",
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
        components.html("""YOUR BLUR TOOL HTML HERE""", height=750)

    # =========================
    # ERASER TOOL
    # =========================
    elif tool == "🖌 Manual Object Eraser":
        st.subheader("🖌 Manual Object Eraser")
        components.html("""YOUR ERASER HTML HERE""", height=800)

    else:
        st.warning("⚠ Upload image first")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("🚀 AI Image Dashboard")
