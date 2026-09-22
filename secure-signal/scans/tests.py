from django.contrib.auth import get_user_model
from django.test import Client, SimpleTestCase, TestCase
from .detector import analyze
from .models import Scan


class DetectorTests(SimpleTestCase):
    def test_benign(self):
        self.assertEqual(analyze("Meet at the library tomorrow")["score"], 0)

    def test_normalization_and_repeated_signals(self):
        self.assertEqual(analyze("ＵＲＧＥＮＴ enter your pass\u200bword immediately immediately")["score"], 5)

    def test_limits(self):
        for value in (None, "", " ", "x" * 5001):
            with self.assertRaises(ValueError):
                analyze(value)
        self.assertEqual(analyze("x" * 5000)["score"], 0)


class AccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.alice = get_user_model().objects.create_user(username="alice")
        cls.bob = get_user_model().objects.create_user(username="bob")
        cls.scan = Scan.objects.create(owner=cls.alice, score=4, level="Alice-only result", signals=[])

    def test_anonymous_redirected(self):
        for url in ("/", f"/scans/{self.scan.pk}/"):
            self.assertEqual(self.client.get(url).status_code, 302)

    def test_owner_can_read(self):
        self.client.force_login(self.alice)
        self.assertContains(self.client.get(f"/scans/{self.scan.pk}/"), "Alice-only result")

    def test_other_user_cannot_read(self):
        self.client.force_login(self.bob)
        self.assertEqual(self.client.get(f"/scans/{self.scan.pk}/").status_code, 404)

    def test_other_user_cannot_delete(self):
        self.client.force_login(self.bob)
        self.assertEqual(self.client.post(f"/scans/{self.scan.pk}/delete/").status_code, 404)
        self.assertTrue(Scan.objects.filter(pk=self.scan.pk).exists())

    def test_history_is_scoped(self):
        self.client.force_login(self.bob)
        self.assertNotContains(self.client.get("/"), "Alice-only result")

    def test_owner_is_not_client_controlled(self):
        self.client.force_login(self.bob)
        response = self.client.post("/", {"message": "hello", "owner": self.alice.pk})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Scan.objects.first().owner_id, self.bob.pk)
        self.assertNotIn("message", [field.name for field in Scan._meta.fields])

    def test_invalid_input_not_saved(self):
        self.client.force_login(self.alice)
        for message in ("", " ", "x" * 5001):
            self.client.post("/", {"message": message})
        self.assertEqual(Scan.objects.count(), 1)

    def test_csrf_required_for_create_delete_and_login(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.alice)
        for url in ("/", f"/scans/{self.scan.pk}/delete/", "/login/"):
            self.assertEqual(client.post(url, {"message": "hello"}).status_code, 403)

    def test_valid_csrf_and_owner_delete(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.alice)
        client.get("/")
        token = client.cookies["csrftoken"].value
        self.assertEqual(client.post(f"/scans/{self.scan.pk}/delete/", {"csrfmiddlewaretoken": token}).status_code, 302)
        self.assertFalse(Scan.objects.filter(pk=self.scan.pk).exists())

    def test_get_cannot_delete(self):
        self.client.force_login(self.alice)
        self.assertEqual(self.client.get(f"/scans/{self.scan.pk}/delete/").status_code, 405)
        self.assertTrue(Scan.objects.filter(pk=self.scan.pk).exists())

    def test_template_escapes_untrusted_data(self):
        self.scan.level = '<script>alert("x")</script>'
        self.scan.save()
        self.client.force_login(self.alice)
        response = self.client.get(f"/scans/{self.scan.pk}/")
        self.assertNotContains(response, "<script>")
        self.assertContains(response, "&lt;script&gt;")

    def test_headers(self):
        response = self.client.get("/login/")
        self.assertEqual(response["Cache-Control"], "no-store")
        self.assertEqual(response["X-Frame-Options"], "DENY")
        self.assertIn("form-action 'self'", response["Content-Security-Policy"])

    def test_login_and_logout(self):
        import secrets
        password = secrets.token_urlsafe(24)
        self.alice.set_password(password)
        self.alice.save()
        self.assertFalse(self.client.login(username="alice", password="wrong"))
        self.assertTrue(self.client.login(username="alice", password=password))
        self.assertEqual(self.client.post("/logout/").status_code, 302)
        self.assertEqual(self.client.get("/").status_code, 302)
