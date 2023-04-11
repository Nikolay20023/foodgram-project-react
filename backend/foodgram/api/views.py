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
    ShoppingSerializer,
    FavouriteSerializer,
)
from .permissions import IsOWnerOrReadOnly
from django.shortcuts import HttpResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from recipes.models import Tag, ShoppingCart
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied


class RecipeReadViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsOWnerOrReadOnly, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        user = self.request.user

        if instance.author != user:
            raise PermissionDenied("Вы не имеете таких полномочий.")
        instance.delete()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny, ]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerialier
    permission_classes = [AllowAny, ]


class ShhoopingViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        user = request.user
        recipe_id = kwargs.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if ShoppingCart.objects.filter(
            user=user, recipe=recipe
        ).exists():
            return Response(
                {'detail': 'Рецепт уже добавлен в список'},
                status=status.HTTP_400_BAD_REQUEST
            )
        cart = ShoppingCart.objects.create(
            user=user,
            recipe=recipe
        )
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        recipe_id = kwargs.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ShoppingCart.objects.get(
            user=user,
            recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        shopping_list = {}
        user = request.user
        if not ShoppingCart.objects.filter(user=user).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ingredients = ShoppingCart.objects.filter(user=user).values_list(
            'recipe__recipe_ingredients__ingredient__name',
            'recipe__recipe_ingredients__amount',
            'recipe__recipe_ingredients__ingredient__units')
        for ingredient in ingredients:
            if ingredient[0] in shopping_list.keys():
                shopping_list[ingredient[0]]['amount'] += ingredient[1]
            else:
                shopping_list[ingredient[0]] = {
                    'amount': ingredient[1],
                    'units':  ingredient[2]
                }

        main_list = ([
            f"{item}: {value['amount']}"
            f"{value['units']}\n"
            for item, value in shopping_list.items()
        ])
        response = HttpResponse(main_list, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="BuyList.txt'
        return response


class FavotiteViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    queryset = Favourite.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = FavouriteSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        recipe_id = kwargs.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if Favourite.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                {'detail': 'Подписка уже создана'},
                status=status.HTTP_400_BAD_REQUEST
            )
        favourite = Favourite.objects.create(user=user, recipe=recipe)
        serializer = self.get_serializer(favourite)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        recipe_id = kwargs.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        Favourite.objects.get(
            user=user,
            recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
