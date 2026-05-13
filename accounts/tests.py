from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import MANAGE_LEASES_PERMISSION

User = get_user_model()


class GoogleAuthViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_missing_google_client_id_returns_503(self):
        with override_settings(GOOGLE_CLIENT_ID=""):
            r = self.client.post("/api/auth/google/", {"id_token": "x"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)

    @override_settings(GOOGLE_CLIENT_ID="test-client.apps.googleusercontent.com")
    @patch("accounts.views.google_id_token.verify_oauth2_token")
    def test_google_login_creates_user_and_returns_tokens(self, mock_verify):
        mock_verify.return_value = {
            "sub": "google-sub-1",
            "email": "newuser@example.com",
            "email_verified": True,
        }
        r = self.client.post("/api/auth/google/", {"id_token": "fake.jwt"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertIn("access", r.data)
        self.assertIn("refresh", r.data)
        self.assertNotIn("needs_role", r.data)
        self.assertEqual(r.data["user"]["email"], "newuser@example.com")
        caps = r.data["user"]["capabilities"]["leasing"]
        self.assertTrue(caps["lessee"])
        self.assertFalse(caps["manage"])
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    @override_settings(GOOGLE_CLIENT_ID="test-client.apps.googleusercontent.com")
    @patch("accounts.views.google_id_token.verify_oauth2_token")
    def test_invalid_token_returns_400(self, mock_verify):
        mock_verify.side_effect = ValueError("bad token")
        r = self.client.post("/api/auth/google/", {"id_token": "bad"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)


class GrantLeaseManagementViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="r@example.com",
            username="ruser",
            password="not-used-for-api",
        )
        access = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    def test_grant_manage_leases(self):
        self.assertFalse(self.user.has_perm(MANAGE_LEASES_PERMISSION))
        r = self.client.post("/api/auth/capabilities/leasing/manage/", {}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertTrue(r.data["capabilities"]["leasing"]["manage"])
        u = User.objects.get(pk=self.user.pk)
        self.assertTrue(u.has_perm(MANAGE_LEASES_PERMISSION))

    def test_grant_manage_leases_idempotent(self):
        self.client.post("/api/auth/capabilities/leasing/manage/", {}, format="json")
        r2 = self.client.post("/api/auth/capabilities/leasing/manage/", {}, format="json")
        self.assertEqual(r2.status_code, status.HTTP_200_OK)
        self.assertTrue(r2.data["capabilities"]["leasing"]["manage"])
