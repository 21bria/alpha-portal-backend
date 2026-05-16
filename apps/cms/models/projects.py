from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    STATUS_CHOICES = [
        ("active", "Active Site"),
        ("development", "Development"),
        ("operational", "Operational"),
        ("exploration", "Exploration"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)

    subtitle = models.TextField(blank=True)
    description = models.TextField(blank=True)
    overview = models.TextField(blank=True)

    location = models.CharField(max_length=200, blank=True)
    province = models.CharField(max_length=100, blank=True)
    commodity = models.CharField(max_length=100, default="Nickel Ore")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="active")

    cover_image = models.ImageField(upload_to="projects/cover/", blank=True, null=True)

    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)

    highlights = models.JSONField(default=list, blank=True)

    seo_title = models.CharField(max_length=200, blank=True)
    seo_description = models.TextField(blank=True)

    is_published = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ProjectSection(models.Model):
    SECTION_TYPE_CHOICES = [
        ("hero", "Hero"),
        ("overview", "Overview"),
        ("content", "Content"),
        ("split_content", "Split Content"),
        ("structured_content", "Structured Content"),
        ("location", "Location"),
        ("map", "Map"),
        ("highlights", "Highlights"),
        ("cards", "Cards"),
        ("gallery", "Gallery"),
        ("quote", "Quote"),

    ]

    IMAGE_POSITION_CHOICES = [
        ("top", "Top"),
        ("bottom", "Bottom"),
        ("left", "Left"),
        ("right", "Right"),
        ("background", "Background"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="sections"
    )

    section_type = models.CharField(max_length=50, choices=SECTION_TYPE_CHOICES)

    eyebrow = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.TextField(blank=True)
    content = models.TextField(blank=True)

    image = models.ImageField(upload_to="projects/sections/", blank=True, null=True)
    image_alt = models.CharField(max_length=255, blank=True)
    image_position = models.CharField(
        max_length=20,
        choices=IMAGE_POSITION_CHOICES,
        default="top"
    )

    data = models.JSONField(default=dict, blank=True)

    primary_button_text = models.CharField(max_length=120, blank=True)
    primary_button_url = models.CharField(max_length=255, blank=True)

    secondary_button_text = models.CharField(max_length=120, blank=True)
    secondary_button_url = models.CharField(max_length=255, blank=True)

    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.project.title} - {self.section_type}"