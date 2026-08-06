from django.urls import reverse
from rest_framework.test import APITestCase


class PagePulseTests(APITestCase):

    def test_empty_url(self):

        response = self.client.post(
            "/analyze/",
            {"url": ""},
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_invalid_url(self):

        response = self.client.post(
            "/analyze/",
            {"url": "abcd1234"},
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_google(self):

        response = self.client.post(
            "/analyze/",
            {"url": "https://google.com"},
            format="json"
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn("seo_score", response.data)

        self.assertIn("status", response.data)

        self.assertIn("title", response.data)

    def test_python(self):

        response = self.client.post(
            "/analyze/",
            {"url": "https://python.org"},
            format="json"
        )

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            response.data["seo_score"] >= 0
        )

    def test_https_added(self):

        response = self.client.post(
            "/analyze/",
            {"url": "github.com"},
            format="json"
        )

        self.assertEqual(response.status_code, 200)