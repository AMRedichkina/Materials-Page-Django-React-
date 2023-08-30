from django_filters import rest_framework as filters

from rest_framework.filters import SearchFilter

from .models import Material


class MaterialSearchFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(filters.FilterSet):
    material_type = filters.ChoiceFilter(
        field_name='material_type',
        choices=Material.TYPE_CHOICES,
    )
    availability = filters.BooleanFilter(
        field_name='availability',
        label='Availability',
    )

    class Meta:
        model = Material
        fields = ['type', 'availability']
