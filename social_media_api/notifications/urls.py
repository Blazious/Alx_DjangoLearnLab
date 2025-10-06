from django.urls import path
from .views import NotificationListView, MarkAllReadAPIView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications-list'),
    path('mark-all-read/', MarkAllReadAPIView.as_view(), name='notifications-mark-all-read'),
]
