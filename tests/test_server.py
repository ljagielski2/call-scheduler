
from server import app
import unittest


class TestServer(unittest.TestCase):
    def setUp(self):
        print('Setup running')

    def test_admin_get(self):
        response = app.test_client().get('/admin')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
