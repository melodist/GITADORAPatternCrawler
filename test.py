import unittest

import requests


class TestStringMethods(unittest.TestCase):

    def test_request(self):
        request = requests.get('https://google.com')
        self.assertEqual(request.status_code, 200)


if __name__ == '__main__':
    unittest.main()
