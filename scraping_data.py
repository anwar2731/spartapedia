import requests
from bs4 import BeautifulSoup


# Read the URL and get the HTML,
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

# You will be scraping the data from this page
url = "https://www.bilibili.tv/id/popular"

# Use the requests library to get the HTML code at the url above
data = requests.get(url=url, headers=headers)

# The BeautifulSoup library makes it easy to
# parse HTML code
soup = BeautifulSoup(data.text, 'html.parser')

# Using select
populars = soup.select("li > .bstar-video-card")
# # Looping through the movies
data_populars = []
for soup in populars:
    # First, let's get the title of the movie
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

    data_populars.append({
        "title" : title,
        "url" : url_video,
        "channel_image" : channel_image,
        "channel_name" : channel_name,
        "viewers" : viewers,
        "cover" : cover
    })
    
print(data_populars)

# print(anime)