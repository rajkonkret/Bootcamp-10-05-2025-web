from django.test import TestCase
from django.urls import reverse
from .models import Post

class PostTests(TestCase):
    def test_list_ok(self):
        Post.objects.create(title="T", body="B")
        r = self.client.get(reverse("post-list"))
        self.assertContains(r, "T")
