import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/get_data/populer', methods=['GET'])
def test_get():

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    url = "https://www.bilibili.tv/id/popular"

    data = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    
    # Using select
    populars = soup.select("li > .bstar-video-card")
    # Looping through the movies
    data_populer = []
    for soup in populars:
        title = soup.select_one("div > p > a").text.strip()
        channel_image_tmp = soup.find('img', class_='bstar-avatar__image')['src']
        channel_image_tmp = channel_image_tmp.split('@')
        channel_image = channel_image_tmp[0]
        channel_name = soup.select_one(".bstar-video-card__nickname").text.strip()
        cover_tmp = soup.find('img', class_='bstar-video-card__cover-img')['src']
        cover_tmp = cover_tmp.split('@')
        cover = cover_tmp[0]

        url_video_tmp = soup.select_one('.bstar-video-card__cover > a')['href']
        url_video = url_video_tmp.replace("//","")

        viewers_tmp = soup.select_one(".bstar-video-card__desc").text.strip()
        viewers = viewers_tmp.replace("Â·","")

        data_populer.append({
            "title" : title,
            "url" : url_video,
            "channel_image" : channel_image,
            "channel_name" : channel_name,
            "viewers" : viewers,
            "cover" : cover
        })
    return jsonify(data_populer)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)