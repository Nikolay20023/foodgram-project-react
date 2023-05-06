from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.routers import APIRootView
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Model


class BanPermission(BasePermission):
    def has_permission(
        self,
        request: WSGIRequest,
        view: APIRootView
    ) -> bool:
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
        )


class AuthenticatedOrReadOnly(BanPermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_superuser
            or request.user.is_admin
        )


class IsOWnerOrReadOnly(BanPermission):

    def has_object_permission(
        self,
        request: WSGIRequest,
        view: APIRootView,
        obj: Model
    ) -> bool:
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
            and request.user == obj.author
            or request.user.is_staff
        )


class AuthoStaffOrReadOnly(BanPermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user


class AdminOrReadOnly(BanPermission):

    def has_object_permission(
            self,
            request: WSGIRequest,
            view: APIRootView
    ):
        return (
            self.request in SAFE_METHODS
            or self.user.is_authenticated
            and self.user.is_active
            and self.user.is_staff
        )


class OwnerUserOrReadOnly(BanPermission):
    """
    Разрешение на создание и изменение только для админа и пользователя.
    Остальным только чтение объекта.
    """
    def has_object_permission(
        self,
        request: WSGIRequest,
        view: APIRootView,
        obj: Model
    ) -> bool:
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
            and request.user == obj.author
            or request.user.is_staff
        )
