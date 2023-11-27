from rest_framework import pagination
from rest_framework.response import Response


class SensorDataRecordIntervalPagination(pagination.PageNumberPagination):
    page_size = 100
    
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': {
                'start_date': data['start_date'],
                'end_date': data['end_date'],
                'records': data['records']
            }
        })
