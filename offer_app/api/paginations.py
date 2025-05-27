# Third-party suppliers
from rest_framework.pagination import PageNumberPagination


class OfferPagination(PageNumberPagination):
    """
    Controls page size and limits for offers.
    """
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 20
