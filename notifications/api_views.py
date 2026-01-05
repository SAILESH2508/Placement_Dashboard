from rest_framework import generics, permissions, serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    pinned = serializers.BooleanField(default=False, read_only=True)
    
    class Meta:
        model = Notification
        fields = '__all__'

class NotificationListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny] # For demo simplicity
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer
