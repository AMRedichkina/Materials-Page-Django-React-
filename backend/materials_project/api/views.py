
from rest_framework.permissions import IsAuthenticated
from .models import Material
from .serializers import MaterialSerializer
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from api.pagination import LimitPageNumberPagination


class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for retrieving material information with filtering and pagination.

    This viewset provides read-only endpoints for retrieving material information.
    It supports filtering based on search term, material type, and availability.
    Pagination is applied using the LimitPageNumberPagination class.

    Attributes:
        queryset (QuerySet): The queryset of Material objects.
        serializer_class (MaterialSerializer): The serializer class for Material.
        filter_backends (list): List of backend classes for filtering.
        permission_classes (tuple): Tuple of permission classes.
        pagination_class (LimitPageNumberPagination): Pagination class for limiting
            the number of items per page.

    Methods:
        get_queryset(): Returns the filtered queryset based on query parameters.
    """
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitPageNumberPagination

    def get_queryset(self):
        """
        Get the filtered queryset based on query parameters.

        Returns:
            QuerySet: The filtered queryset of Material objects.
        """

        queryset = Material.objects.all()

        search_term = self.request.query_params.get('search', None)
        material_type = self.request.query_params.get('type', None)
        availability_value = self.request.query_params.get('availability', None)

        if search_term:
            queryset = queryset.filter(name__icontains=search_term)
        if material_type:
            material_type_list = material_type.split(',')
            queryset = queryset.filter(type__in=material_type_list)
        if availability_value is not None:
            is_available = availability_value.lower() == 'true'
            queryset = queryset.filter(availability=is_available)

        return queryset
    