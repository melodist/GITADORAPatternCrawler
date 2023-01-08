import csv
import unittest

import csvdiff
import requests
from bs4 import BeautifulSoup


def get_request(session_id, url):
    return requests.get(url=url, cookies={'M573SSID': session_id})


def read_session_id():
    f = open("session_id.txt", "r", encoding="utf-8")
    session_id = f.read()
    f.close()
    return session_id


class MyTestCase(unittest.TestCase):
    def test_request(self):
        request = requests.get('https://google.com')
        self.assertEqual(request.status_code, 200)

    def test_request_crawl(self):
        session_id = read_session_id()
        home_url = 'https://p.eagate.573.jp/game/gfdm/gitadora_highvoltage/s/playdata/music.html'
        url = 'https://p.eagate.573.jp/game/gfdm/gitadora_highvoltage/p/playdata/music_detail.html?' \
              'gtype=gf&cat=&sid=2&index=2&page=1'

        requests.get(url=home_url, cookies={'M573SSID': session_id})
        request = requests.get(url=url, cookies={'M573SSID': session_id})
        print(request.text)
        self.assertRegex(request.text, r'1/n')

    def test_beautiful_soup(self):
        session_id = read_session_id()

        home_url = 'https://p.eagate.573.jp/game/gfdm/gitadora_highvoltage/s/playdata/music.html'
        url = 'https://p.eagate.573.jp/game/gfdm/gitadora_highvoltage/p/playdata/music_detail.html?' \
              'gtype=gf&cat=&sid=2&index=2&page=1'

        requests.get(url=home_url, cookies={'M573SSID': session_id})
        r = get_request(session_id, url)

        bs = BeautifulSoup(r.text, 'html.parser')
        title = bs.find('div', attrs={'class': 'live_title'})
        print(title.string)
        diff = bs.find_all('div', attrs={'class': 'diff_area'})
        [print(s.string) for s in diff]
        self.assertIn("1/n", title.strings)

    def test_session_id_reader(self):
        with open("test.txt", "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "test")


class CsvDiffTest(unittest.TestCase):
    def test_csvdiff(self):
        with open("result.csv", 'r', encoding='UTF-8') as f:
            with open("result_old.csv", 'r', encoding='UTF-8') as f_old:
                r = csv.DictReader(f)
                r_old = csv.DictReader(f_old)

                patch = csvdiff.diff_records(r_old, r, ['title', 'diff']);
                print(patch['added'])
                print(patch['removed'])
                print(patch['changed'])


if __name__ == '__main__':
    unittest.main()
