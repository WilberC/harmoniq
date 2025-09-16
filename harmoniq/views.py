"""
Views for the harmoniq project.
"""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView


@require_http_methods(["GET"])
def health_check(request):
    """
    Simple health check endpoint to verify the application is running.
    """
    return JsonResponse(
        {
            "status": "healthy",
            "service": "harmoniq",
            "version": "1.0.0",
        }
    )


class IndexView(TemplateView):
    """
    Render the index template.
    """

    template_name = "index.html"


class V1View(TemplateView):
    """
    Render the v1 template.
    """

    template_name = "v1/index_v1.html"


class V2View(TemplateView):
    """
    Render the v2 template.
    """

    template_name = "v2/index_v2.html"
