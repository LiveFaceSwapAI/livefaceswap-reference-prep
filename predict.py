from pathlib import Path
from typing import Literal

from cog import BasePredictor, Input, Path as CogPath

from image_prep import prepare_reference_image


class Predictor(BasePredictor):
    def predict(
        self,
        image: CogPath = Input(description="Authorized portrait reference image (JPG, PNG, or WebP)."),
        size: Literal[512, 768, 1024] = Input(
            default=1024,
            description="Square PNG output size in pixels."
        ),
        focus_x: float = Input(
            default=0.5,
            ge=0.0,
            le=1.0,
            description="Horizontal crop focus: 0 is left and 1 is right."
        ),
        focus_y: float = Input(
            default=0.42,
            ge=0.0,
            le=1.0,
            description="Vertical crop focus: 0 is top and 1 is bottom."
        ),
    ) -> CogPath:
        output = Path("/tmp/livefaceswap-reference.png")
        prepare_reference_image(Path(image), output, int(size), focus_x, focus_y)
        return CogPath(output)

