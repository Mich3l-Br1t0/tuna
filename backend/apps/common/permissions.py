from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsUniversityAccount(BasePermission):
    message = "Only university accounts can manage athletes."

    def has_permission(self, request: Request, view: APIView) -> bool:
        user = request.user
        return bool(
            user and user.is_authenticated and getattr(user, "is_university_account", False)
        )
