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

    def has_object_permission(
            self,
            view: APIRootView,
            request: WSGIRequest,
            obj: Model
    ):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            or request.user.is_active
            and (
                request.user == obj.author
                or request.user.is_staff
            )
        )


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
