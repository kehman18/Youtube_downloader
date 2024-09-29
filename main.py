'''all necessry modules to scrape a video from youtube'''
from pytube import YouTube

yt = YouTube('https://youtu.be/z3Gq46SjD8Q?si=XYNFTcHMz6GVZzn2')
video_title = yt.title
print(yt)