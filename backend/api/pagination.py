from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """ Параметры пагинации: размер страницы и максимальный размер. """
    page_size = 8
    page_size_query_param = 'limit'
    max_page_size = 100
