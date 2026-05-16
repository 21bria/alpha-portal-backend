# apps/cms/models/news.py
from django.db import models
from django.utils.text import slugify
from apps.cms.utils.images import make_thumbnail

class NewsCategory(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class NewsTag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class NewsArticle(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("archived", "Archived"),
    ]

    category = models.ForeignKey(
        NewsCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="articles"
    )

    tags = models.ManyToManyField(
        NewsTag,
        blank=True,
        related_name="articles"
    )

    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True, blank=True)

    excerpt = models.TextField(blank=True)
    content = models.TextField()

    cover_image = models.ImageField(upload_to="news/cover/", blank=True, null=True)
    cover_thumbnail = models.ImageField(upload_to="news/cover/thumbs/", blank=True, null=True)

    author_name = models.CharField(max_length=120, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )

    is_featured = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=True)

    published_at = models.DateTimeField(blank=True, null=True)

    view_count = models.PositiveIntegerField(default=0)
    reading_time = models.PositiveIntegerField(default=1)

    seo_title = models.CharField(max_length=200, blank=True)
    seo_description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.cover_image and not self.cover_thumbnail:
            thumb_name, thumb_file = make_thumbnail(
                self.cover_image
            )

            self.cover_thumbnail.save(
                thumb_name,
                thumb_file,
                save=False
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class NewsTopic(models.Model):
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True)

    subtitle = models.TextField(blank=True)

    category = models.ForeignKey(
        NewsCategory, on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="topics",
    )

    tags = models.ManyToManyField(
        NewsTag,
        blank=True,
        related_name="topics",
    )

    cover_image = models.ImageField(
        upload_to="news/topics/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title