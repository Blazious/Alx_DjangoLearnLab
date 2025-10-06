from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'profile_picture']

class NotificationSerializer(serializers.ModelSerializer):
    actor = ActorSerializer(read_only=True)
    # represent target as simple string
    target_repr = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'target_repr', 'unread', 'timestamp']
        read_only_fields = ['id', 'actor', 'verb', 'target_repr', 'timestamp']

    def get_target_repr(self, obj):
        if obj.target is None:
            return None
        return str(obj.target)
