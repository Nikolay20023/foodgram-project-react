from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Follow
from rest_framework.validators import UniqueTogetherValidator
from recipes.models import Recipe


User = get_user_model()


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = '__all__',


class CurrentSertializer(serializers.ModelSerializer):
    is_subscrited = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'is_subscrited'
            'first_name',
            'last_name',
            'password',
        )

    def get_is_subcribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return Follow.objects.filter(
            user_id=user,
            following_user_id=obj
        ).exists()


class UserFollowSerializer(serializers.ModelSerializer):

    following = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all()
    )
    user = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('user', 'following'),
                message='Такая подписка уже существует'
            )
        ]


class FollowListSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'recipes', 'recipes_count'
        )


class CustomUserSerializator(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = 'is_subscribed',

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user

        if user.is_anonymous or (user == obj):
            return False
        return Follow.objects.filter(
            user=user,
            author=obj
        ).exists()

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSubscribeSerializer(CustomUserSerializator):
    recipes = ShortRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'id',
            'password',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes_count(self, recipe):
        user = self.context.get('request').user
        return user.recipes.count()

    def get_is_subscribed(self, obj):
        return True
