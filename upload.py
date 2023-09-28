import pynput
import time
import pyautogui
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

        media_file = MediaFileUpload(f"Videos/{titles[i]}.mp4")
        video = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media_file).execute()
        print(titles[i])
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
        driver.execute_script("arguments[0].style.display = 'block';", input_file)
        
        input_file.click()
        
        time.sleep(2)

        file_path = f"/home/adamrespeliers/Code/projet-python/RobotYoutubeur/Videos/{titles[i]}.mp4"
        
        for c in file_path:
            pynput.keyboard.Controller().press(c)
            time.sleep(0.1)
            pynput.keyboard.Controller().release(c)

        pyautogui.press('enter')

        WebDriverWait(driver, 120).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "uploading-container"))
        )

        time.sleep(30)

        next_button = WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "css-y1m958"))
        )

        next_button.click()

        time.sleep(5)

        driver.quit()

def upload(youtube, titles, nb_videos):
    #upload_youtube(youtube, titles, nb_videos)
    upload_tiktok(titles, nb_videos)