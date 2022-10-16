import csv

import requests
from bs4 import BeautifulSoup


def get_request(session_id, url):
    return requests.get(url=url, cookies={'M573SSID': session_id})


def read_session_id():
    with open("session_id.txt", "r", encoding="utf-8") as f:
        return f.read()


def get_music_data(session_id, url):
    home_url = 'https://p.eagate.573.jp/game/gfdm/gitadora_highvoltage/s/playdata/music.html'

    requests.get(url=home_url, cookies={'M573SSID': session_id})
    r = get_request(session_id, url)

    return BeautifulSoup(r.text, 'html.parser')


def crawl_song_data(data):
    title = data.find('div', attrs={'class': 'live_title'}).string

    diffs = ["BASIC", "ADVANCED", "EXTREME", "MASTER"]
    levels = {}
    for d in diffs:
        diff = data.select(f'.diff_{d} > .diff_area')
        levels[d] = [level.string for level in diff]

    song = {"title": title, "levels": levels}
    return song


def crawl_songs_for_one_char(session_id, char_index):
    error_msg_class = "common_tb_frame_black"

    songs = []
    i = 0
    while True:
        url = 'https://p.eagate.573.jp/game/gfdm/gitadora_highvoltage/p/playdata/music_detail.html?' \
              f'gtype=gf&cat={char_index}&sid=2&index={i}&page=1'

        print(url)
        data = get_music_data(session_id, url)
        if data.find("div", class_=error_msg_class):
            break

        songs.append(crawl_song_data(data))
        i += 1

    return songs


def songs_to_csv(filename, songs):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['title', 'diff', 'level']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for song in songs:
            [writer.writerow({'title': song['title'], 'diff': diff, 'level': level}) for (diff, level) in song['levels'].items()]


def run():
    print('GITADORA Pattern Crawler start')


if __name__ == '__main__':
    run()
