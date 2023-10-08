import os
import pickle
import subprocess
import webbrowser
from time import sleep
from threading import Thread
from pyautogui import scroll, click
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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
                os.remove(f"token/token{i}.pickle")
                authenticate(i)

        else:
            # else auth by google
            flow = InstalledAppFlow.from_client_secrets_file(
                f"client/client{i}.json", ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.force-ssl"])
                        
            thread = Thread(target=run_local_server, args=(flow,))
            thread.start()
                
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("/usr/bin/google-chrome"))
            webbrowser.get('chrome').open_new(flow.authorization_url(prompt='select_account')[0])

            chrome_class_name = "google-chrome"
            sleep(4)
            window_id = subprocess.check_output(["xdotool", "search", "--class", chrome_class_name]).strip()

            if window_id:
                subprocess.Popen(["xdotool", "windowactivate", window_id])
        
            pyautogui_connect()

            thread.join()

            if window_id:
                subprocess.Popen(["google-chrome", "--kill"])

            credentials = flow.credentials

            with open(f"token/token{i}.pickle", 'wb') as token: # type: ignore
                pickle.dump(credentials, token) 

    return build("youtube", "v3", credentials=credentials)

def pyautogui_connect():
    sleep(7)
    print("je me connecte en tant que Pierre")
    click(564, 445)

    sleep(7)
    print("Je me connecte avec la chaine youtube")
    click(564, 445)
    
    sleep(5)
    print("j'authorise mon code a accéder a ma chaine youtube")
    click(489, 427)
    
    sleep(5)
    print("je valide les trucs") 
    scroll(-30)
    sleep(1)
    click(718, 512)
    
    sleep(2)