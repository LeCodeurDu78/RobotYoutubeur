import os
from upload import upload
from montage import montage
from download import download
from authenticate import authenticate
from PyQt5.QtGui import QStandardItem

if:
    api_number = 2
    nb_videos = 5

    for i in range(api_number):
        youtube = authenticate(i)
        titles, secondsVideos = download(youtube, nb_videos, i, list_view)
        
        item = QStandardItem("\nDownload fini\n\n")
        list_view.appendRow(item)
        
        try:
            montage(nb_videos, secondsVideos, titles)
            
            item = QStandardItem("Montage fini\n\n")
            list_view.appendRow(item)
        except: 
            montage(nb_videos, secondsVideos, titles)
            
            item = QStandardItem("Montage fini\n\n")
            list_view.appendRow(item)
        try: 
            upload(youtube, titles, nb_videos, list_view)

            item = QStandardItem("Upload fini")
            list_view.appendRow(item)
        except:
            upload(youtube, titles, nb_videos, list_view)
            
            item = QStandardItem("Upload fini")
            list_view.appendRow(item)

        for i in range(len(titles)):
            os.remove(f"Videos/{titles[i]}.mp4") 
            os.remove(f"Videos/youtube{i}_all.mp4")