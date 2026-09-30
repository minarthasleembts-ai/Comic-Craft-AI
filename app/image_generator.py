from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont


PANELS_DIR = Path("static/panels")
PANELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def get_font(size, bold=False):

    possible_fonts = [
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    ]

    for font_path in possible_fonts:

        try:
            return ImageFont.truetype(
                font_path,
                size
            )

        except Exception:
            pass

    return ImageFont.load_default()


def draw_text_box(
    draw,
    text,
    x,
    y,
    width,
    font
):

    words = text.split()
    lines = []
    current = ""

    for word in words:

        test = (
            current + " " + word
        ).strip()

        if draw.textlength(
            test,
            font=font
        ) <= width:

            current = test

        else:

            if current:
                lines.append(current)

            current = word

    if current:
        lines.append(current)

    line_height = 28

    for index, line in enumerate(lines[:6]):

        draw.text(
            (
                x,
                y + index * line_height
            ),
            line,
            fill="black",
            font=font
        )


def draw_character(
    draw,
    center_x,
    center_y,
    panel_number
):

    # Head
    draw.ellipse(
        [
            center_x - 75,
            center_y - 130,
            center_x + 75,
            center_y + 20
        ],
        fill="orange",
        outline="black",
        width=5
    )

    # Ears
    draw.polygon(
        [
            (center_x - 65, center_y - 100),
            (center_x - 105, center_y - 160),
            (center_x - 25, center_y - 125)
        ],
        fill="orange",
        outline="black"
    )

    draw.polygon(
        [
            (center_x + 65, center_y - 100),
            (center_x + 105, center_y - 160),
            (center_x + 25, center_y - 125)
        ],
        fill="orange",
        outline="black"
    )

    # Eyes
    draw.ellipse(
        [
            center_x - 45,
            center_y - 75,
            center_x - 25,
            center_y - 55
        ],
        fill="black"
    )

    draw.ellipse(
        [
            center_x + 25,
            center_y - 75,
            center_x + 45,
            center_y - 55
        ],
        fill="black"
    )

    # Nose
    draw.ellipse(
        [
            center_x - 10,
            center_y - 35,
            center_x + 10,
            center_y - 15
        ],
        fill="black"
    )

    # Body
    draw.ellipse(
        [
            center_x - 85,
            center_y,
            center_x + 85,
            center_y + 180
        ],
        fill="orange",
        outline="black",
        width=5
    )

    # Tail
    draw.arc(
        [
            center_x + 55,
            center_y + 30,
            center_x + 190,
            center_y + 170
        ],
        250,
        100,
        fill="orange",
        width=18
    )


def create_comic_panel(
    prompt,
    panel_number,
    file_path
):

    width = 768
    height = 768

    image = Image.new(
        "RGB",
        (width, height),
        "white"
    )

    draw = ImageDraw.Draw(image)

    title_font = get_font(
        30,
        bold=True
    )

    text_font = get_font(
        20
    )

    # Different background for each panel
    backgrounds = [
        "#DFF3FF",
        "#E8F8E0",
        "#FFF1CC",
        "#EDE0FF",
        "#FFE1E1"
    ]

    background = backgrounds[
        (panel_number - 1) % len(backgrounds)
    ]

    draw.rectangle(
        [0, 0, width, height],
        fill=background
    )

    # Outer comic border
    draw.rectangle(
        [12, 12, width - 12, height - 12],
        outline="black",
        width=8
    )

    # Header
    draw.rectangle(
        [30, 30, width - 30, 95],
        fill="white",
        outline="black",
        width=4
    )

    draw.text(
        (50, 48),
        f"PANEL {panel_number}",
        fill="black",
        font=title_font
    )

    # Decorative environment
    draw.rectangle(
        [40, 430, width - 40, 680],
        fill="#B8E0A5",
        outline="black",
        width=4
    )

    # Trees
    for x in [100, 650]:

        draw.rectangle(
            [x - 12, 270, x + 12, 460],
            fill="#704214",
            outline="black"
        )

        draw.ellipse(
            [x - 70, 200, x + 70, 330],
            fill="#58A957",
            outline="black",
            width=4
        )

    # Character position changes by panel
    positions = [
        (380, 360),
        (300, 360),
        (470, 360),
        (350, 360),
        (400, 360)
    ]

    character_x, character_y = positions[
        (panel_number - 1) % 5
    ]

    draw_character(
        draw,
        character_x,
        character_y,
        panel_number
    )

    # Speech bubble
    bubble_x = 480
    bubble_y = 145

    draw.ellipse(
        [
            bubble_x,
            bubble_y,
            720,
            255
        ],
        fill="white",
        outline="black",
        width=4
    )

    short_text = (
        "What an adventure!"
        if panel_number == 1
        else
        "Something mysterious!"
        if panel_number == 2
        else
        "I found the secret!"
        if panel_number == 3
        else
        "The magic is growing!"
        if panel_number == 4
        else
        "Adventure continues!"
    )

    draw.text(
        (
            bubble_x + 25,
            bubble_y + 35
        ),
        short_text,
        fill="black",
        font=text_font
    )

    # Scene description
    draw.rectangle(
        [40, 690, width - 40, 735],
        fill="white",
        outline="black",
        width=2
    )

    scene_text = " ".join(
        prompt.split()
    )

    if len(scene_text) > 85:
        scene_text = scene_text[:85] + "..."

    draw.text(
        (55, 702),
        scene_text,
        fill="black",
        font=get_font(16)
    )

    image.save(
        file_path
    )

    print(
        f"Local comic panel created: {file_path}"
    )

    return str(file_path)


def generate_image(
    prompt,
    filename="comic_panel.png"
):

    file_path = (
        PANELS_DIR / filename
    )

    print(
        f"Creating comic panel locally: {filename}"
    )

    return create_comic_panel(
        prompt,
        int(
            Path(filename).stem.split("_")[-1]
        )
        if "_" in filename
        else 1,
        file_path
    )