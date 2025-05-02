import yt_dlp
import os
import csv
from googleapiclient.discovery import build

def SearchVideos():
    youtube_api_key = ''
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    urls = []
    with open("songs.csv", "r") as file:
        reader = csv.reader(file)
        # Skip the header line
        next(reader)
        
        for row in reader:
            query = row[0].strip()
            print(f"Searching for: {query}")    

            request = youtube.search().list(
                q=query,
                part="snippet",
                type="video",
                maxResults=5
            )

            response = request.execute()

            found = False
            for item in response.get("items", []):
                title = item['snippet']['title'].lower()
                if "lyrics" in title and "music video" not in title:
                    video_id = item['id']['videoId']
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    urls.append(video_url)
                    print(f"Found: {video_url}")
                    found = True
                    break

            # Fallback if nothing matched
            if not found and response.get("items"):
                fallback_id = response["items"][0]["id"]["videoId"]
                fallback_url = f"https://www.youtube.com/watch?v={fallback_id}"
                urls.append(fallback_url)
                print(f"Fallback: {fallback_url}")

    print("Final URLs:", urls)
    return urls
                



def DownloadVideos(urls, download_path):
    print("Now Downloading")
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            try:
                print(f"Downloading: {url}")
                ydl.download([url])
                print(f"Downloaded: {url}")
            except Exception as e:
                print(f"Failed to download {url}. Error: {str(e)}")


def main():
    urls = SearchVideos()
    DownloadVideos(urls, "MusicDownloadsPython")

main()
