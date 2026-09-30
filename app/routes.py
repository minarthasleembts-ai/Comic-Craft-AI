import asyncio

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pathlib import Path
from datetime import datetime

from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_image
from .exporters import save_pdf


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@router.post("/generate", response_class=HTMLResponse)
async def generate_comic(
    request: Request,
    prompt: str = Form(...),
    character: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):

    # Generate the 5-panel comic outline
    outline = generate_outline(
        prompt,
        character,
        setting,
        tone,
        art_style
    )

    # Generate story content
    story = generate_story(outline)

    # Store generated image paths
    image_paths = []

    # Generate each panel one by one
    for panel in outline:

        panel_number = panel.get("panel", 1)

        filename = f"panel_{panel_number}.png"

        image_path = None

        # Try each image up to 3 times
        for attempt in range(3):

            print(
                f"Generating Panel {panel_number} "
                f"(Attempt {attempt + 1}/3)"
            )

            image_path = await asyncio.to_thread(
                generate_image,
                panel.get(
                    "image_prompt",
                    panel.get(
                        "scene_description",
                        ""
                    )
                ),
                filename
            )

            # Stop retrying if successful
            if image_path:

                print(
                    f"Panel {panel_number} generated successfully."
                )

                break

            print(
                f"Panel {panel_number} failed."
            )

            if attempt < 2:

                print(
                    f"Retrying Panel {panel_number}..."
                )

        # Store image path
        image_paths.append(image_path)

    # Show comic preview
    return templates.TemplateResponse(
        request=request,
        name="comic_preview.html",
        context={
            "outline": outline,
            "story": story,
            "image_paths": image_paths
        }
    )


@router.post("/export")
async def export_comic(
    request: Request,
    image_paths: list[str] = Form(...),
    titles: list[str] = Form([]),
    narrations: list[str] = Form([]),
    dialogues: list[str] = Form([])
):

    # Create PDF
    pdf_path = save_pdf(
        image_paths=image_paths,
        titles=titles,
        narrations=narrations,
        dialogues=dialogues
    )

    # Show export success page
    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={
            "pdf_path": pdf_path
        }
    )


@router.post(
    "/feedback",
    response_class=HTMLResponse
)
async def submit_feedback(
    request: Request,
    feedback: str = Form(...)
):

    feedback = feedback.strip()

    feedback_file = Path(
        "feedback.txt"
    )

    with feedback_file.open(
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            f"\n[{datetime.now()}]\n"
        )

        file.write(
            f"{feedback}\n"
        )

        file.write(
            "-" * 60 + "\n"
        )

    # Show feedback success page
    return templates.TemplateResponse(
        request=request,
        name="feedback_success.html",
        context={}
    )