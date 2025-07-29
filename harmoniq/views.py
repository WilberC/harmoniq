"""
Views for the harmoniq project.
"""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


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