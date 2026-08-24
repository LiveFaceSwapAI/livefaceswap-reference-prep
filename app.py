from io import BytesIO

import streamlit as st
from PIL import Image, UnidentifiedImageError

from livefaceswap_reference_prep import prepare_reference


MAX_UPLOAD_BYTES = 20 * 1024 * 1024

st.set_page_config(
    page_title="LiveFaceSwap Reference Image Prep",
    page_icon="🖼️",
    layout="centered",
)

st.title("LiveFaceSwap Reference Image Prep")
st.write(
    "Prepare an authorized portrait reference by normalizing its orientation, "
    "cropping it to a square, and exporting a clean RGB PNG."
)

uploaded = st.file_uploader("Portrait image", type=["jpg", "jpeg", "png", "webp"])
size = st.selectbox("Output size", [512, 768, 1024], index=2)
focus_x = st.slider("Horizontal focus", 0.0, 1.0, 0.5, 0.01)
focus_y = st.slider("Vertical focus", 0.0, 1.0, 0.42, 0.01)

if uploaded is not None:
    if uploaded.size > MAX_UPLOAD_BYTES:
        st.error("Please use an image smaller than 20 MB.")
    else:
        try:
            with Image.open(uploaded) as source:
                prepared = prepare_reference(source, size, focus_x, focus_y)

            output = BytesIO()
            prepared.save(output, format="PNG", optimize=True)
            output_bytes = output.getvalue()

            st.image(prepared, caption=f"Prepared {size} × {size} RGB PNG")
            st.download_button(
                "Download prepared PNG",
                data=output_bytes,
                file_name="livefaceswap-reference.png",
                mime="image/png",
            )
        except (UnidentifiedImageError, OSError, ValueError) as error:
            st.error(f"The image could not be prepared: {error}")

st.caption(
    "This utility does not perform face swapping. Only process images you own or have permission to use."
)
st.markdown(
    "[LiveFaceSwap AI](https://livefaceswap.ai/) · "
    "[Source code](https://github.com/LiveFaceSwapAI/livefaceswap-reference-prep)"
)
