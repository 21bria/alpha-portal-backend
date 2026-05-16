from django.db import models
from django.contrib.auth.models import AbstractUser
ROLE_CHOICES = (
    ("SYSTEM", "System Admin"),          # internal full control
    ("GLOBAL_VIEWER", "Global Viewer"),  # read only semua
    ("ADMIN_USER", "Admin User"),        # hanya Admin sendiri
)

class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="ADMIN_USER"
    )

    # Helper properties biar enak dipakai di API
    @property
    def is_system(self):
        return self.role == "SYSTEM" or self.is_superuser

    @property
    def is_global_viewer(self):
        return self.role == "GLOBAL_VIEWER"

    @property
    def is_admin_user(self):
        return self.role == "ADMIN_USER"
    
    