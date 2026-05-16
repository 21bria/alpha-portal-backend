from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model

User = get_user_model()

from apps.cms.utils.media import (
    media_upload_path,
    media_thumbnail_path,
    make_thumbnail,
)

class MediaType(models.TextChoices):
    IMAGE = "IMAGE", "Image"
    VIDEO = "VIDEO", "Video"


class MediaCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "media_categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class MediaAlbum(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)

    description = models.TextField(blank=True, null=True)

    cover = models.ForeignKey(
        "Media",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="album_covers",
    )

    is_public = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="media_albums",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "media_albums"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

class Media(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    type = models.CharField(
        max_length=10,
        choices=MediaType.choices,
        default=MediaType.IMAGE,
    )

    file = models.FileField(
        upload_to=media_upload_path
    )
    thumbnail = models.ImageField(
        upload_to=media_thumbnail_path,
        blank=True,
        null=True
    )
    
    mime_type = models.CharField(max_length=100, blank=True, null=True)
    size = models.BigIntegerField(blank=True, null=True)

    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)

    duration = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Video duration in seconds",
    )

    alt_text = models.CharField(max_length=255, blank=True, null=True)
    caption = models.TextField(blank=True, null=True)

    is_public = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    category = models.ForeignKey(
        MediaCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="media_items",
    )

    albums = models.ManyToManyField(
        MediaAlbum,
        through="MediaAlbumItem",
        blank=True,
        related_name="media_items",
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="media_items",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "media"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or self.file.name
    
    def save(self, *args, **kwargs):
        if self.file:
            self.size = self.file.size

        if self.file and self.type == MediaType.IMAGE:
            try:
                
                self.file.seek(0)

                image = Image.open(self.file)

                if image.mode != "RGB":
                    image = image.convert("RGB")

                # resize jika terlalu besar
                max_width = 1920

                if image.width > max_width:
                    ratio = max_width / float(image.width)

                    height = int(image.height * ratio)

                    image = image.resize(
                        (max_width, height),
                        Image.LANCZOS
                    )

                self.width = image.width
                self.height = image.height
                self.mime_type = "image/webp"

                # compress main image
                output = BytesIO()

                image.save(
                    output,
                    format="WEBP",
                    quality=75,
                    optimize=True,
                )

                output.seek(0)

                import os

                name, _ = os.path.splitext(self.file.name)

                self.file.save(
                    f"{name}.webp",
                    ContentFile(output.read()),
                    save=False,
                )

                self.size = self.file.size

                # thumbnail
                if not self.thumbnail:
                    self.file.seek(0)

                    thumb_name, thumb_file = make_thumbnail(self.file)

                    self.thumbnail.save(
                        thumb_name,
                        thumb_file,
                        save=False,
                    )

            except Exception:
                pass

        super().save(*args, **kwargs)

class MediaAlbumItem(models.Model):
    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        related_name="album_items",
    )

    album = models.ForeignKey(
        MediaAlbum,
        on_delete=models.CASCADE,
        related_name="album_items",
    )

    position = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "media_album_items"
        ordering = ["position", "-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["media", "album"],
                name="unique_media_album_item",
            )
        ]

    def __str__(self):
        return f"{self.media} - {self.album}"