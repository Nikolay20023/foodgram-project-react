from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Follow
from rest_framework.validators import UniqueTogetherValidator


User = get_user_model()


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
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('user', 'following'),
                message='Такая подписка уже существует'
            )
        ]

    def validate(self, data):
        if (data['user'] == data['following']
                and self.context['request'].method == 'POST'):
            raise serializers.ValidationError(
                'Нельязя оформитб подписку на самого себя'
            )
        return data


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
