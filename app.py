
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
