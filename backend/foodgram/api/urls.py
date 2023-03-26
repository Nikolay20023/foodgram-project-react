from django.urls import path, include
from .views import FavouriteRecipeView
from .views import MyTokenObtainPair
from rest_framework.routers import DefaultRouter
from .views import (
    RecipeViewset,
    TagList,
    TagRetrieve,
    LogoutView,
    ChangePasswordView,
    RegisterView,
    UsersList,
)

router = DefaultRouter()

router.register(
    r'recipes', RecipeViewset
)

urlpatterns = [
    path('recipes/<int:pk>/favorite/', FavouriteRecipeView.as_view()),
    path('auth/token/login/', MyTokenObtainPair.as_view()),
    path('auth/token/logout/', LogoutView.as_view()),
    path('', include(router.urls)),
    path('tags/', TagList.as_view()),
    path('tags/<int:pk>/', TagRetrieve.as_view()),
    path('users/set_password/', ChangePasswordView.as_view()),
    path('users/', RegisterView.as_view()),
]