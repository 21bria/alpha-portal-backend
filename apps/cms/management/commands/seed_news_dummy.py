# python manage.py seed_news_dummy --schema=kawi

from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from django_tenants.utils import schema_context

from apps.cms.models.news import (
    NewsArticle,
    NewsCategory,
    NewsTag,
)


class Command(BaseCommand):
    help = "Seed dummy news data with categories, tags, and cover images"

    def add_arguments(self, parser):
        parser.add_argument(
            "--schema",
            type=str,
            default="kawi",
            help="Tenant schema name. Example: kawi",
        )

    def handle(self, *args, **options):
        schema_name = options.get("schema") or "kawi"

        with schema_context(schema_name):
            self.stdout.write(
                self.style.SUCCESS(f"Seeding news dummy data for schema: {schema_name}")
            )
            self.seed()

    def seed(self):
        categories = [
            ("Operations", "operations"),
            ("Sustainability", "sustainability"),
            ("Technology", "technology"),
            ("Corporate", "corporate"),
        ]

        tags = [
            ("Productions", "productions"),
            ("Nickel Ore", "nickel-ore"),
            ("ESG", "esg"),
            ("Digital Mining", "digital-mining"),
        ]

        cover_images = [
            "news/cover/career-2.jpg",
            "news/cover/foto-overview.jpg",
            "news/cover/female-nickel.jpg",
            "news/cover/engineering_discussion.jpg",
        ]

        category_map = self.create_categories(categories)
        tag_map = self.create_tags(tags)
        articles = self.build_articles()

        for index, item in enumerate(articles):
            article, created = NewsArticle.objects.get_or_create(
                slug=item["slug"],
                defaults={
                    "title": item["title"],
                    "excerpt": item["excerpt"],
                    "content": item["content"],
                    "category": category_map[item["category"]],
                    "status": "published",
                    "author_name": "Bria",
                    "published_at": timezone.now(),
                    "reading_time": 2,
                    "seo_title": item["title"],
                    "seo_description": item["excerpt"],
                },
            )

            article.title = item["title"]
            article.excerpt = item["excerpt"]
            article.content = item["content"]
            article.category = category_map[item["category"]]
            article.status = "published"
            article.author_name = "Bria"
            article.published_at = article.published_at or timezone.now()
            article.reading_time = 2
            article.seo_title = item["title"]
            article.seo_description = item["excerpt"]

            article.tags.set([tag_map[tag_slug] for tag_slug in item["tags"]])

            self.set_cover_image(
                article=article,
                image_path=cover_images[index % len(cover_images)],
            )

            article.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created: {article.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated: {article.title}"))

        self.stdout.write(self.style.SUCCESS("20 dummy news articles seeded."))

    def create_categories(self, categories):
        category_map = {}

        for name, slug in categories:
            category, _ = NewsCategory.objects.get_or_create(
                slug=slug,
                defaults={"name": name},
            )
            category_map[slug] = category

        return category_map

    def create_tags(self, tags):
        tag_map = {}

        for name, slug in tags:
            tag, _ = NewsTag.objects.get_or_create(
                slug=slug,
                defaults={"name": name},
            )
            tag_map[slug] = tag

        return tag_map

    def build_articles(self):
        base_articles = [
            {
                "title": "Strengthening ESG initiatives across mining operations",
                "category": "sustainability",
                "tags": ["esg", "nickel-ore"],
            },
            {
                "title": "Digital mining ecosystem integration continues to grow",
                "category": "technology",
                "tags": ["digital-mining", "nickel-ore"],
            },
            {
                "title": "Stockpile readiness supports nickel ore logistics",
                "category": "operations",
                "tags": ["nickel-ore", "productions"],
            },
            {
                "title": "Corporate operations support long-term mining development",
                "category": "corporate",
                "tags": ["esg", "digital-mining"],
            },
        ]

        articles = []

        for i in range(1, 21):
            base = base_articles[(i - 1) % len(base_articles)]
            title = f"{base['title']} #{i}"

            articles.append(
                {
                    "title": title,
                    "slug": slugify(title),
                    "category": base["category"],
                    "tags": base["tags"],
                    "excerpt": (
                        "Dummy article for testing news listing, category filters, "
                        "tag relationships, search behavior, detail pages, and pagination."
                    ),
                    "content": self.build_content(title),
                }
            )

        return articles

    def build_content(self, title):
        return f"""
            <p><strong>{title}</strong> is a dummy article created for testing the public news module.</p>

            <p>This article helps validate pagination, category filtering, tag relationships, search functionality, and related post rendering.</p>

            <h3>Operational Context</h3>

            <p>Integrated mining visibility supports production monitoring, stockpile readiness, logistics coordination, and sustainable operational development.</p>

            <h3>Testing Purpose</h3>

            <p>This content is generated to test frontend rendering, spacing, bold text, article detail layout, related posts, and TinyMCE HTML output.</p>
            """

    def set_cover_image(self, article, image_path):
        cover_path = Path(settings.MEDIA_ROOT) / image_path

        if not cover_path.exists():
            self.stdout.write(
                self.style.WARNING(f"Cover image not found: {cover_path}")
            )
            return

        article.cover_image.delete(save=False)

        with open(cover_path, "rb") as image_file:
            article.cover_image.save(
                cover_path.name,
                File(image_file),
                save=False,
            )