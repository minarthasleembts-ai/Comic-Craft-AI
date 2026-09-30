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

    outline = generate_outline(
        prompt,
        character,
        setting,
        tone,
        art_style
    )

    story = generate_story(outline)

    async def generate_panel(panel):

        panel_number = panel.get("panel", 1)

        filename = f"panel_{panel_number}.png"

        image_path = await asyncio.to_thread(
            generate_image,
            panel.get(
                "image_prompt",
                panel.get("scene_description", "")
            ),
            filename
        )

        return image_path

    image_paths = await asyncio.gather(
        *[
            generate_panel(panel)
            for panel in outline
        ]
    )

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

    pdf_path = save_pdf(
        image_paths=image_paths,
        titles=titles,
        narrations=narrations,
        dialogues=dialogues
    )

    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={
            "pdf_path": pdf_path
        }
    )


@router.post("/feedback", response_class=HTMLResponse)
async def submit_feedback(
    request: Request,
    feedback: str = Form(...)
):

    feedback = feedback.strip()

    feedback_file = Path("feedback.txt")

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

    return templates.TemplateResponse(
        request=request,
        name="feedback_success.html",
        context={}
    )