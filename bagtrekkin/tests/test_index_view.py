from django.test import TestCase


class IndexViewTestCase(TestCase):

    def test_index_ok(self):
        with self.assertTemplateUsed('index.jade'):
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
