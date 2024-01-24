from notification.models import Notification
from account.authentication import CustomAuthentication
from notification.serializers import NotificationSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions


class AllUserNotificationsView(APIView):
    '''View retireves all user mnotifications (i.e read and unread).'''
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [CustomAuthentication, ]
    ordering = ['-created_at']

    def get(self, request):
        notifications = Notification.objects.filter(user_id=request.user, is_active=True).order_by('-created_at')
        serializer = self.serializer_class(notifications, context={'request': request}, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AllUnreadUserNotificationView(APIView):
    '''View gets all unread user notifications.'''
    serializer_class = NotificationSerializer
    permission_classese = [IsAuthenticated, ]
    authentication_classes = [CustomAuthentication, ]
    ordering = ['-created_at']

    def get(self, request):
        notifications = Notification.objects.filter(user_id=self.request.user, is_read=False, is_active=True).order_by('-created_at')
        serializer = self.serializer_class(notifications, context={'request': request}, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class MarkNotificationReadView(APIView):
    '''View marks specific notification as read.'''
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [CustomAuthentication,]

    def get_object(self, pk, user):
        try:
            context = {'status': 'error','message': 'Notification not found'}
            notification = Notification.objects.get(user_id=user, pk=pk, is_active=True)
            notification.is_read = True
            notification.save()
            return notification

        except (Notification.DoesNotExist, TypeError):
            raise exceptions.ParseError(context)

    def get(self, request, pk, format=None):
        context = {'status': 'success'}
        serializer = self.serializer_class(self.get_object(pk, request.user))
        context.update(serializer.data)
        return Response(context, status.HTTP_200_OK)


class ClearNotificationsView(APIView):
    '''View clears all user notification.'''
    serializer_class = None
    permission_classes = [IsAuthenticated,]
    authentication_classes = [CustomAuthentication,]

    def get(self, request):
        data = {'is_read': True, 'is_active': False}
        Notification.objects.filter(user_id=request.user, is_active=True).update(**data)
        context = {'status': 'success'}
        return Response(context, status.HTTP_200_OK)
