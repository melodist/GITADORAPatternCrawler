import unittest

import requests
from bs4 import BeautifulSoup


def request(session_id, url):
    return requests.get(url=url, cookies={'M573SSID': session_id})


class TestStringMethods(unittest.TestCase):

    def test_request(self):
        request = requests.get('https://google.com')
        self.assertEqual(request.status_code, 200)

    def test_request_crawl(self):
        session_id = '36565579-b2bd-456f-a32f-eb3973bdf34d'
        url = 'https://p.eagate.573.jp/game/gfdm/gitadora_highvoltage/p/playdata/music_detail.html?' \
              'gtype=gf&cat=&sid=2&index=2&page=1'
        request = requests.get(url=url, cookies={'M573SSID': session_id})
        print(request.text)
        self.assertRegex(request.text, r'1/n')

    def test_beautiful_soup(self):
        session_id = '36565579-b2bd-456f-a32f-eb3973bdf34d'
        url = 'https://p.eagate.573.jp/game/gfdm/gitadora_highvoltage/p/playdata/music_detail.html?' \
              'gtype=gf&cat=&sid=2&index=2&page=1'
        r = request(session_id, url)
        bs = BeautifulSoup(r.text, 'html.parser')
        tag = bs.find('div', attrs={'class': 'live_title'})
        [print(s) for s in tag.strings]
        self.assertIn("1/n", tag.strings)


if __name__ == '__main__':
    unittest.main()
