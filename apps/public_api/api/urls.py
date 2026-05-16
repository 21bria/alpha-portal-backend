from django.urls import path
from apps.public_api.api.news.views import (
    PublicNewsListView,
    PublicNewsDetailView,
    PublicNewsCategoryListView,
    PublicNewsTagListView
)
from apps.public_api.api.news_topics.views import (
    PublicNewsTopicListView,
    PublicNewsTopicDetailView,
)
from apps.public_api.api.pages.views import (
    PublicHomeView,
    PublicPageDetailView,
)
from  apps.public_api.api.projects.views import PublicProjectDetailView, PublicProjectListView

from  apps.public_api.api.profile.views import PublicCompanyProfileView

from apps.public_api.api.careers.views import (
    PublicJobVacancyListView,
    PublicJobVacancyDetailView,
)

from apps.public_api.api.media.views import (
    PublicMediaListView,
    PublicMediaDetailView,
    PublicMediaAlbumListView,
    PublicMediaAlbumDetailView,
    PublicMediaCategoryListView,
)

urlpatterns = [
    path("home/", PublicHomeView.as_view(), name="public-home"),
    path("pages/<slug:slug>/", PublicPageDetailView.as_view(), name="public-page-detail"),

    path("news/", PublicNewsListView.as_view(), name="public-news-list"),
    path( "news/categories/", PublicNewsCategoryListView.as_view(),name="public-news-categories"),
    path( "news/tags/",PublicNewsTagListView.as_view(), name="public-news-tags"),

    path("news/<slug:slug>/", PublicNewsDetailView.as_view(), name="public-news-detail"),

    # Topic News 
    path("news/topics/",PublicNewsTopicListView.as_view(), name="public-news-topic-list"),

    path("news/topics/<slug:slug>/", PublicNewsTopicDetailView.as_view(), name="public-news-topic-detail"),

    path("projects/", PublicProjectListView.as_view(), name="public-project-list"),
    path("projects/<slug:slug>/", PublicProjectDetailView.as_view(), name="public-project-detail"),

    path("company-profile/",PublicCompanyProfileView.as_view(),name="public-company-profile"),

    # Careers
    path("careers/",PublicJobVacancyListView.as_view(), name="public-job-vacancy-list"),
    path("careers/<slug:slug>/", PublicJobVacancyDetailView.as_view(),name="public-job-vacancy-detail"),

    # Media
    path("media/",PublicMediaListView.as_view(),name="public-media-list"),
    path("media/<int:id>/",PublicMediaDetailView.as_view(), name="public-media-detail"),
    path("media/albums/",PublicMediaAlbumListView.as_view(),name="public-media-album-list"),
    path("media/albums/<slug:slug>/",PublicMediaAlbumDetailView.as_view(),name="public-media-album-detail"),
    path("media/categories/", PublicMediaCategoryListView.as_view(),name="public-media-category-list"),
    
]

