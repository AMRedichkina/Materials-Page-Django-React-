
from rest_framework.permissions import IsAuthenticated
from .models import Material
from .serializers import MaterialSerializer
from .filters import MaterialSearchFilter

from rest_framework import viewsets
from api.pagination import LimitPageNumberPagination


class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    filter_backends = (MaterialSearchFilter,)
    search_fields = ('^name',)
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitPageNumberPagination

