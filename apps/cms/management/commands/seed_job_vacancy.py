# python manage.py seed_job_vacancy --schema=kawi

from django.core.management.base import BaseCommand
from django.utils import timezone
from django_tenants.utils import schema_context

from apps.cms.models import JobVacancy


JOB_VACANCIES = [
    {
        "title": "Mine Planning Engineer",
        "department": "Operations",
        "location": "Site Gebe, Halmahera",
        "employment_type": "Full-time",
        "summary": (
            "Responsible for short-term and long-term mine planning, "
            "production scheduling, and operational optimization."
        ),
        "responsibilities": [
            "Develop weekly and monthly mine plans.",
            "Monitor production performance and mine progress.",
            "Coordinate with geology and production teams.",
            "Prepare operational reports and planning analysis.",
            "Ensure mining activities align with safety standards.",
        ],
        "requirements": [
            "Minimum 3 years experience in mine planning.",
            "Familiar with Surpac or Minescape software.",
            "Strong analytical and reporting skills.",
            "Good communication and teamwork abilities.",
            "Bachelor degree in Mining Engineering.",
        ],
        "is_open": True,
    },

    {
        "title": "Heavy Equipment Mechanic",
        "department": "Maintenance",
        "location": "Site Weda",
        "employment_type": "Contract",
        "summary": (
            "Perform preventive and corrective maintenance "
            "for mining heavy equipment operations."
        ),
        "responsibilities": [
            "Inspect heavy equipment regularly.",
            "Perform preventive maintenance activities.",
            "Troubleshoot mechanical breakdowns.",
            "Coordinate spare part requirements.",
            "Maintain maintenance reporting records.",
        ],
        "requirements": [
            "Minimum 4 years experience as heavy equipment mechanic.",
            "Understand hydraulic and engine systems.",
            "Able to read technical manuals.",
            "Good troubleshooting capability.",
            "Willing to work on site roster schedule.",
        ],
        "is_open": True,
    },

    {
        "title": "ESG Officer",
        "department": "Sustainability",
        "location": "Jakarta Head Office",
        "employment_type": "Full-time",
        "summary": (
            "Support sustainability programs, ESG reporting, "
            "and stakeholder engagement initiatives."
        ),
        "responsibilities": [
            "Prepare ESG performance reports.",
            "Coordinate sustainability programs.",
            "Monitor environmental compliance.",
            "Support stakeholder communication.",
            "Assist CSR implementation activities.",
        ],
        "requirements": [
            "Bachelor degree in Environmental Engineering or related field.",
            "Minimum 2 years ESG or sustainability experience.",
            "Good report writing skills.",
            "Familiar with sustainability frameworks.",
            "Strong communication skills.",
        ],
        "is_open": True,
    },

    {
        "title": "GIS Specialist",
        "department": "Digital Mining",
        "location": "Jakarta",
        "employment_type": "Full-time",
        "summary": (
            "Manage spatial mining data and support "
            "operational mapping systems."
        ),
        "responsibilities": [
            "Maintain GIS database and mapping systems.",
            "Produce operational and exploration maps.",
            "Analyze geospatial data.",
            "Support drone mapping integration.",
            "Coordinate with survey teams.",
        ],
        "requirements": [
            "Experience using ArcGIS or QGIS.",
            "Strong spatial analysis capability.",
            "Understanding of mining operations.",
            "Minimum 2 years GIS experience.",
            "Bachelor degree in Geodesy or related field.",
        ],
        "is_open": True,
    },
]


class Command(BaseCommand):
    help = "Seed dummy job vacancies"

    def add_arguments(self, parser):
        parser.add_argument(
            "--schema",
            type=str,
            required=True,
            help="Tenant schema name"
        )

    def handle(self, *args, **options):
        schema_name = options["schema"]

        with schema_context(schema_name):

            created = 0
            updated = 0

            for item in JOB_VACANCIES:

                obj, is_created = JobVacancy.objects.update_or_create(
                    slug=item["title"].lower().replace(" ", "-"),
                    defaults={
                        "title": item["title"],
                        "department": item["department"],
                        "location": item["location"],
                        "employment_type": item["employment_type"],
                        "summary": item["summary"],
                        "responsibilities": item["responsibilities"],
                        "requirements": item["requirements"],
                        "is_open": item["is_open"],
                        "published_at": timezone.now(),
                    }
                )

                if is_created:
                    created += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Created job vacancy: {obj.title}"
                        )
                    )
                else:
                    updated += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"Updated job vacancy: {obj.title}"
                        )
                    )

            self.stdout.write("")
            self.stdout.write(
                self.style.SUCCESS(
                    f"Done. Created={created}, Updated={updated}"
                )
            )