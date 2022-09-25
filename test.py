import unittest

import requests


class TestStringMethods(unittest.TestCase):

    def test_request(self):
        request = requests.get('https://google.com')
        self.assertEqual(request.status_code, 200)

    def test_request_crawl(self):
        session_id = input()
        url = 'https://p.eagate.573.jp/game/gfdm/gitadora_highvoltage/p/playdata/music_detail.html?' \
              'gtype=gf&cat=&sid=2&index=2&page=1'
        request = requests.get(url=url, cookies={'M573SSID': session_id})
        print(request.text)
        self.assertRegex(request.text, r'1/n')


if __name__ == '__main__':
    unittest.main()
