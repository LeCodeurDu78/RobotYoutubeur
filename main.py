import os
import time
import pickle
import threading
import pyautogui
import subprocess
from upload import upload
from montage import montage
from download import download
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import webbrowser

def run_local_server(flow):
    flow.run_local_server(open_browser=False)

def authenticate(i):
    credentials = None

    if os.path.exists(f"token/token{i}.pickle"):
        with open(f"token/token{i}.pickle", 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:

        # Check if the credentials have expired
        if credentials and credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
            except:
                os.remove("token/token{i}.pickle")
                authenticate(i)

        else:
            # else auth by google
            flow = InstalledAppFlow.from_client_secrets_file(
                f"client/client{i}.json", ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.force-ssl"])
                        
            thread = threading.Thread(target=run_local_server, args=(flow,))
            thread.start()
                
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("/usr/bin/google-chrome"))
            webbrowser.get('chrome').open_new(flow.authorization_url(prompt='select_account')[0])

            chrome_class_name = "google-chrome"
            time.sleep(4)
            window_id = subprocess.check_output(["xdotool", "search", "--class", chrome_class_name]).strip()

            if window_id:
                subprocess.Popen(["xdotool", "windowactivate", window_id])
        
            time.sleep(7)
            print("je me connecte en tant que Pierre")
            pyautogui.click(564, 445)

            time.sleep(7)
            print("Je me connecte avec la chaine youtube")
            pyautogui.click(564, 445)

            time.sleep(5)
            print("j'authorise mon code a accéder a ma chaine youtube")
            pyautogui.click(489, 427)

            time.sleep(5)
            print("je valide les trucs") 
            pyautogui.scroll(-30)
            time.sleep(1)
            pyautogui.click(718, 512)

            time.sleep(2)
            
            thread.join()
            if window_id:
                subprocess.Popen(["google-chrome", "--kill"])

            credentials = flow.credentials

            with open(f"token/token{i}.pickle", 'wb') as token: # type: ignore
                pickle.dump(credentials, token) 

    return build("youtube", "v3", credentials=credentials)

if __name__ == "__main__":
    api_number = 2
    nb_videos = 5

    for i in range(api_number - 1):
        youtube = authenticate(i)
        titles, secondsVideos = download(youtube, nb_videos, i)
        print("\nDownload fini\n\n")
        
        try:
            montage(nb_videos, secondsVideos, titles)
            print("Montage fini\n\n")
        except: 
            montage(nb_videos, secondsVideos, titles)
            print("Montage fini\n\n")

        try: 
            upload(youtube, titles, nb_videos)
            print("Upload fini")
        except:
        
        upload(youtube, titles, nb_videos)
        print("Upload fini")