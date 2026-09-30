from pathlib import Path

import requests

from .config import get_settings


settings = get_settings()

PANELS_DIR = Path("static/panels")
PANELS_DIR.mkdir(parents=True, exist_ok=True)


GENERATE_URL = (
    "https://gateway.pixazo.ai/"
    "flux-1-schnell/v1/getData"
)


def generate_image(prompt, filename="comic_panel.png"):

    file_path = PANELS_DIR / filename

    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
       "Ocp-Apim-Subscription-Key": settings.PIXAZO_API_KEY.strip()
    }

    data = {
        "prompt": prompt,
        "num_steps": 4,
        "seed": 15,
        "height": 512,
        "width": 512
    }

    print(f"Generating Pixazo image for: {prompt}")

    try:

        response = requests.post(
            GENERATE_URL,
            json=data,
            headers=headers,
            timeout=120
        )

        print("Pixazo response:", response.text)

        response.raise_for_status()

        result = response.json()

        # Pixazo returns the generated image URL
        image_url = result.get("output")

        if isinstance(image_url, dict):
            image_url = image_url.get("media_url")

            if isinstance(image_url, list):
                image_url = image_url[0]

        if not image_url:
            print("No image URL received.")
            return None

        image_response = requests.get(
            image_url,
            timeout=120
        )

        image_response.raise_for_status()

        file_path.write_bytes(
            image_response.content
        )

        print(
            f"Pixazo image generated successfully: "
            f"{file_path}"
        )

        return str(file_path)

    except Exception as error:

        print(
            f"Pixazo image generation failed: {error}"
        )

        return None