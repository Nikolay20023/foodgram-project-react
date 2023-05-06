from django.urls import path, include
from .views import CustomizeUserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', CustomizeUserViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
