from rest_framework.pagination import PageNumberPagination as Pagination


class PageNumberPagination(Pagination):
    # Client can control the page size using this query parameter.
    # Default is 'None'. Set to eg 'page_size' to enable usage.
    page_size_query_param = 'page_size'

    # Set to an integer to limit the maximum page size the client may request.
    # Only relevant if 'page_size_query_param' has also been set.
    max_page_size = 50

    def __init__(self):
        super(PageNumberPagination, self).__init__()
