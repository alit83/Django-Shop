

class NoIndexMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        noindex_paths = [
            "/dashboard/",
            "/cart/",
            "/order/",
            "/admin/",
        ]
        if any(request.path.startswith(path) for path in noindex_paths):
            response["X-Robots-Tag"] = "noindex"

        return response
