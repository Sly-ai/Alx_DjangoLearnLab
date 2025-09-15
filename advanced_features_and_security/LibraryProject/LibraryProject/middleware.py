# LibraryProject/middleware.py
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    """
    Adds a Content-Security-Policy header constructed from settings.CSP_POLICY dict.
    Use settings.CSP_POLICY to tune allowed sources.
    """
    def _build_csp(self):
        policy = getattr(settings, "CSP_POLICY", {})
        parts = []
        for directive, sources in policy.items():
            if isinstance(sources, (list, tuple)):
                parts.append(f"{directive} {' '.join(sources)}")
            else:
                parts.append(f"{directive} {sources}")
        return "; ".join(parts)

    def process_response(self, request, response):
        csp_header = self._build_csp()
        if csp_header:
            response.setdefault("Content-Security-Policy", csp_header)
        return response
