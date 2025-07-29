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

    def get_context_data(self, **kwargs):
        """
        Add context data to the template.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Harmoniq"
        return context
