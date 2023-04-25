from rest_framework import serializers
from collections import OrderedDict
from django.contrib.auth import get_user_model
import base64
from django.core.files.base import ContentFile
from recipes.models import (
    Recipe,
    Tag,
    Ingredient,
    RecipeIngredient,
    ShoppingCart,
    Favourite
)
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import F
from django.db.transaction import atomic


User = get_user_model()


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp' + ext)
        return super().to_internal_value()


class IngredientSerialier(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = '__all__',

        def validate(self, data: OrderedDict):
            for attr, value in data.items():
                data[attr] = value.sttrip(' # ').upper()
            return data


class IngredientRecipeGetSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    units = serializers.ReadOnlyField(source='ingredient.units')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'units', 'amount')
        validators = [
            UniqueTogetherValidator(
                queryset=RecipeIngredient.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = '__all__',


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = serializers.StringRelatedField(many=True)
    recipe = serializers.StringRelatedField(many=True)

    class Meta:
        model = RecipeIngredient
        fields = ('__all__')


class TagSerializer(serializers.ModelSerializer):
    color = Base64ImageField()

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = '__all__',


class ShoppingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = '__all__'


class FavouriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourite
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=Favourite.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже добавлен в избранное'
            )
        ]


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shooping_cart = serializers.SerializerMethodField()
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'author',
            'tags',
            'text',
            'ingredients',
            'cooking_time',
            'image',
            'is_favorited',
            'is_in_shooping_cart'
        )
        read_only_fields = (
            'is_favorited',
            'is_in_shooping_cart'
        )

    def get_ingredients(self, recipe: Recipe):
        ingredients = recipe.ingredients.values(
            'id', 'name', 'units', amount=F('ingredient_recipes__amount')
        )
        return ingredients

    def get_is_favorited(self, recipe: Recipe):
        user = self.context.get('request').user

        if user.is_anonymous:
            return False

        return user.favorites.filter(recipe=recipe).exists()

    def get_is_in_shooping_cart(self, recipe: Recipe):
        user = self.context.get('request').user

        if user.is_anonymous:
            return False

        return user.user_cart.filter(recipe=recipe).exists()

    @atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        recipe.ingredients.set(ingredients)
        return recipe

    @atomic
    def update(self, validate_data: dict, recipe: Recipe):
        tags = validate_data.pop('tags')
        ingredients = validate_data.pop('ingredients')
        for key, value in validate_data.items():
            if hasattr(recipe, key):
                setattr(recipe, key, value)

        if tags:
            recipe.tags.clear()
            recipe.tags.set(tags)

        if ingredients:
            recipe.ingredients.clear()
            recipe.ingredients.set(ingredients)

        recipe.save()
        return recipe

    """def to_representation(self, instance):
        self.fields.pop('ingredient')
        self.fields.pop('tag')
        representation = super().to_representation(instance)
        representation['ingredient'] = IngredientRecipeGetSerializer(
            RecipeIngredient.objects.filter(recipe=instance), many=True
        ).data
        representation['tag'] = TagSerializer(
            instance.tag, many=True
        ).data
        return representation"""
