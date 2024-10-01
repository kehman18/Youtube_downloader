'''modules needed for the youtube downloader'''
import os
import re
from flask import Flask, render_template, request, send_file, redirect, url_for
from pytube import YouTube

app = Flask(__name__)

# Function to download the video based on the user's selection
def download_video(video_url, resolution):
    '''the function that downloads video from client side'''
    yt = YouTube(video_url)
    
    # Filtering streams based on selected resolution
    stream = yt.streams.filter(res=f"{resolution}p", file_extension="mp4").first()
    
    # If the resolution is not found, fallback to the highest resolution
    if stream is None:
        stream = yt.streams.filter(file_extension="mp4").get_highest_resolution()

    # Download the video
    file_path = stream.download(output_path="downloads/")
    return file_path

# Improved YouTube URL validation
def validate_yt_link(user_url):
    '''this function checks if the user inputs the correct YouTube URL'''
    youtube_regex = r'^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/(watch\?v=|embed\/|v\/|.+\?v=)?([^&=%\?]{11})'
    ytlink_match = re.match(youtube_regex, user_url)
    if ytlink_match:
        return user_url
    else:
        return None

# Home page that renders the form
@app.route('/')
def home():
    '''renders the home page'''
    return render_template('index.html')

# Handling the form submission and downloading the video
@app.route('/download', methods=['POST'])
def download():
    '''this function downloads video received from the client'''
    youtube_link = request.form['youtube_link']
    validated_youtube_link = validate_yt_link(youtube_link)
    
    if validated_youtube_link is None:
        return 'This is not a correct YouTube URL format', 400
    
    resolution = request.form['resolution']

    try:
        file_path = download_video(validated_youtube_link, resolution)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        print(e)
        return redirect(url_for('home'))

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)
