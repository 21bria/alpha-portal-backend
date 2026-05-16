# apps/cms/models.py
from django.db import models
from apps.cms.models.pages import Page

class NavigationMenu(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class NavigationItem(models.Model):
    menu = models.ForeignKey(
        NavigationMenu,
        related_name="items",
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255, blank=True)

    page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children"
    )

    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.title

    @property
    def final_url(self):
        if self.url:
            return self.url

        if self.page:
            return f"/{self.page.slug}"

        return "#"