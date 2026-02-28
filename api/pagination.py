from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    """
    Default pagination class for limiting queryset size to 20 objects.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
