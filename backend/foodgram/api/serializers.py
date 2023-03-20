from rest_framework import serializers
from django.contrib.auth import get_user_model
import base64
from django.core.files.base import ContentFile
from recipes.models import Recipe, Tag, Ingredient
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


class UserCreationSerializers(serializers.Serializer):

    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp' + ext)
        return super().to_internal_value()
    

class RecipesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'author',
            'name',
            'image',
            'text',
            'ingredient',
            'time_to_coooking',
            'tag'
        )


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('')


class IngredientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['username'] = user.username
        return token
    