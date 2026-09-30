from pathlib import Path
import time

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


def generate_image(
    prompt,
    filename="comic_panel.png"
):

    file_path = PANELS_DIR / filename

    print(
        f"Generating Hugging Face image for: {prompt}"
    )

    for attempt in range(3):

        try:

            print(
                f"Image generation attempt "
                f"{attempt + 1}/3"
            )

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
                f"Hugging Face image generation failed "
                f"on attempt {attempt + 1}: {error}"
            )

            if attempt < 2:

                print(
                    "Waiting before retry..."
                )

                time.sleep(5)

    print(
        f"Failed to generate image: {filename}"
    )

    return None