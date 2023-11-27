from drf_yasg import openapi, inspectors


class SearchQueryFilterInspector(inspectors.FilterInspector):
    def get_filter_parameters(self, filter_backend):
        result = [openapi.Parameter(
            name='q',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='Search keyword'
        )]
        return result
