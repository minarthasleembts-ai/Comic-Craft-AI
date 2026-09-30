from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont, ImageFilter


PANELS_DIR = Path("static/panels")
PANELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def get_font(size, bold=False):

    fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "DejaVuSans-Bold.ttf"
        if bold
        else "DejaVuSans.ttf"
    ]

    for font in fonts:
        try:
            return ImageFont.truetype(font, size)
        except Exception:
            pass

    return ImageFont.load_default()


def gradient_background(
    width,
    height,
    top_color,
    bottom_color
):

    image = Image.new(
        "RGB",
        (width, height)
    )

    pixels = image.load()

    for y in range(height):

        ratio = y / (height - 1)

        r = int(
            top_color[0] * (1 - ratio)
            + bottom_color[0] * ratio
        )

        g = int(
            top_color[1] * (1 - ratio)
            + bottom_color[1] * ratio
        )

        b = int(
            top_color[2] * (1 - ratio)
            + bottom_color[2] * ratio
        )

        for x in range(width):
            pixels[x, y] = (r, g, b)

    return image


def draw_tree(
    draw,
    x,
    ground,
    scale=1.0
):

    trunk_width = int(45 * scale)
    trunk_height = int(300 * scale)

    draw.rectangle(
        [
            x - trunk_width // 2,
            ground - trunk_height,
            x + trunk_width // 2,
            ground
        ],
        fill=(55, 38, 30)
    )

    branches = [
        (-100, -220, 100, -300),
        (80, -250, 170, -330),
        (-40, -280, -130, -360)
    ]

    for x1, y1, x2, y2 in branches:

        draw.line(
            [
                x,
                ground + int(y1 * scale),
                x + int(x2 * scale),
                ground + int(y2 * scale)
            ],
            fill=(48, 32, 27),
            width=max(8, int(18 * scale))
        )

    for dx, dy, size in [
        (-90, -330, 110),
        (20, -350, 140),
        (100, -300, 100),
        (-10, -270, 120)
    ]:

        draw.ellipse(
            [
                x + int((dx - size) * scale),
                ground + int((dy - size) * scale),
                x + int((dx + size) * scale),
                ground + int((dy + size) * scale)
            ],
            fill=(30, 70, 45)
        )


def draw_ground(
    draw,
    width,
    height
):

    draw.rectangle(
        [
            0,
            int(height * 0.70),
            width,
            height
        ],
        fill=(38, 55, 38)
    )

    # grass / vegetation
    for x in range(20, width, 35):

        base = int(height * 0.70)

        draw.line(
            [
                x,
                base + 30,
                x + 10,
                base - 10
            ],
            fill=(65, 95, 55),
            width=4
        )

        draw.line(
            [
                x + 10,
                base + 30,
                x + 25,
                base
            ],
            fill=(55, 85, 48),
            width=3
        )


def draw_fox(
    draw,
    cx,
    cy,
    scale=1.0
):

    # Body
    body_w = int(125 * scale)
    body_h = int(170 * scale)

    draw.ellipse(
        [
            cx - body_w,
            cy,
            cx + body_w,
            cy + body_h
        ],
        fill=(157, 76, 35),
        outline=(45, 28, 20),
        width=max(2, int(4 * scale))
    )

    # Neck
    draw.ellipse(
        [
            cx - int(75 * scale),
            cy - int(70 * scale),
            cx + int(75 * scale),
            cy + int(80 * scale)
        ],
        fill=(170, 83, 38)
    )

    # Head
    head = int(85 * scale)

    draw.ellipse(
        [
            cx - head,
            cy - int(155 * scale),
            cx + head,
            cy + int(5 * scale)
        ],
        fill=(178, 88, 40),
        outline=(45, 28, 20),
        width=max(2, int(4 * scale))
    )

    # Ears
    draw.polygon(
        [
            (
                cx - int(55 * scale),
                cy - int(125 * scale)
            ),
            (
                cx - int(95 * scale),
                cy - int(210 * scale)
            ),
            (
                cx - int(10 * scale),
                cy - int(160 * scale)
            )
        ],
        fill=(150, 70, 35)
    )

    draw.polygon(
        [
            (
                cx + int(55 * scale),
                cy - int(125 * scale)
            ),
            (
                cx + int(95 * scale),
                cy - int(210 * scale)
            ),
            (
                cx + int(10 * scale),
                cy - int(160 * scale)
            )
        ],
        fill=(150, 70, 35)
    )

    # White face
    draw.ellipse(
        [
            cx - int(55 * scale),
            cy - int(85 * scale),
            cx + int(55 * scale),
            cy - int(5 * scale)
        ],
        fill=(225, 205, 175)
    )

    # Eyes
    eye_size = max(3, int(8 * scale))

    draw.ellipse(
        [
            cx - int(38 * scale),
            cy - int(75 * scale),
            cx - int(38 * scale) + eye_size,
            cy - int(75 * scale) + eye_size
        ],
        fill=(20, 15, 12)
    )

    draw.ellipse(
        [
            cx + int(30 * scale),
            cy - int(75 * scale),
            cx + int(30 * scale) + eye_size,
            cy - int(75 * scale) + eye_size
        ],
        fill=(20, 15, 12)
    )

    # Nose
    draw.ellipse(
        [
            cx - int(12 * scale),
            cy - int(35 * scale),
            cx + int(12 * scale),
            cy - int(15 * scale)
        ],
        fill=(25, 18, 15)
    )

    # Tail
    tail_box = int(170 * scale)

    draw.arc(
        [
            cx + int(65 * scale),
            cy + int(30 * scale),
            cx + tail_box,
            cy + int(190 * scale)
        ],
        250,
        110,
        fill=(170, 82, 38),
        width=max(10, int(30 * scale))
    )


