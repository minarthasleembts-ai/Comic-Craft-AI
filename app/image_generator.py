from pathlib import Path
import time

from PIL import Image, ImageDraw, ImageFont
from huggingface_hub import InferenceClient

from .config import get_settings


settings = get_settings()

PANELS_DIR = Path("static/panels")
PANELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

MODEL = "black-forest-labs/FLUX.1-schnell"

client = InferenceClient(
    api_key=settings.HF_API_KEY
)


def create_fallback_image(
    prompt,
    file_path
):
    """
    Creates a local comic-style placeholder
    when Hugging Face image generation is unavailable.
    """

    width = 768
    height = 768

    image = Image.new(
        "RGB",
        (width, height),
        "white"
    )

    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype(
            "DejaVuSans.ttf",
            28
        )

        small_font = ImageFont.truetype(
            "DejaVuSans.ttf",
            20
        )

    except Exception:

        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Comic border
    draw.rectangle(
        [10, 10, width - 10, height - 10],
        outline="black",
        width=8
    )

    # Header
    draw.rectangle(
        [25, 25, width - 25, 100],
        fill="black"
    )

    draw.text(
        (45, 45),
        "COMIC CRAFT",
        fill="white",
        font=font
    )

    # Main comic area
    draw.rectangle(
        [40, 130, width - 40, 570],
        outline="black",
        width=5
    )

    # Simple comic illustration
    draw.ellipse(
        [270, 210, 500, 440],
        outline="black",
        width=6
    )

    draw.arc(
        [325, 275, 445, 385],
        20,
        160,
        fill="black",
        width=5
    )

    draw.ellipse(
        [330, 285, 350, 305],
        fill="black"
    )

    draw.ellipse(
        [420, 285, 440, 305],
        fill="black"
    )

    # Prompt text
    text = prompt[:180]

    draw.text(
        (55, 610),
        "AI COMIC PANEL",
        fill="black",
        font=font
    )

    draw.text(
        (55, 660),
        text,
        fill="black",
        font=small_font
    )

    image.save(file_path)

    print(
        f"Fallback image created: {file_path}"
    )

    return str(file_path)


def generate_image(
    prompt,
    filename="comic_panel.png"
):

    file_path = PANELS_DIR / filename

    print(
        f"Generating Hugging Face image for: {prompt}"
    )

    try:

        image = client.text_to_image(
            prompt=prompt,
            model=MODEL,
            width=512,
            height=512
        )

        image.save(file_path)

        print(
            f"Image generated successfully: "
            f"{file_path}"
        )

        return str(file_path)

    except Exception as error:

        print(
            f"Hugging Face unavailable: {error}"
        )

        print(
            "Using local fallback image..."
        )

        return create_fallback_image(
            prompt,
            file_path
        )