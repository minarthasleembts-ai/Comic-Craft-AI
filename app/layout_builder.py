from pathlib import Path
from PIL import Image, ImageOps


def build_comic_layout(image_paths, output_path="static/panels/comic_layout.png"):
    if not image_paths:
        return None

    images = []

    for image_path in image_paths:
        path = Path(image_path)

        if path.exists():
            image = Image.open(path).convert("RGB")
            images.append(image)

    if not images:
        return None

    width = max(image.width for image in images)
    total_height = sum(image.height for image in images)

    canvas = Image.new("RGB", (width, total_height), "white")

    y = 0

    for image in images:
        canvas.paste(image, (0, y))
        y += image.height

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    canvas.save(output)

    return str(output)