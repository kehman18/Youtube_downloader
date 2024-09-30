from flask import Flask, render_template, request, send_file, redirect, url_for
from pytube import YouTube
import os

app = Flask(__name__)

# Function to download the video based on the user's selection
def download_video(video_url, resolution):
    yt = YouTube(video_url)
    
    # Filtering streams based on selected resolution
    stream = yt.streams.filter(res=f"{resolution}p", file_extension="mp4").first()
    
    # If the resolution is not found, fallback to the lowest resolution
    if stream is None:
        stream = yt.streams.filter(file_extension="mp4").get_lowest_resolution()

    # Download the video
    file_path = stream.download(output_path="downloads/")
    return file_path

# Home page that renders the form
@app.route('/')
def home():
    return render_template('index.html')

# Handling the form submission and downloading the video
@app.route('/download', methods=['POST'])
def download():
    youtube_link = request.form['youtube_link']
    resolution = request.form['resolution']

    try:
        file_path = download_video(youtube_link, resolution)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        print(e)
        return redirect(url_for('home'))

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')  # Create the downloads folder if it doesn't exist
    app.run(debug=True)
