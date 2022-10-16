import unittest

import requests
import main
from bs4 import BeautifulSoup


def get_request(session_id, url):
    return requests.get(url=url, cookies={'M573SSID': session_id})


def read_session_id():
    f = open("session_id.txt", "r", encoding="utf-8")
    session_id = f.read()
    f.close()
    return session_id


class TestStringMethods(unittest.TestCase):

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

    def test_not_exist_song(self):
        session_id = read_session_id()
        exist_url = 'https://p.eagate.573.jp/game/gfdm/gitadora_highvoltage/p/playdata/music_detail.html?' \
              'gtype=gf&cat=&sid=2&index=3&page=1'
        not_exist_url = "https://p.eagate.573.jp/game/gfdm/gitadora_highvoltage/p/playdata/music_detail.html?" \
              "gtype=&sid=2&index=22&cat=&page=1"

        error_msg_class = "common_tb_frame_black"

        bs1 = main.get_music_data(session_id, exist_url)
        bs2 = main.get_music_data(session_id, not_exist_url)

        self.assertTrue(not bs1.find("div", class_=error_msg_class))
        self.assertFalse(not bs2.find("div", class_=error_msg_class))

    def test_song_crawl(self):
        session_id = read_session_id()
        url = 'https://p.eagate.573.jp/game/gfdm/gitadora_highvoltage/p/playdata/music_detail.html?' \
              'gtype=gf&cat=&sid=2&index=2&page=1'

        data = main.get_music_data(session_id, url)
        result = main.crawl_song_data(data)

        self.assertEqual(result['title'], "1/n")
        self.assertCountEqual(result["levels"]["BASIC"], ["3.75", "4.10"])
        self.assertCountEqual(result["levels"]["ADVANCED"], ["5.70", "5.15"])
        self.assertCountEqual(result["levels"]["EXTREME"], ["7.25", "5.85"])

    def test_crawl_songs_for_one_char(self):
        songs = main.crawl_songs_for_one_char(read_session_id(), 0)
        self.assertEqual(len(songs), 22)

    def test_songs_to_csv(self):
        levels = {'BASIC': '8.75', 'ADVANCED': '9.20', 'EXTREME': '9.45', 'MASTER': '9.98'}
        songs = [{'title': 'test', 'levels': levels}]
        main.songs_to_csv('test.csv', songs)

    def test_session_id_reader(self):
        with open("test.txt", "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "test")


if __name__ == '__main__':
    unittest.main()
