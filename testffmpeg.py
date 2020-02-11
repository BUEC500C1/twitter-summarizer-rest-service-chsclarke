import ffmpeg
import API
import json
import re
import time

handle = 'elonmusk'
twitter = API.Twitter('auth/twitterAuth.json')
status = twitter.get_user_timeline(handle, 3)

# tweet = status[0].text #re.sub(r'[^\w]', '', status[1].text)

# generate a short video for every tweet
for i in range(0, len(status)):
    tweet = status[i].text

    stream = ffmpeg.input('a.jpg', pattern_type='glob', framerate=1)
    stream = ffmpeg.drawtext(stream, text="@" + handle, x=450, y=100, box=1, boxborderw=10, escape_text=True, fontsize=30)
    stream = ffmpeg.drawtext(stream, text="Tweet: " + str(i + 1), x=450, y=300, box=1, boxborderw=10, escape_text=True, fontsize=30)
    stream = ffmpeg.drawtext(stream, text=status[i]._json["user"]["description"], x=450, y=150, box=1, boxborderw=10, escape_text=True, fontsize=30)

    
    tweet = tweet.split(" ")
    slices = len(tweet) // 4
    for j in range(0,slices):
        startIndex = (len(tweet) // slices) * (j)
        endIndex = (len(tweet) // slices) * (j + 1)
        stream = ffmpeg.drawtext(stream, text=" ".join(tweet[startIndex:endIndex]), x=500, y=350 + (50*j), box=1, boxborderw=10, escape_text=True, fontsize=30)

    stream = ffmpeg.output(stream, 'img/movie' + str(i) + '.mp4')
    ffmpeg.run(stream)

(
    ffmpeg
    .concat(ffmpeg.input('img/movie0.mp4'),
        ffmpeg.input('img/movie1.mp4'),
        ffmpeg.input('img/movie2.mp4'))
    .overlay(ffmpeg.input(status[0]._json["user"]["profile_image_url_https"][:-11] + ".jpg"))
    .drawbox(0, 0, 400, 400, color='black', thickness=10)
    .output('img/out.mp4')
    .run()
)

