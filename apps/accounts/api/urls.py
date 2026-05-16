from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from apps.accounts.api.views import LoginView, MeView

router = DefaultRouter()

from apps.accounts.api.admin.views import AdminUserViewSet
from apps.accounts.api.group.views import AdminGroupViewSet
from apps.accounts.api.group.lookup import GroupLookupViewSet
from apps.accounts.api.permissions.views import PermissionTreeView
from apps.accounts.api.group.permissions import GroupPermissionsView

from apps.accounts.api.security.account_update_view import AccountUpdateView
from apps.accounts.api.security.change_password_view import ChangePasswordView
from apps.accounts.api.profile.views import ProfileView

router.register(r"admin/users", AdminUserViewSet, basename="admin-users")
router.register(r"admin/groups", AdminGroupViewSet, basename="admin-groups")
router.register(r"groups/lookup", GroupLookupViewSet, basename="group-lookup")

urlpatterns = [

    path("login/", LoginView.as_view(), name="auth-login"),
    path("refresh/", TokenRefreshView.as_view(), name="auth-refresh"),
    path("me/", MeView.as_view(), name="auth-me"),

    # permission tree
    path("permissions/tree/", PermissionTreeView.as_view(), name="permission-tree"),
    path("admin/groups/<int:pk>/permissions/",GroupPermissionsView.as_view(),),

    # Account & Password
    path("account/update/", AccountUpdateView.as_view(), name="account-update"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),

    path('profile/', ProfileView.as_view(), name='auth-profile'),

    # ADMIN (router)
    path("", include(router.urls)),
]