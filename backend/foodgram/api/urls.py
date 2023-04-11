from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RecipeViewset,
    TagViewSet,
    IngredientViewSet,
    FavotiteViewSet,
    ShhoopingViewSet
)

router = DefaultRouter()
app_name = 'api'

router.register(
    r'recipes', RecipeViewset, basename='recipes'
)
router.register(
    r'tags', TagViewSet, basename='tags'
)
router.register(
    r'ingredients', IngredientViewSet, basename='ingredients'
)

urlpatterns = [
    path(
        'recipes/<int:id>/shopping_cart/',
        ShhoopingViewSet.as_view(
            {
                'post': 'create',
                'delete': 'destroy'
            }
        ),
        name='shopping_cart'
    ),
    path(
        'recipes/<int:id>/favorite/',
        FavotiteViewSet.as_view(
            {
                'post': 'create',
                'delete': 'destroy'
            }
        ),
        name='favourite'
    ),
    path(
        'recipes/download_shopping_cart/',
        ShhoopingViewSet.as_view(
            {
                'get': 'list'
            }
        )
    ),
    path('', include(router.urls)),
]
