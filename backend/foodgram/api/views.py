from rest_framework.views import APIView
from recipes.models import Recipe
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    MyTokenObtainPairSerializer,
    RecipesSerializers,
    TagSerializers
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from rest_framework import generics
from recipes.models import Tag
from rest_framework_simplejwt.tokens import RefreshToken


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


class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers


class TagRetrieve(generics.RetrieveAPIView):
    queryset = Tag.objects.all(id=id)
    serializer_class = TagSerializers


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                content_type=e
            )
