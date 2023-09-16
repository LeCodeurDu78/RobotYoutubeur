from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload

def upload(youtube, titles, nb_videos):
    for i in range(nb_videos):
        request_body = {
            "part": "snippet,status",
            "snippet": {
                "categoryId": 22,
                "title": f"{titles[i]} : Best Moments",
                "description": f"{titles[i]} : Best Moments"
            },
            "status": {
                "privacyStatus": "public"
            }
        }

        print(f"{titles[i]} : Best Moments")

        media_file = MediaFileUpload(f"Videos/youtube{i}.mp4")
        video = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media_file).execute()

        print("Video uploaded successfully. Video ID:", video["id"])