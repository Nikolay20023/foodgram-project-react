from rest_framework.views import APIView
from recipes.models import (
    Recipe,
    Favourite,
    Ingredient,
)
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    RecipeSerializer,
    TagSerializer,
    IngredientSerialier,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from recipes.models import Tag


class FavouriteRecipeView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        recipe = get_object_or_404(Recipe, id=request.data.get('id'))
        if recipe not in Favourite.objects.all(id=request.id):
            Favourite.objects.create(
                user=request.user,
                recipe=recipe
            )
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
        if recipe in Favourite.objects.all():
            Favourite.objects.delete(id=request.id)
            return Response(
                {'detail': 'Пользователь удалён с подписок'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {'detail': self.bad_request_message},
            status=status.HTTP_400_BAD_REQUEST
        )


class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerialier
    permission_classes = (IsAuthenticated, )
