import re

from django.test import TestCase


class TestProfiling(TestCase):
    TEST_VIEW_REGEX = re.compile(r"tests/test_urls.py:\d+\(test_view\)")

    def test_profile(self):
        resp = self.client.get(
            "/view",
            data={"SNAKEVIZ_PROFILING": "PLEASE_PROFILE_REQUESTS"},
        )
        self.assertEqual(200, resp.status_code)
        text = resp.content.decode("utf8")

        self.assertTrue(self.TEST_VIEW_REGEX.search(text) is not None)
        self.assertTrue(r'FROM \"auth_user\"' in text)
