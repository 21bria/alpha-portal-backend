from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Client(TenantMixin):
    name = models.CharField(max_length=150)
    company_code = models.CharField(max_length=50, unique=True)

    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # otomatis create schema saat tenant disimpan
    auto_create_schema = True

    class Meta:
        db_table = "tenant_clients"
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    class Meta:
        db_table = "tenant_domains"
        verbose_name = "Domain"
        verbose_name_plural = "Domains"