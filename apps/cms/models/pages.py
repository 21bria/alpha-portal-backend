# apps/cms/models.py
from django.db import models
from django.utils.text import slugify


class Page(models.Model):
    PAGE_TYPE_CHOICES = [
        ("company", "Company"),
        ("sustainability", "Sustainability"),
        ("project", "Project"),
        ("career", "Career"),
        ("document", "Document"),
        ("custom", "Custom"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    page_type = models.CharField(max_length=50, choices=PAGE_TYPE_CHOICES, default="custom")
    subtitle = models.TextField(blank=True)
    description = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to="pages/hero/", blank=True, null=True)

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


class PageSection(models.Model):
    SECTION_TYPE_CHOICES = [
        ("hero", "Hero"),
        ("landing_feature", "Landing Feature"),
        ("content", "Content"),
        ("split_content", "Split Content"),
        ("structured_content", "Structured Content"),
        ("project_location", "Project Location"),
        ("image", "Image"),
        ("cards", "Cards"),
        ("values", "Values"),
        ("quote", "Quote"),
        ("gallery", "Gallery"),
        ("cta", "CTA"),
    ]
    IMAGE_POSITION_CHOICES = [
        ("top", "Top"),
        ("bottom", "Bottom"),
        ("left", "Left"),
        ("right", "Right"),
        ("background", "Background"),
    ]


    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="sections")
    section_type = models.CharField(max_length=50, choices=SECTION_TYPE_CHOICES)
    eyebrow = models.CharField(max_length=120,blank=True)
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.TextField(blank=True)
    content = models.TextField(blank=True)

    image = models.ImageField(upload_to="pages/sections/", blank=True, null=True)
    image_alt = models.CharField(max_length=255, blank=True)
    image_position = models.CharField(max_length=20, choices=IMAGE_POSITION_CHOICES,default="top")
    
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
        return f"{self.page.title} - {self.section_type}"