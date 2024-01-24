'''Notification url mappings.'''
from django.urls import path

from notification import views


app_name = 'notification'

urlpatterns = [
    path('all/', views.AllUserNotificationsView.as_view(), name='all_notifications'),
    path('unread/', views.AllUnreadUserNotificationView.as_view(), name='unread_notifications'),
    path('<int:pk>/', views.MarkNotificationReadView.as_view(), name='mark_notification_read'),
    path('clear/', views.ClearNotificationsView.as_view(), name='clear_all_notifications'),
]
