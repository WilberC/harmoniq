"""
Tests for the health check endpoint.
"""

import json

from django.test import Client, TestCase
from django.urls import reverse


class HealthCheckTestCase(TestCase):
    """Test cases for the health check endpoint."""

    def setUp(self):
        """Set up test client."""
        self.client = Client()

    def test_health_check_endpoint(self):
        """Test that the health check endpoint returns correct response."""
        response = self.client.get(reverse("health_check"))

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Check content type
        self.assertEqual(response["Content-Type"], "application/json")

        # Parse JSON response
        data = json.loads(response.content)

        # Check response structure
        self.assertIn("status", data)
        self.assertIn("service", data)
        self.assertIn("version", data)

        # Check expected values
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "harmoniq")
        self.assertEqual(data["version"], "1.0.0")

    def test_health_check_method_not_allowed(self):
        """Test that POST requests are not allowed."""
        response = self.client.post(reverse("health_check"))
        self.assertEqual(response.status_code, 405)
