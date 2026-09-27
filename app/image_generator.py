from pathlib import Path
import requests

from .config import get_settings

settings = get_settings()

PANELS_DIR = Path("static/panels")
PANELS_DIR.mkdir(parents=True, exist_ok=True)


def generate_image(prompt, filename="comic_panel.png"):
    file_path = PANELS_DIR / filename

    url = "https://gen.pollinations.ai/image/" + requests.utils.quote(prompt)

    response = requests.get(
        url,
        params={"model": "flux"},
        headers={
            "Authorization": f"Bearer {settings.POLLINATIONS_API_KEY}"
        },
        timeout=120
    )

    response.raise_for_status()

    with open(file_path, "wb") as file:
        file.write(response.content)

    return str(file_path)
