from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin)


class IsInstructorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.is_instructor or request.user.is_admin)
        )


class IsInstructorOwnerOrReadOnly(BasePermission):
    """Course ka instructor ya admin hi object edit kar sakta hai."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_admin:
            return True
        instructor = getattr(obj, "instructor", None)
        if instructor is None:
            return False
        return instructor.id == request.user.id
