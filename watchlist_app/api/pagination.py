from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination

class WatchlistPagination(PageNumberPagination):
    page_size = 3
    # page_query_param ='p' #custom page name means instead of page it shows p 
    page_size_query_param = 'size' # client to set the page size on a per-request basis
    max_page_size  = 10
    # last_page_strings = 'end'
    
class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'start'
    
class WatchListCPagination(CursorPagination):
    page_size = 5
    ordering = 'created_at'
    cursor_query_param = 'record'