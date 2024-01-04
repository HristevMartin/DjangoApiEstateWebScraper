# pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 8  # Default to 10 items per page
    page_size_query_param = (
        "page_size"  # Allow client to override, using `?page_size=20`
    )
    max_page_size = 1000  # Maximum limit allowed when using `page_size_query_param`

    def get_paginated_response(self, data):
        return Response(
            {
                "total_items": self.page.paginator.count,
                "next_link": self.get_next_link(),
                "prev_link": self.get_previous_link(),
                "data": data,
            }
        )
