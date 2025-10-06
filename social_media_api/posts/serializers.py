from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like

User = get_user_model()

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'profile_picture']

class CommentSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=User.objects.all(), source='author', required=False
    )

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_id', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def validate(self, attrs):
        # Ensure post is provided (if creating) — view may set post from URL instead
        if self.instance is None and 'post' not in attrs:
            raise serializers.ValidationError({"post": "Post is required."})
        return attrs

class LikeSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all(), source='user')

    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'user_id', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=User.objects.all(), source='author', required=False
    )
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_id', 'title', 'content', 'created_at', 'updated_at', 'comments']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'comments']
    def get_liked_by_user(self, obj):
        request = self.context.get('request')
        if not request or not request.user or not request.user.is_authenticated:
            return False
        return obj.likes.filter(user=request.user).exists()