def add_atmosphere(
    image,
    panel_number
):

    overlay = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(
        overlay
    )

    width, height = image.size

    # Moon / light source
    if panel_number in [1, 3, 5]:

        draw.ellipse(
            [
                width - 180,
                80,
                width - 70,
                190
            ],
            fill=(255, 235, 170, 210)
        )

    # Light rays
    for i in range(7):

        x = width // 2 + i * 45

        draw.polygon(
            [
                (x, 120),
                (x + 25, 120),
                (x + 170, 650),
                (x + 100, 650)
            ],
            fill=(255, 225, 150, 22)
        )

    overlay = overlay.filter(
        ImageFilter.GaussianBlur(8)
    )

    image = Image.alpha_composite(
        image.convert("RGBA"),
        overlay
    )

    return image.convert("RGB")


def create_comic_panel(
    prompt,
    panel_number,
    file_path
):

    width = 900
    height = 700

    backgrounds = [
        ((18, 32, 48), (80, 115, 82)),
        ((24, 42, 38), (70, 100, 70)),
        ((30, 25, 45), (90, 75, 70)),
        ((20, 35, 30), (95, 85, 55)),
        ((15, 30, 48), (110, 90, 60))
    ]

    top, bottom = backgrounds[
        (panel_number - 1) % len(backgrounds)
    ]

    image = gradient_background(
        width,
        height,
        top,
        bottom
    )

    draw = ImageDraw.Draw(image)

    # Background trees
    draw_tree(
        draw,
        120,
        520,
        1.2
    )

    draw_tree(
        draw,
        780,
        530,
        1.0
    )

    draw_tree(
        draw,
        650,
        520,
        0.75
    )

    draw_ground(
        draw,
        width,
        height
    )

    # Character
    positions = [
        (420, 430),
        (330, 425),
        (500, 420),
        (410, 430),
        (470, 425)
    ]

    cx, cy = positions[
        (panel_number - 1) % 5
    ]

    draw_fox(
        draw,
        cx,
        cy,
        1.05
    )

    # Atmospheric lighting
    image = add_atmosphere(
        image,
        panel_number
    )

    draw = ImageDraw.Draw(image)

    # Cinematic dark overlay at bottom
    overlay = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    overlay_draw = ImageDraw.Draw(
        overlay
    )

    overlay_draw.rectangle(
        [
            0,
            590,
            width,
            height
        ],
        fill=(0, 0, 0, 150)
    )

    image = Image.alpha_composite(
        image.convert("RGBA"),
        overlay
    ).convert("RGB")

    draw = ImageDraw.Draw(image)

    title_font = get_font(
        30,
        bold=True
    )

    body_font = get_font(
        19
    )

    # Panel title
    draw.text(
        (35, 30),
        f"SCENE {panel_number}",
        fill=(245, 235, 210),
        font=title_font
    )

    # Scene text
    scene = " ".join(
        prompt.split()
    )

    if len(scene) > 150:
        scene = scene[:150] + "..."

    wrapped = "\n".join(
        [
            scene[i:i + 70]
            for i in range(
                0,
                len(scene),
                70
            )
        ][:2]
    )

    draw.multiline_text(
        (35, 610),
        wrapped,
        fill=(240, 235, 220),
        font=body_font,
        spacing=7
    )

    # Cinematic border
    draw.rectangle(
        [
            8,
            8,
            width - 8,
            height - 8
        ],
        outline=(220, 205, 175),
        width=5
    )

    image.save(
        file_path,
        quality=95
    )

    print(
        f"Cinematic comic panel created: {file_path}"
    )

    return str(file_path)


def generate_image(
    prompt,
    filename="comic_panel.png"
):

    file_path = (
        PANELS_DIR / filename
    )

    try:

        panel_number = int(
            Path(filename)
            .stem
            .split("_")[-1]
        )

    except Exception:

        panel_number = 1

    return create_comic_panel(
        prompt,
        panel_number,
        file_path
    )