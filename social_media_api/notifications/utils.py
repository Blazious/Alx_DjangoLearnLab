from django.contrib.contenttypes.models import ContentType
from .models import Notification

def create_notification(recipient, actor, verb, target=None):
    """
    Creates a Notification record.
    - recipient: User instance that will receive notification
    - actor: User instance who performed the action
    - verb: short text like 'liked', 'commented on', 'followed'
    - target: optional model instance related to the action
    """
    kwargs = {
        'recipient': recipient,
        'actor': actor,
        'verb': verb,
    }
    if target is not None:
        ct = ContentType.objects.get_for_model(target.__class__)
        kwargs['target_content_type'] = ct
        kwargs['target_object_id'] = target.pk

    return Notification.objects.create(**kwargs)
