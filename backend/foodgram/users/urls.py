from django.urls import path, include
from .views import CustomUserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('users/subscriptions/', CustomUserViewSet.as_view(
        {'get': 'subscriptions'}
    )),
    path(
        'users/<int:id>/subscribe',
        CustomUserViewSet.as_view({
            'post': 'subscribe',
        })
    ),
    path(
        'users/<int:id>/unsubscribe',
        CustomUserViewSet.as_view(
            {
                'delete': 'unsubscribe',
            }
        )
    )
]
