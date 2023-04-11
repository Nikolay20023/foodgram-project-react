from rest_framework import serializers
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


User = get_user_model()


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp' + ext)
        return super().to_internal_value()


class RecipeSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField(many=True)
    ingredient = serializers.StringRelatedField(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'


class IngredientSerialier(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = serializers.StringRelatedField(many=True)
    recipe = serializers.StringRelatedField(many=True)

    class Meta:
        model = RecipeIngredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


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