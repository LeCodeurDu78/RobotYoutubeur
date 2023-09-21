import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
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

        print(f"{titles[i]} : Best Moments")

        media_file = MediaFileUpload(f"Videos/{titles[i]}.mp4")
        video = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media_file).execute()

        print("Video uploaded successfully. Video ID:", video["id"])

def upload_tiktok(titles, nb_videos):
    for i in range(nb_videos):
        driver = webdriver.Chrome()

        auth = AuthBackend(cookies="client/cookies.txt")
        driver = auth.authenticate_agent(driver)

        driver.get("https://www.tiktok.com/upload")

        file_input_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "input"))
        )
        file_input_button.send_keys(f"Videos/{titles[i]}.mp4")

        WebDriverWait(driver, 120).until(
            EC.invisibility_of_element_located((By.XPATH, "//div[@class='uploading-container']"))
        )

        next_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[2]/div[2]/div[8]/div[2]/button")
        next_button.click()

        driver.quit()

def upload(youtube, titles, nb_videos):
    upload_youtube(youtube, titles, nb_videos)
    upload_tiktok(titles, nb_videos)