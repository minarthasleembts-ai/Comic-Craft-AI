from pathlib import Path
import base64
import requests

from .config import get_settings


settings = get_settings()

PANELS_DIR = Path("static/panels")
PANELS_DIR.mkdir(parents=True, exist_ok=True)

MODEL = "@cf/black-forest-labs/flux-1-schnell"


def generate_all_images(outline):

    print("Generating 5 comic panels with Cloudflare AI...")

    image_paths = []

    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{settings.CLOUDFLARE_ACCOUNT_ID}/ai/run/"
        f"{MODEL}"
    )

    headers = {
        "Authorization": (
            f"Bearer {settings.CLOUDFLARE_API_TOKEN}"
        ),
        "Content-Type": "application/json"
    }

    for index, panel in enumerate(outline):

        panel_number = panel.get(
            "panel",
            index + 1
        )

        scene = panel.get(
            "image_prompt",
            panel.get(
                "scene_description",
                ""
            )
        )

        prompt = f"""
Create a single complete comic illustration.

Panel {panel_number}

Scene:
{scene}

Style:
hand-drawn coloured comic illustration,
clean ink outlines,
pencil sketch details,
storybook artwork,
soft natural colours,
expressive characters,
cinematic lighting,
detailed background,
2D illustration.

IMPORTANT:
Create ONLY ONE complete scene.
Fill the entire image with the scene.
Do not create multiple panels.
Do not split the image.
Do not create a collage.
Do not create half scenes.

Avoid:
3D render,
plastic,
toy,
doll,
photorealistic style,
text,
speech bubbles,
captions,
watermarks.
"""

        print(
            f"Generating Panel {panel_number}..."
        )

        data = {
            "prompt": prompt,
            "steps": 4
        }

        try:

            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=120
            )

            response.raise_for_status()

            result = response.json()

            image_base64 = result["result"]["image"]

            image_data = base64.b64decode(
                image_base64
            )

            filename = (
                f"panel_{panel_number}.png"
            )

            panel_path = (
                PANELS_DIR / filename
            )

            panel_path.write_bytes(
                image_data
            )

            image_paths.append(
                str(panel_path)
            )

            print(
                f"Panel {panel_number} saved."
            )

        except Exception as error:

            print(
                f"Panel {panel_number} failed: "
                f"{error}"
            )

            image_paths.append(None)

    return image_paths