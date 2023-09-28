# type: ignore
from pytubefix import YouTube
import datetime

def get_most_viewed_today(youtube, nb_videos, api_used):
    yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
    yesterday_format = yesterday.strftime("%Y-%m-%d")

    if api_used == 1:
        nb_videos += 5
    elif api_used == 2:
        nb_videos += 10

    response = youtube.search().list(part="id", maxResults=nb_videos, order="viewCount", publishedAfter=f"{yesterday_format}T00:00:00Z").execute()
    if 'items' in response:
        videosId: list[str] = []
        for i in range(nb_videos):
            videosId.append(response['items'][i]['id']['videoId'])
        print(videosId)
        print("\n")
        
        if api_used == 1:
            for _ in range(5):
                videosId.pop(0)
        elif api_used == 2:
            for _ in range(10):
                videosId.pop(0)
        
        return videosId
    return ["erreur"]

def get_titles_videos(youtube, videosId, nb_videos):
    titles = []
    for i in range(nb_videos):
        response = youtube.videos().list(id=videosId[i], part="snippet").execute()
        if len(response['items'][0]['snippet']['title']) < 81:
            titles.append(f"{response['items'][0]['snippet']['title']} : Best Moments")
        else:
            titles.append(f"{response['items'][0]['snippet']['title'][:80]} : Best Moments")
    return titles


def get_most_viewed_moment(youtube, video_id):
    response = youtube.videos().list(part="snippet,statistics,contentDetails", id=video_id).execute()
    if 'items' in response:
        
        statistics = response['items'][0]['statistics']

        view_history = statistics.get('dailyViewCount', [])

        if view_history:
            max_views = max(view_history)
            second_max_views = view_history.index(max_views)
        
            return second_max_views
        else:
            return -1
    return None

def download_video(videosId):
    i = 0
    for id in videosId:
        try: 
            print("je commence à download")
            yt = YouTube(url=f"https://www.youtube.com/watch?v={id}",use_oauth=False, allow_oauth_cache=False)
            yt.streams.get_lowest_resolution().download(output_path="Videos/", filename=f"youtube{i}_all.mp4")
            print("Video download\n")
            i += 1
        except:
            print("je commence à download")
            yt = YouTube(url=f"https://www.youtube.com/watch?v={id}",use_oauth=True, allow_oauth_cache=True)
            yt.streams.get_lowest_resolution().download(output_path="Videos/", filename=f"youtube{i}_all.mp4")
            print("Video download\n")
            i += 1

def download(youtube, nb_videos, api_used):

    videosId: list[str] = get_most_viewed_today(youtube, nb_videos, api_used)
    download_video(videosId)

    titles = get_titles_videos(youtube, videosId, nb_videos)
    print(titles)

    secondsVideos = []
    for videoId in videosId:
        secondsVideos.append(get_most_viewed_moment(youtube, videoId))

    return titles, secondsVideos