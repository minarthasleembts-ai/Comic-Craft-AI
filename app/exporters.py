from pathlib import Path
from fpdf import FPDF


EXPORT_DIR = Path("static/exports")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def save_pdf(
    image_paths,
    titles=None,
    narrations=None,
    dialogues=None,
    filename="comic.pdf"
):

    pdf_path = EXPORT_DIR / filename

    titles = titles or []
    narrations = narrations or []
    dialogues = dialogues or []

    pdf = FPDF()

    for index, image_path in enumerate(image_paths):

        if not Path(image_path).exists():
            continue

        pdf.add_page()

        # IMAGE
        pdf.image(
            str(image_path),
            x=10,
            y=10,
            w=190
        )

        # STORY BELOW IMAGE
        # Move cursor to the bottom area of the image
        pdf.set_y(190)

        pdf.set_font("Arial", "B", 14)

        title = ""
        if index < len(titles):
            title = titles[index]

        pdf.multi_cell(
            190,
            8,
            f"Panel {index + 1}: {title}"
        )

        pdf.ln(2)

        pdf.set_font("Arial", "", 11)

        narration = ""
        if index < len(narrations):
            narration = narrations[index]

        if narration:
            pdf.multi_cell(
                190,
                7,
                f"Narration: {narration}"
            )

        pdf.ln(2)

        dialogue = ""
        if index < len(dialogues):
            dialogue = dialogues[index]

        if dialogue:
            pdf.multi_cell(
                190,
                7,
                f"Dialogue: {dialogue}"
            )

    pdf.output(str(pdf_path))

    return str(pdf_path)