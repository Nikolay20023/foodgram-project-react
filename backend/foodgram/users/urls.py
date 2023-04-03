from django.urls import path, include
from .views import FollowApiView, FollowListApiView


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('users/subscriptions/', FollowListApiView.as_view()),
    path('users/<int:following_id>/subscribe', FollowApiView.as_view())
]