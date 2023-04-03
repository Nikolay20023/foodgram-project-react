from django.urls import path, include
from .views import FavouriteRecipeView
from rest_framework.routers import DefaultRouter
from .views import (
    RecipeViewset,
    TagViewSet,
)

router = DefaultRouter()

router.register(
    r'recipes', RecipeViewset
)

router.register(
    r'tags', TagViewSet
)

urlpatterns = [
    path('recipes/<int:pk>/favorite/', FavouriteRecipeView.as_view()),
    path('', include(router.urls)),
]