from django.urls import path, include
from .views import FavouriteRecipeView
from rest_framework.routers import DefaultRouter
from .views import (
    RecipeViewset,
    TagViewSet,
    IngredientViewSet
)

router = DefaultRouter()

router.register(
    r'recipes', RecipeViewset
)

router.register(
    r'tags', TagViewSet
)

router.register(
    r'ingredients', IngredientViewSet
)

urlpatterns = [
    path('recipes/<int:pk>/favorite/', FavouriteRecipeView.as_view()),
    path('', include(router.urls)),
]