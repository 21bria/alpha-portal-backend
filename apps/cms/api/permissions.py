from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthenticatedOrReadOnlyCMS(BasePermission):

    perms_map = {
        "GET": "view",
        "OPTIONS": None,
        "HEAD": None,
        "POST": "add",
        "PUT": "change",
        "PATCH": "change",
        "DELETE": "delete",
    }

    def has_permission(self, request, view):

        # Public read
        if request.method in SAFE_METHODS:
            return True

        # Must login
        if not request.user or not request.user.is_authenticated:
            return False

        model = getattr(view.get_queryset().model, "_meta", None)

        if not model:
            return False

        action = self.perms_map.get(request.method)

        if not action:
            return True

        perm = f"{model.app_label}.{action}_{model.model_name}"

        return request.user.has_perm(perm)