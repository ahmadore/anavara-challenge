import math
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class PageSizeAndNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        effective_page_size = int(self.request.query_params.get('page_size', self.page_size))
        page_resp = super().get_paginated_response(data)
        page_obj = page_resp.data
        num_of_pages = math.ceil(page_obj['count'] / effective_page_size)
        resp_dct = {'number_of_pages': num_of_pages}
        page_obj['number_of_pages'] = num_of_pages
        resp_dct.update(page_obj)
        return Response(resp_dct)
