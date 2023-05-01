from recipes.models import (
    Recipe,
    Favourite,
    Ingredient,
    RecipeIngredient
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
from .permissions import IsOWnerOrReadOnly, AdminOrReadOnly
from django.shortcuts import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from recipes.models import Tag, ShoppingCart
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from django.db.models import Sum
from urllib.parse import unquote
from core.enums import UrlQueries, Tuples
from core.services import incorrect_layout
from api.paginator import PageLimitPagination


class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related('author')
    serializer_class = RecipeSerializer
    pagination_class = PageLimitPagination
    permission_classes = [IsOWnerOrReadOnly, ]

    def get_queryset(self):
        queryset = self.queryset
        tags: list = self.request.query_params.getlist(UrlQueries.TAGS.value)
        if tags:
            queryset = queryset.filter(
                tags__slug__in=tags
            )
        author: str = self.request.query_params.get(UrlQueries.AUTHOR.value)
        if author:
            queryset = queryset.filter(author=author)

        if self.request.user.is_anonymous:
            return queryset

        is_in_cart = self.request.query_params.get(UrlQueries.SHOP_CART)
        if is_in_cart in Tuples.SYMBOL_TRUE_SEARCH.value:
            queryset = queryset.filter(cart__user=self.request.user)
        if is_in_cart in Tuples.SYMBOL_FALSE_SEARCH.value:
            queryset = queryset.exclude(cart__user=self.request.user)

        is_in_favourite = self.request.query_params.get(UrlQueries.SHOP_CART)
        if is_in_favourite in Tuples.SYMBOL_TRUE_SEARCH.value:
            queryset = queryset.filter(
                favorites_recipes__user=self.request.user
            )
        if is_in_favourite in Tuples.SYMBOL_FALSE_SEARCH.value:
            queryset = queryset.exclude(
                favorites_recipes__user=self.request.user
            )
        return queryset

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
    permission_classes = (AdminOrReadOnly, )


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerialier
    permission_classes = [AdminOrReadOnly, ]

    def get_queryset(self):
        name: str = self.request.query_params.get(UrlQueries.SEARCH_ING_NAME)
        queryset = self.queryset

        if name:
            if name == '%':
                name = unquote(name)
            else:
                name = name.translate(incorrect_layout)

            name = name.lower()
            start_queryset = list(queryset.filter(name__istartswith=name))
            ingredient_set = set(start_queryset)
            cont_queryset = queryset.filter(name__icontains=name)
            start_queryset.extend(
                [ing for ing in cont_queryset if ing not in ingredient_set]
            )
            queryset = start_queryset

        return queryset


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
        user = request.user
        if not ShoppingCart.objects.filter(user=user).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ingredients = RecipeIngredient.objects.filter(
            recipe__cart__user=request.user
        ).values(
            'ingredient__name', 'ingredient__units'
        ).order_by(
            'ingredient__name'
        ).annotate(amount_sum=Sum('amount'))
        main_list = ([
            f"{ingredient['ingredient__name']}: "
            f"{ingredient['amount_sum']} "
            f"{ingredient['ingredient__units']}\n"
            for ingredient in ingredients
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
