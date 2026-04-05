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
    page_title="AI Image Studio",
    page_icon=favicon,
    layout="wide"
)

# =========================
# TOP NAVBAR CSS
# =========================
st.markdown("""
<style>

/* REMOVE SIDEBAR */
section[data-testid="stSidebar"] {
    display: none;
}

/* NAVBAR */
.navbar {
    background: linear-gradient(90deg, #7b2ff7, #9f44d3);
    padding: 15px 30px;
    border-radius: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: white;
}

/* LOGO */
.logo {
    font-size: 20px;
    font-weight: bold;
}

/* NAV LINKS */
.nav-links {
    display: flex;
    gap: 25px;
}

.nav-links button {
    background: none;
    border: none;
    color: white;
    font-size: 16px;
    cursor: pointer;
}

.nav-links button:hover {
    text-decoration: underline;
}

/* CENTER CONTENT */
.center-box {
    text-align: center;
    margin-top: 50px;
}

.tool-card {
    padding: 20px;
    border-radius: 15px;
    background: #f5f5f5;
    margin: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# NAVBAR STATE
# =========================
if "page" not in st.session_state:
    st.session_state.page = "Home"

def nav(page):
    st.session_state.page = page

# =========================
# NAVBAR UI
# =========================
st.markdown(f"""
<div class="navbar">
    <div class="logo">🎨 AI Image Studio</div>
    <div class="nav-links">
        <button onclick="window.location.reload()">Home</button>
    </div>
</div>
""", unsafe_allow_html=True)

# Buttons (Streamlit controlled)
col1, col2, col3, col4 = st.columns([1,1,1,1])

with col1:
    if st.button("🏠 Home"):
        st.session_state.page = "Home"

with col2:
    if st.button("✨ Features"):
        st.session_state.page = "Features"

with col3:
    if st.button("🧰 Tools"):
        st.session_state.page = "Tools"

with col4:
    if st.button("📤 Upload"):
        st.session_state.page = "Upload"

# =========================
# HOME PAGE
# =========================
if st.session_state.page == "Home":

    st.markdown("<div class='center-box'>", unsafe_allow_html=True)

    st.title("Create Stunning Images with AI")
    st.write("Remove objects, enhance photos, and edit like a pro.")

    st.image("logo.png", width=200)

    st.subheader("🚀 Powerful AI Tools")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("<div class='tool-card'>🎨 Background Edit<br><b>Fast</b></div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='tool-card'>✨ Enhancement<br><b>HD Quality</b></div>", unsafe_allow_html=True)

    with c3:
        st.markdown("<div class='tool-card'>🧍 Object Removal<br><b>Smart</b></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# FEATURES PAGE
# =========================
elif st.session_state.page == "Features":

    st.title("✨ Features")

    st.write("""
    ✔ Background Change  
    ✔ Image Enhancement  
    ✔ Auto Person Removal  
    ✔ Background Removal  
    ✔ Blur Tool  
    ✔ Manual Object Eraser  
    """)

# =========================
# UPLOAD PAGE
# =========================
elif st.session_state.page == "Upload":

    uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        st.session_state.image = Image.open(uploaded_file).convert("RGB")
        st.image(st.session_state.image)

# =========================
# TOOLS PAGE
# =========================
elif st.session_state.page == "Tools":

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

    if "image" not in st.session_state:
        st.warning("⚠ Please upload image first from Upload tab")
    else:
        image = st.session_state.image

        # ================= NORMAL TOOLS =================
        if tool == "🎨 Background Change":
            color_hex = st.color_picker("Pick Color", "#00ffaa")
            color = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))

            if st.button("Apply"):
                arr = np.array(image)
                mask = np.mean(arr, axis=2) > 200
                arr[mask] = color
                result = Image.fromarray(arr)
                st.image(result)

        elif tool == "✨ Enhance Image":
            if st.button("Enhance"):
                result = image.filter(ImageFilter.SHARPEN)
                st.image(result)

        elif tool == "🧍 Auto Person Remove":
            if st.button("Remove"):
                mask_img = remove(image)
                mask = np.array(mask_img)
                alpha = mask[:, :, 3]
                _, binary = cv2.threshold(alpha, 10, 255, cv2.THRESH_BINARY)
                result = cv2.inpaint(np.array(image), binary, 3, cv2.INPAINT_TELEA)
                st.image(result)

        elif tool == "🌄 Background Removal":
            if st.button("Remove BG"):
                out = remove(image.convert("RGBA"))
                st.image(out)

        # ================= HTML TOOLS (UNCHANGED) =================
        elif tool == "✨ Blur Object Tool":
            st.subheader("Blur Tool")
            components.html("<h3>Use your existing blur tool HTML here</h3>", height=400)

        elif tool == "🖌 Manual Object Eraser":
            st.subheader("Manual Eraser")
            components.html("<h3>Use your existing eraser HTML here</h3>", height=400)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("© 2026 AI Image Studio")
