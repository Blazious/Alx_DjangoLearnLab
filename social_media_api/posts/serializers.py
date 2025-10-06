from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment

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


class PostSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=User.objects.all(), source='author', required=False
    )
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_id', 'title', 'content', 'created_at', 'updated_at', 'comments']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'comments']
