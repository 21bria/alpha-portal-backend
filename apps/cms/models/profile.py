from django.db import models


class CompanyProfile(models.Model):
    company_name = models.CharField(max_length=160, default="Karya Wijaya")
    legal_name = models.CharField(max_length=200, default="PT Karya Wijaya")
    tagline = models.CharField(
        max_length=255,
        blank=True,
        default="Integrated digital mining ecosystem.",
    )

    primary_logo = models.ImageField(upload_to="company/logo/",blank=True,null=True)
    white_logo = models.ImageField(upload_to="company/logo/", blank=True,null=True)
    favicon = models.ImageField(upload_to="company/favicon/",blank=True,null=True)
    
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=80, blank=True)
    email = models.EmailField(blank=True)

    # socials
    social_links = models.JSONField(default=dict, blank=True,null=True)
    footer_products = models.JSONField(default=list, blank=True,null=True)
    linkedin_url = models.URLField(blank=True,null=True)
    instagram_url = models.URLField(blank=True,null=True)
    youtube_url = models.URLField(blank=True,null=True)
    x_url = models.URLField(blank=True,null=True)

    # footer / seo
    copyright_text = models.CharField(max_length=255, blank=True)
    meta_title = models.CharField(max_length=255,blank=True,null=True)

    meta_description = models.TextField(blank=True,null=True)
    designer_name = models.CharField(max_length=120, blank=True,null=True)
    designer_url = models.CharField(max_length=255, blank=True,null=True)

    # links
    privacy_policy_url = models.CharField(max_length=255, blank=True,null=True)
    cookie_policy_url = models.CharField(max_length=255, blank=True,null=True)
    terms_url = models.CharField(max_length=255, blank=True,null=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company Profile"
        verbose_name_plural = "Company Profile"

    def __str__(self):
        return self.company_name