from pathlib import Path

from huggingface_hub import InferenceClient

from .config import get_settings


settings = get_settings()


PANELS_DIR = Path("static/panels")
PANELS_DIR.mkdir(parents=True, exist_ok=True)


client = InferenceClient(
    api_key=settings.HF_API_KEY,
    provider="auto"
)


def generate_image(
    prompt,
    filename="comic_panel.png"
):

    file_path = PANELS_DIR / filename

    image = client.text_to_image(
        prompt=prompt,
        model="black-forest-labs/FLUX.1-schnell"
    )

    image.save(file_path)

    return str(file_path)