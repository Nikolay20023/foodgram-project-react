from rest_framework.views import APIView
from recipes.models import Recipe
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .serializers import MyTokenObtainPairSerializer, RecipesSerializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from recipes.models import Recipe



class FavouriteRecipeView(APIView):

    def post(self, request):
        recipe = get_object_or_404(Recipe, id=request.data.get('id'))
        if request.user not in recipe.favourite.all():
            recipe.favourite.add(request.user)
            return Response(
                {'detail': 'Пользователь добавил в избранное '},
                status=status.HTTP_200_OK
            )
        return Response(
            {'detail': self.bad_request_message},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request):
        recipe = get_object_or_404(Recipe, id=request.data.get('id'))
        if request.user in recipe.favourite.all():
            recipe.favourite.remove(request.user)
            return Response(
                {'detail': 'Пользователь удалён с подписок'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {'detail': self.bad_request_message},
            status=status.HTTP_400_BAD_REQUEST
        )


class MyTokenObtainPair(TokenObtainPairView):
    permission_classes = (AllowAny, )
    serializer_class = MyTokenObtainPairSerializer


class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializers
