import os
import uuid
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


def media_upload_path(instance, filename):
    ext = filename.split(".")[-1]

    if instance.type == "VIDEO":
        folder = "uploads/videos"
    else:
        folder = "uploads/images"

    return os.path.join(
        folder,
        f"{uuid.uuid4()}.{ext}"
    )


def media_thumbnail_path(instance, filename):
    return os.path.join(
        "uploads/thumbnails",
        filename
    )


def make_thumbnail(image_field, size=(1200, 675)):
    image = Image.open(image_field)

    if image.mode != "RGB":
        image = image.convert("RGB")

    image.thumbnail(size)

    thumb_io = BytesIO()

    image.save(
        thumb_io,
        format="WEBP",
        quality=80,
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