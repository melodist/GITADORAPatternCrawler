import csv

import requests
from bs4 import BeautifulSoup
from time import sleep


class Crawler:
    def __init__(self, request_delay=0.2):
        print('GITADORA Pattern Crawler start')
        self.session_id = self.read_session_id()
        self.request_delay = request_delay

    @staticmethod
    def read_session_id():
        with open("session_id.txt", "r", encoding="utf-8") as f:
            return f.read()

    def get_request(self, url):
        sleep(self.request_delay)
        return requests.get(url=url, cookies={'M573SSID': self.session_id})

    def post_category_request(self, char_index):
        url = 'https://p.eagate.573.jp/game/gfdm/gitadora_highvoltage/s/playdata/music.html'
        requests.post(url=url, cookies={'M573SSID': self.session_id}, data={'cat': char_index})

    def get_music_data(self, url):
        home_url = 'https://p.eagate.573.jp/game/gfdm/gitadora_highvoltage/s/playdata/music.html'

        requests.get(url=home_url, cookies={'M573SSID': self.session_id})
        r = self.get_request(url)

        return BeautifulSoup(r.text, 'html.parser')

    def crawl_song_data(self, char_index, i):
        url = 'https://p.eagate.573.jp/game/gfdm/gitadora_highvoltage/p/playdata/music_detail.html?' \
              f'gtype=gf&cat={char_index}&sid=2&index={i}&page=1'

        error_msg_class = "common_tb_frame_black"

        print(url)
        retry_cnt = 0

        data = None
        while retry_cnt < 5:
            data = self.get_music_data(url)
            if data.find("div", class_=error_msg_class):
                return
            elif not data.find('div', attrs={'class': 'live_title'}):
                if retry_cnt < 5:
                    retry_cnt += 1
                    sleep(1)
                    print(f'Song Data Empty retry_cnt: {retry_cnt}')
                    continue
                else:
                    print('Song Data Request Error')
                    raise ConnectionError
            else:
                break

        title = data.find('div', attrs={'class': 'live_title'}).string

        diffs = ["BASIC", "ADVANCED", "EXTREME", "MASTER"]
        levels = {}
        for d in diffs:
            diff = data.select(f'.diff_{d} > .diff_area')
            levels[d] = [level.string for level in diff]

        song = {"title": title, "levels": levels}
        return song

    def crawl_songs_for_one_char(self, char_index):
        print(f'Request for index {char_index}')
        self.post_category_request(char_index)

        songs = []
        i = 0
        while True:
            data = self.crawl_song_data(char_index, i)
            if data:
                songs.append(data)
                i += 1
            else:
                break

        return songs

    def crawl_songs_for_all_chars(self):
        songs = []
        for i in range(0, 37):
            songs += self.crawl_songs_for_one_char(i)

        return songs

    @staticmethod
    def songs_to_csv(filename, songs):
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'diff', 'level']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for song in songs:
                [writer.writerow({'title': song['title'], 'diff': diff, 'level': level}) for (diff, level) in
                 song['levels'].items()]


def run():
    crawler = Crawler()

    print('Get session id')
    songs = crawler.crawl_songs_for_all_chars()

    print('Print result to csv')
    crawler.songs_to_csv('result.csv', songs)

    print('GITADORA Pattern Crawler end')


if __name__ == '__main__':
    run()
