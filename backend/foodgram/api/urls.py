from django.urls import path
from views import FavouriteRecipeView
from rest_framework_simplejwt.views import TokenRefreshView
from views import MyTokenObtainPair


urlpatterns = {
    path('recipes/<int:id>/favorite/', FavouriteRecipeView.as_view()),
    path('auth/token/login/', MyTokenObtainPair.as_view()),
    path('auth/token/logout/', TokenRefreshView.as_view()),
}