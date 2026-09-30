from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pathlib import Path
from datetime import datetime

from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_all_images
from .exporters import save_pdf


router = APIRouter()


templates = Jinja2Templates(
    directory="templates"
)


# ==========================================
# HOME PAGE
# ==========================================

@router.get(
    "/",
    response_class=HTMLResponse
)
async def home(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# ==========================================
# GENERATE COMIC
# ==========================================

@router.post(
    "/generate",
    response_class=HTMLResponse
)
async def generate_comic(
    request: Request,

    prompt: str = Form(...),

    character: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...)
):

    print("\n================================")
    print("STARTING COMIC GENERATION")
    print("================================")

    print(f"Prompt: {prompt}")
    print(f"Character: {character}")
    print(f"Setting: {setting}")
    print(f"Tone: {tone}")
    print(f"Art Style: {art_style}")


    # ======================================
    # STEP 1
    # Generate 5-panel outline
    # ======================================

    print("\nGenerating comic outline...")

    outline = generate_outline(
        prompt,
        character,
        setting,
        tone,
        art_style
    )


    print(
        f"Outline generated: "
        f"{len(outline)} panels"
    )


    # ======================================
    # STEP 2
    # Generate story
    # ======================================

    print("\nGenerating story content...")

    story = generate_story(
        outline
    )


    print(
        f"Story generated: "
        f"{len(story)} panels"
    )


    # ======================================
    # STEP 3
    # Generate ALL 5 images
    # using ONE image-generation request
    # ======================================

    print("\n================================")
    print("GENERATING 5-PANEL COMIC IMAGE")
    print("ONE API REQUEST")
    print("================================")


    image_paths = generate_all_images(
        outline
    )


    print("\n================================")
    print("ALL 5 PANEL IMAGES CREATED")
    print("================================")


    # ======================================
    # STEP 4
    # Show comic preview
    # ======================================

    return templates.TemplateResponse(
        request=request,
        name="comic_preview.html",
        context={
            "outline": outline,

            "story": story,

            "image_paths": image_paths,

            "art_style": art_style
        }
    )


# ==========================================
# EXPORT COMIC AS PDF
# ==========================================

@router.post(
    "/export",
    response_class=HTMLResponse
)
async def export_comic(
    request: Request,

    image_paths: list[str] = Form(...),

    titles: list[str] = Form([]),

    narrations: list[str] = Form([]),

    dialogues: list[str] = Form([])
):

    print("\n================================")
    print("EXPORTING COMIC PDF")
    print("================================")


    pdf_path = save_pdf(
        image_paths=image_paths,

        titles=titles,

        narrations=narrations,

        dialogues=dialogues
    )


    print(
        f"PDF created: {pdf_path}"
    )


    return templates.TemplateResponse(
        request=request,

        name="export_success.html",

        context={
            "pdf_path": pdf_path
        }
    )


# ==========================================
# FEEDBACK
# ==========================================

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


    print(
        "Feedback submitted successfully."
    )


    return templates.TemplateResponse(
        request=request,

        name="feedback_success.html",

        context={}
    )