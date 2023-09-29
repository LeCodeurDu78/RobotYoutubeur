from os import remove
from upload import upload
from montage import montage
from download import download
from authenticate import authenticate

if __name__ == "__main__":
    api_number = 2
    nb_videos = 5

    for i in range(api_number):
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

        for i in range(len(titles)):
            remove(f"Videos/{titles[i]}.mp4") 
            remove(f"Videos/youtube{i}_all.mp4")