import yt_dlp
from youtubesearchpython import VideosSearch
import os
import csv

def SearchVideos():
    urls = []
    with open("songs.csv", "r") as file:
        reader = csv.reader(file)
        # Skip the header line
        next(reader)
        
        for row in reader:
            song_title = row[0].strip()
            print(f"Searching for: {song_title}")
        
            search_query = song_title
            
            # Perform the video search
            videossearch = VideosSearch(search_query, limit=4)
            results = videossearch.result()['result']
            
            # Loop through the search results
            official_audio_found = False

            for video in results:
                if "Official Audio" in video['title']:
                    url = video['link']
                    print(url)
                    official_audio_found = True
                    urls.append(url)
                    break  # Stop looking for other official audios if one is found

            if not official_audio_found and results:
                url = results[0]['link']
                urls.append(url)

    print(urls)
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
