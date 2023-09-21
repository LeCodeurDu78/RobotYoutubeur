from moviepy.editor import VideoFileClip, clips_array

def get_time(secondsVideos ,nb_videos):
    secondsStarts = []
    secondsEnds = []

    for i in range(nb_videos):
        offset = 15
        secondsEnd = VideoFileClip(f"Videos/youtube{i}_all.mp4").duration
        secondsStart = 0

        if secondsVideos[i] == -1:
            secondsVideos[i] = secondsEnd / 2

        if (secondsVideos[i] - offset) > 0.00:
            secondsStart = secondsVideos[i] - offset

        if (secondsVideos[i] + offset) < secondsEnd:
            secondsEnd = secondsVideos[i] + offset

        secondsStarts.append(secondsStart)
        secondsEnds.append(secondsEnd)
        
    return secondsStarts, secondsEnds

def edit_subclip(secondsStart, secondsEnd, i):
    youtubeClip = VideoFileClip(f"Videos/youtube{i}_all.mp4")
    anotherClip = VideoFileClip(f"Videos/another.mp4")

    youtubeClip = youtubeClip.subclip(secondsStart, secondsEnd)
    anotherClip = anotherClip.subclip(30, youtubeClip.duration + 30)

    return youtubeClip, anotherClip

def split_screen_video(youtubeClip, anotherClip, title):
    combined = clips_array([[youtubeClip],
                            [anotherClip]]) 
    combined.write_videofile(f"Videos/{title}.mp4")
    combined.close()

def montage(nb_videos, secondsVideos, titles):
    secondsStarts, secondsEnds = get_time(secondsVideos, nb_videos)

    for i in range(nb_videos):
        youtubeClip, anotherClip = edit_subclip(secondsStarts[i], secondsEnds[i], i)
        split_screen_video(youtubeClip, anotherClip, titles[i])
        youtubeClip.close()
        anotherClip.close()