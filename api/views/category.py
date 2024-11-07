from rest_framework import viewsets
from api.models.category import Category
from api.serializers.category import CategorySerializer
from rest_framework.permissions import IsAuthenticated

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        project_id = self.request.GET.get("project_id")
        queryset = self.queryset.filter(project=project_id, project__members=self.request.user.id)
        return queryset