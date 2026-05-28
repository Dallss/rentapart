from rest_framework.pagination import LimitOffsetPagination

class DefaultPagination(LimitOffsetPagination):
   default_limit = 12
   max_limit = 70

class BigPagination(LimitOffsetPagination):
   default_limit = 50
   max_limit = 100