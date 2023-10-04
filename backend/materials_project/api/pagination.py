from rest_framework.pagination import PageNumberPagination


class LimitPageNumberPagination(PageNumberPagination):
    """
    Custom pagination class that limits the number of items per page.

    This pagination class extends the PageNumberPagination provided by
    Django REST framework. It allows clients to specify the desired
    number of items per page using the 'limit' query parameter.

    Attributes:
        page_size (int): Default number of items per page.
        page_size_query_param (str): Name of the query parameter for
            specifying the desired number of items per page.

    Example:
        To request 10 items per page:
        /api/items/?limit=10
    """

    page_size = 6
    page_size_query_param = 'limit'
