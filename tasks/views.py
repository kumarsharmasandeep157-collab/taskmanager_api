from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Category, Task
from .serializers import TaskSerializer, CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority', 'category']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority']

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user).select_related('category')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path='complete')
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        task.status = 'completed'
        task.save()
        return Response({'status': 'Task marked as completed.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='stats')
    def get_stats(self, request):
        user_tasks = self.get_queryset()
        stats = {
            'total': user_tasks.count(),
            'pending': user_tasks.filter(status='pending').count(),
            'in_progress': user_tasks.filter(status='in_progress').count(),
            'completed': user_tasks.filter(status='completed').count(),
            'cancelled': user_tasks.filter(status='cancelled').count(),
            'overdue': sum(1 for t in user_tasks if t.is_overdue)
        }
        return Response(stats)
