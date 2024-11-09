from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.models.category import Category
from api.serializers.category import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        project_id = self.request.GET.get("project_id")
        queryset = self.queryset.filter(project=project_id, project__members=self.request.user.id)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        # Handle delete category with referenced devices
        instance = self.get_object()
        if instance.devices.count() > 0:
            return Response(
                {"error": "Categoria possui dispositivos vinculados."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)