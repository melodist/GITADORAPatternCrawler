import unittest

import crawler


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.crawler = crawler.Crawler()

    def test_not_exist_song(self):
        exist_url = 'https://p.eagate.573.jp/game/gfdm/gitadora_highvoltage/p/playdata/music_detail.html?' \
                    'gtype=gf&cat=&sid=2&index=3&page=1'
        not_exist_url = "https://p.eagate.573.jp/game/gfdm/gitadora_highvoltage/p/playdata/music_detail.html?" \
                        "gtype=&sid=2&index=22&cat=&page=1"

        error_msg_class = "common_tb_frame_black"

        bs1 = self.crawler.get_music_data(exist_url)
        bs2 = self.crawler.get_music_data(not_exist_url)

        self.assertTrue(not bs1.find("div", class_=error_msg_class))
        self.assertFalse(not bs2.find("div", class_=error_msg_class))

    def test_song_crawl(self):
        result = self.crawler.crawl_song_data(0, 2)

        self.assertEqual(result['title'], "1/n")
        self.assertCountEqual(result["levels"]["BASIC"], ["3.75", "4.10"])
        self.assertCountEqual(result["levels"]["ADVANCED"], ["5.70", "5.15"])
        self.assertCountEqual(result["levels"]["EXTREME"], ["7.25", "5.85"])

    def test_crawl_songs_for_one_char(self):
        songs = self.crawler.crawl_songs_for_one_char(0)
        self.assertEqual(len(songs), 22)

    def test_songs_to_csv(self):
        levels = {'BASIC': '8.75', 'ADVANCED': '9.20', 'EXTREME': '9.45', 'MASTER': '9.98'}
        songs = [{'title': 'test', 'levels': levels}]
        self.crawler.songs_to_csv('test.csv', songs)

    def test_songs_to_csv_with_unicode(self):
        levels = {'BASIC': '8.75', 'ADVANCED': '9.20', 'EXTREME': '9.45', 'MASTER': '9.98'}
        songs = [{'title': 'テスト', 'levels': levels}]
        self.crawler.songs_to_csv('test.csv', songs)


if __name__ == '__main__':
    unittest.main()
