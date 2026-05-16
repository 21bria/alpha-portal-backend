from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.cms.api.page.views import (
    PageViewSet,
    PageSectionViewSet,
)
from apps.cms.api.news.views import (
    NewsCategoryViewSet,
    NewsTagViewSet,
    NewsArticleViewSet,
)

from apps.cms.api.news_topics.views import NewsTopicViewSet

from apps.cms.api.project.views import ProjectViewSet,ProjectSectionViewSet
from apps.cms.api.jobs.views import JobVacancyViewSet
from apps.cms.api.documents.views import (
    DocumentCategoryViewSet,
    DocumentViewSet,
)

from apps.cms.api.upload_views import *
from apps.cms.api.upload_section_image import upload_section_image
from apps.cms.api.profile.views import CompanyProfileViewSet
from apps.cms.api.tasks.views import TaskViewSet

# Media
from apps.cms.api.media.views import (
    MediaAlbumItemViewSet,
    MediaAlbumViewSet,
    MediaCategoryViewSet,
    MediaViewSet,
)

router = DefaultRouter()
router.register("pages", PageViewSet, basename="cms-pages")
router.register("sections", PageSectionViewSet, basename="cms-sections")

router.register("news-categories", NewsCategoryViewSet, basename="cms-news-categories")
router.register("news-tags", NewsTagViewSet, basename="cms-news-tags")
router.register("news", NewsArticleViewSet, basename="cms-news")
router.register("news-topics",NewsTopicViewSet,basename="cms-news-topics")

router.register("job-vacancies", JobVacancyViewSet, basename="cms-job-vacancies")

router.register("projects", ProjectViewSet, basename="cms-projects")
router.register("projects-sections", ProjectSectionViewSet, basename="cms-projects-sections")

router.register("document-categories", DocumentCategoryViewSet, basename="cms-document-categories")
router.register("documents", DocumentViewSet, basename="cms-documents")

router.register("company-profile",CompanyProfileViewSet, basename="cms-company-profile")

router.register("tasks", TaskViewSet, basename="cms-tasks")

# Media
router.register("media-categories", MediaCategoryViewSet, basename="media-category")
router.register("albums", MediaAlbumViewSet, basename="media-album")
router.register("album-items", MediaAlbumItemViewSet, basename="media-album-item")
router.register("media", MediaViewSet, basename="media")


urlpatterns = [
    path("tinymce/upload-image/", TinyMCEImageUploadView.as_view()),
    path("tinymce/upload-section-image/",TinyMCEImageUploadSectionsView.as_view()),
    path("section-images/upload/",upload_section_image, name="section-images-upload"),

    # Project Images:
    path(
    "tinymce/upload-project-image/",
    TinyMCEProjectImageUploadView.as_view(),
    name="tinymce-upload-project-image",
    ),
    path(
        "tinymce/upload-project-section-image/",
        TinyMCEProjectSectionImageUploadView.as_view(),
        name="tinymce-upload-project-section-image",
    ),
    path("", include(router.urls)),
]
