from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import User, Task
from .serializers import UserSerializer, TaskSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                return User.objects.all()
            return User.objects.filter(pk=user.pk)
        return User.objects.none()

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'due_date']
    ordering_fields = ['due_date', 'priority', 'created_at']

    def get_queryset(self):
        return self.request.user.tasks.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='mark-complete')
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        if task.status == 'C':
            return Response({'detail': 'Task already completed.'}, status=status.HTTP_400_BAD_REQUEST)
        task.status = 'C'
        task.completed_at = timezone.now()
        task.save()
        return Response({'status': 'completed'})

    @action(detail=True, methods=['post'], url_path='mark-incomplete')
    def mark_incomplete(self, request, pk=None):
        task = self.get_object()
        if task.status == 'P':
            return Response({'detail': 'Task already pending.'}, status=status.HTTP_400_BAD_REQUEST)
        task.status = 'P'
        task.completed_at = None
        task.save()
        return Response({'status': 'incomplete'})
