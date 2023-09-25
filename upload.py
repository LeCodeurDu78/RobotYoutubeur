import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tiktok_uploader.auth import AuthBackend
from googleapiclient.http import MediaFileUpload

def upload_youtube(youtube, titles, nb_videos):
    for i in range(nb_videos):
        request_body = {
            "part": "snippet,status",
            "snippet": {
                "categoryId": 22,
                "title": titles[i],
                "description": titles[i]
            },
            "status": {
                "privacyStatus": "public"
            }
        }

        print(titles[i])

        media_file = MediaFileUpload(f"Videos/{titles[i]}.mp4")
        video = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media_file).execute()

        print("Video uploaded successfully. Video ID:", video["id"], "\n")

def upload_tiktok(titles, nb_videos):
    for i in range(nb_videos):
        driver = webdriver.Chrome()

        auth = AuthBackend(cookies="client/cookies.txt")
        driver = auth.authenticate_agent(driver)

        driver.get("https://www.tiktok.com/creator-center/upload")

        time.sleep(20)

        iframe = driver.find_element(By.TAG_NAME, 'iframe')
        driver.switch_to.frame(iframe)

        input_file = driver.find_element(By.CLASS_NAME, 'jsx-2751257330 ')
        input_file.send_keys(f"/home/adamrespeliers/Code/projet-python/RobotYoutubeur/Videos/Who did it better?😍 #elsarca #tiktok : Best Moments.mp4")

        WebDriverWait(driver, 120).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "uploading-container"))
        )

        next_button = driver.find_element(By.TAG_NAME, "button")
        next_button.click()

        driver.quit()

def upload(youtube, titles, nb_videos):
    upload_youtube(youtube, titles, nb_videos)
    #upload_tiktok(titles, nb_videos)