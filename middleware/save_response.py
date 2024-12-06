from django.utils.deprecation import MiddlewareMixin

class SaveResponseMiddleware(MiddlewareMixin):
    """
    Middleware برای ذخیره Response جاری در request.META
    """
    def process_response(self, request, response):
        request.META['_response'] = response
        return response