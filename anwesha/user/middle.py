class DisableCSRFMiddleware:
    """
    Middleware class to disable CSRF (Cross-Site Request Forgery) checks for all requests.

    This middleware is used when CSRF protection needs to be bypassed for specific use cases.

    Use Case:
    - Some API endpoints or views may require bypassing CSRF checks for specific purposes.
    - By using this middleware, CSRF checks will be disabled for all requests.

    Note:
    - Bypassing CSRF protection should be done with caution and only for valid reasons.
    - Disabling CSRF checks can expose the application to potential security risks.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        response = self.get_response(request)
        return response
