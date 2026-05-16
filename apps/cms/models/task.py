from django.db import models
from django.utils.text import slugify


class Task(models.Model):
    STATUS_CHOICES = [
        ("backlog", "Backlog"),
        ("todo", "Todo"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
        ("canceled", "Canceled"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True, blank=True)

    code = models.CharField(max_length=40, unique=True, blank=True)

    description = models.TextField(blank=True)

    location = models.CharField(max_length=180, blank=True)
    department = models.CharField(max_length=120, blank=True)

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="todo",
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium",
    )

    assigned_to = models.CharField(max_length=160, blank=True)

    start_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)

    checklist = models.JSONField(default=list, blank=True)
    attachments = models.JSONField(default=list, blank=True)

    is_public = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-due_date", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if not self.code:
            last_id = Task.objects.count() + 1
            self.code = f"TASK-{last_id:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title