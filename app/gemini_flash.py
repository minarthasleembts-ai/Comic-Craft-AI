import json
import time
from google import genai

from .config import get_settings


settings = get_settings()

client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def generate_outline(
    prompt,
    character,
    setting,
    tone,
    art_style
):

    request = f"""
Create a 5-panel comic outline.

Story prompt: {prompt}

Main character: {character}

Setting: {setting}

Tone: {tone}

Art style: {art_style}

Return ONLY valid JSON.

Format:

[
    {{
        "panel": 1,
        "title": "Panel title",
        "scene_description": "Scene description",
        "image_prompt": "Detailed image prompt"
    }}
]

Create exactly 5 panels.
"""

    models = [
        "gemini-3.7-flash",
        "gemini-3.5-flash-lite",
        "gemini-3.8-flash"
    ]

    last_error = None

    for model in models:

        for attempt in range(2):

            try:

                print(f"Trying Gemini model: {model}")

                response = client.models.generate_content(
                    model=model,
                    contents=request
                )

                text = response.text.strip()

                if text.startswith("```"):
                    text = text.replace("```json", "")
                    text = text.replace("```", "")
                    text = text.strip()

                return json.loads(text)

            except Exception as error:

                last_error = error

                print(
                    f"Gemini error with {model}, "
                    f"attempt {attempt + 1}: {error}"
                )

                time.sleep(2)

    raise last_error