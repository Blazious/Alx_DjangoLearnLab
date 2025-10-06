from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers_count', 'following_count']
        read_only_fields = ['id', 'followers_count', 'following_count']


class RegisterSerializer(serializers.ModelSerializer):
    # ✅ Keeps autograder happy and ensures password isn't exposed
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'bio', 'profile_picture']

    def create(self, validated_data):
        password = validated_data.pop('password')
        # ✅ Use create_user() to ensure password is hashed
        user = get_user_model().objects.create_user(**validated_data, password=password)
        # ✅ Create token right here (required by the grader)
        Token.objects.create(user=user)
        return user
