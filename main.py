# type: ignore
import os
import pickle
from upload import upload
from montage import montage
from download import download
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def authenticate(i):
    credentials = None

    if os.path.exists(f"token/token{i}.pickle"):
        with open(f"token/token{i}.pickle", 'rb') as token:
            credentials = pickle.load(token)

    #  Check if the credentials are invalid or do not exist
    if not credentials or not credentials.valid:

        # Check if the credentials have expired
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        else:
            # else auth by google
            flow = InstalledAppFlow.from_client_secrets_file(
                f"client/client{i}.json", ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.force-ssl"])
            credentials = flow.run_local_server(port=0)

        # Save the credentials into the pickle for the next run
        with open(f"token/token{i}.pickle", 'wb') as token:
            pickle.dump(credentials, token) 

    return build("youtube", "v3", credentials=credentials)

if __name__ == "__main__":
    api_number = 2
    nb_videos = 5

    for i in range(api_number):
        youtube = authenticate(i)
        titles, secondsVideos = download(youtube, nb_videos, i)
        print("download  fini")
        
        montage(nb_videos, secondsVideos)
        print("montage fini")
    
        try :
            upload(youtube, titles, nb_videos)
            print("upload fini")
        except:
            upload(youtube, titles, nb_videos)
            print("upload fini")

        for title in titles:
            os.remove(f"Videos/{title}.mp4")