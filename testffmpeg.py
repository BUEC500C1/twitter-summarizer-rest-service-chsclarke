import ffmpeg
import API
import json
import re
import time
from textwrap import wrap
import threading 


numberTweets = 3
handle = 'elonmusk'
twitter = API.Twitter('auth/twitterAuth.json')
status = twitter.get_user_timeline(handle, numberTweets)
output = ""


# generate a short video for every tweet
def createImg(i):
    tweet = status[i].text

    stream = ffmpeg.input('a.jpg', pattern_type='glob', framerate=1)
    stream = ffmpeg.drawtext(stream, text="@" + handle, x=450, y=100, box=1, boxborderw=10, escape_text=True, fontsize=30, font="OpenSansEmoji")
    stream = ffmpeg.drawtext(stream, text=status[i]._json["user"]["description"], x=450, y=150, box=1, boxborderw=10, escape_text=True, fontsize=30, font="OpenSansEmoji")
    stream = ffmpeg.drawtext(stream, text="Tweet: " + str(i + 1), x=450, y=300, box=1, boxborderw=10, escape_text=True, fontsize=30, font="OpenSansEmoji")
    
    fomattedTweet = wrap(tweet, 30)
    for j, line in enumerate(fomattedTweet):
        stream = ffmpeg.drawtext(stream, text=line, x=500, y=350 + (50*j), box=1, boxborderw=10, escape_text=True, fontsize=30, font="OpenSansEmoji")

    stream = ffmpeg.output(stream, 'img/movie' + str(i) + '.mp4')
    ffmpeg.run(stream)

t1 = threading.Thread(target=createImg, args=(0,))
t2 = threading.Thread(target=createImg, args=(1,))
t3 = threading.Thread(target=createImg, args=(2,))

t1.start() 
t2.start() 
t3.start()

t1.join() 
t2.join()
t3.join() 
  
(
    ffmpeg
    .concat(ffmpeg.input('img/movie0.mp4'),
        ffmpeg.input('img/movie1.mp4'),
        ffmpeg.input('img/movie2.mp4'))
    .overlay(ffmpeg.input(status[0]._json["user"]["profile_image_url_https"][:-11] + ".jpg"))
    .drawbox(0, 0, 400, 400, color='black', thickness=10)
    #.filter('fps', fps=1, round='up')
    .output('img/out.mp4')
    .run()
)

