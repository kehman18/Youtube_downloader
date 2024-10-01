from pytube import YouTube

yt = YouTube('https://youtube.com/shorts/YarmPTWse9c?si=ZvdNTXTkghwot24g')
video = yt.streams.get_highest_resolution()

try:
    video.download()
    print('Youtube video downloaded complately')
except:
    print('Could not download the video')