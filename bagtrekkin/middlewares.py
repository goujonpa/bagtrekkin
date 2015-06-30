from django import http


class ViewExceptionMiddleware(object):
    '''
    Middleware which handles errors to return
    a formatted JSON if error occures on API side
    '''
    def process_exception(self, request, exception):
        if request.environ.get('CONTENT_TYPE') == 'application/json':
            return http.JsonResponse(
                data={'error': exception.message},
                content_type='application/json',
                status=400,
                charset='utf-8'
            )
