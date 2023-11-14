from rest_framework.pagination import PageNumberPagination


class CustomPaginator(PageNumberPagination):
    """Пагинатор для отображения 6 объектов на странице."""
    page_size = 6
    page_size_query_param = 'limit'
