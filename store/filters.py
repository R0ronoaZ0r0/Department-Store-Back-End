from django_filters import rest_framework as filters


class SubcategoryFilter(filters.FilterSet):
    department_number = filters.NumberFilter(field_name='department__department_number')


class ProductFilter(filters.FilterSet):
    department_number = filters.NumberFilter(field_name='department__department_number')
    subcategory_number = filters.NumberFilter(field_name='subcategory__subcategory_number')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    brand = filters.CharFilter(field_name='name', lookup_expr='icontains')
    stock_quantity_gte = filters.NumberFilter(field_name='stock_quantity', lookup_expr='gte')
    stock_quantity_lte = filters.NumberFilter(field_name='stock_quantity', lookup_expr='lte')
    price_gte = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_lte = filters.NumberFilter(field_name='price', lookup_expr='lte')
    average_rating_gte = filters.NumberFilter(field_name='average_rating', lookup_expr='gte')
    average_rating_lte = filters.NumberFilter(field_name='average_rating', lookup_expr='lte')
