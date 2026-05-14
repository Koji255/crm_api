from rest_framework import pagination

class DefaultLimitOffsetPagination(pagination.LimitOffsetPagination):
    default_limit = 25
    max_limit = 100

class LargeDataSetPagination(pagination.CursorPagination):
    #for deals, contracts etc
    page_size = 100 # default page size
    page_size_query_param = 'page_size' # defines the parameter to specify custom page size for client: GET /deals/?page_size=100
    max_page_size=500
    ordering='-created_at'