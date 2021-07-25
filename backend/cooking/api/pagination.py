from rest_framework import pagination
from rest_framework.response import Response


class CustomPaginationIdeas(pagination.PageNumberPagination):
    page_size = 3
    max_page_size = 5

    # custom (based on docs) next+previous = will be sent not as 2 separ links
    # but as object likns:{next,prev}

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'prev': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })