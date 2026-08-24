from io import BytesIO

import streamlit as st
from PIL import Image, UnidentifiedImageError

from livefaceswap_reference_prep import prepare_reference


MAX_UPLOAD_BYTES = 20 * 1024 * 1024
PRODUCT_URL = "https://livefaceswap.ai/"
SOURCE_URL = "https://github.com/LiveFaceSwapAI/livefaceswap-reference-prep"
WORKFLOW_IMAGE = "assets/reference-prep-workflow.svg"

st.set_page_config(
    page_title="LiveFaceSwap AI – Face Swap Reference Image Prep",
    page_icon="🎭",
    layout="centered",
)

st.title("LiveFaceSwap AI: Prepare a Reference Image for Face Swap")
st.markdown(
    "A live face swap starts with a usable reference portrait. This free tool "
    "normalizes rotation and color, lets you center the face in a square crop, "
    "and exports a clean PNG for an authorized real-time face swap workflow."
)
st.info(
    "This page prepares the reference image. It does not replace a face, train "
    "an identity model, or run the face swap itself."
)

st.subheader("Prepare your reference portrait")
st.write(
    "Upload a JPG, PNG, or WebP portrait that you own or have permission to use. "
    "Adjust the focus only when the face is not centered in the preview."
)

uploaded = st.file_uploader(
    "Portrait reference image",
    type=["jpg", "jpeg", "png", "webp"],
    help="Maximum file size: 20 MB. Use a clear portrait with the face visible.",
)
size = st.selectbox(
    "Square PNG output size",
    [512, 768, 1024],
    index=2,
    help="1024 keeps the largest output; choose a smaller size when your next tool requires it.",
)
focus_x = st.slider(
    "Horizontal face position",
    0.0,
    1.0,
    0.5,
    0.01,
    help="Move left or right to keep the face inside the square crop.",
)
focus_y = st.slider(
    "Vertical face position",
    0.0,
    1.0,
    0.42,
    0.01,
    help="Move up or down to keep the head and facial features inside the crop.",
)

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

            st.success("Reference image ready for the next step in your face swap workflow.")
            st.image(prepared, caption=f"Prepared {size} × {size} RGB PNG")
            st.download_button(
                "Download face swap reference PNG",
                data=output_bytes,
                file_name="livefaceswap-reference.png",
                mime="image/png",
                type="primary",
            )
        except (UnidentifiedImageError, OSError, ValueError) as error:
            st.error(f"The image could not be prepared: {error}")

st.divider()
st.subheader("How this helps a live face swap workflow")
st.image(
    WORKFLOW_IMAGE,
    caption="Authorized portrait → normalized square PNG → LiveFaceSwap AI reference",
    width="stretch",
)
st.markdown(
    """
1. **Choose an authorized portrait.** A clear, well-lit face is easier to position than a distant or obstructed photo.
2. **Standardize the file here.** The tool applies EXIF orientation, converts to RGB, square-crops around your chosen focus, and resizes the result.
3. **Download the PNG.** Use the prepared file as the reference portrait in LiveFaceSwap AI or another compatible workflow.

Preparing the file first removes avoidable differences in rotation, color mode, framing, and dimensions before the face swap model receives it.
"""
)

st.subheader("What the tool changes")
st.markdown(
    """
- Corrects camera orientation stored in EXIF metadata
- Converts palette, grayscale, or transparent sources to RGB
- Creates an adjustable square crop around the face
- Exports a consistent 512, 768, or 1024 pixel PNG
- Removes source metadata from the generated file
"""
)

with st.expander("Frequently asked questions"):
    st.markdown(
        """
**Does this page perform a face swap?**

No. It prepares the portrait used by a face swap workflow; the actual face swap runs in a compatible application.

**Does it train or upload a face model?**

No. The operation is deterministic image processing: orientation, RGB conversion, crop, resize, and PNG export.

**Which size should I choose?**

Use 1024 for the largest available reference. Choose 512 or 768 when the next tool requires a smaller input.
"""
    )

st.caption(
    "Only process portraits you own or have permission to use. Do not use reference images for impersonation, fraud, harassment, or deceptive activity."
)
st.markdown(
    f"[LiveFaceSwap AI]({PRODUCT_URL}) · [Official source]({SOURCE_URL}) · "
    "[Python package](https://pypi.org/project/livefaceswap-reference-prep/)"
)
