from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
import os


def make_thumbnail(image_field, size=(300, 180)):
    image = Image.open(image_field)

    if image.mode != "RGB":
        image = image.convert("RGB")

    image.thumbnail(size)

    thumb_io = BytesIO()

    image.save(
        thumb_io,
        format="WEBP",
        quality=85,
        optimize=True,
    )

    name, _ = os.path.splitext(image_field.name)

    thumb_name = f"{name}_thumb.webp"

    return thumb_name, ContentFile(thumb_io.getvalue())


def optimize_image(image_field, quality=75, max_width=1920):
    image = Image.open(image_field)

    if image.mode != "RGB":
        image = image.convert("RGB")

    # Resize jika terlalu besar
    if image.width > max_width:
        ratio = max_width / float(image.width)

        height = int(image.height * ratio)

        image = image.resize((max_width, height), Image.LANCZOS)

    output = BytesIO()

    image.save(
        output,
        format="WEBP",
        quality=quality,
        optimize=True,
    )

    name, _ = os.path.splitext(image_field.name)

    optimized_name = f"{name}.webp"

    return optimized_name, ContentFile(output.getvalue())