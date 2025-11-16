# materials/paginators.py
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    """
    Класс пагинации для материалов (курсы, уроки)
    """

    page_size = 6
    page_size_query_param = "page_size"
    max_page_size = 50
