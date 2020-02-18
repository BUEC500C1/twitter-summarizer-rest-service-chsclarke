import ffmpeg
import API
import json
import re
import time
from textwrap import wrap
import threading 


# generate a short video (slide) for every tweet
def createSlide(i, status, handle, hash):
    tweet = status[i].text

    stream = ffmpeg.input('a.jpg', pattern_type='glob', framerate=1)
    stream = ffmpeg.drawtext(stream, text="@" + handle, x=450, y=100, box=1, boxborderw=10, escape_text=True, fontsize=30, font="OpenSansEmoji")
    stream = ffmpeg.drawtext(stream, text=status[i]._json["user"]["description"], x=450, y=150, box=1, boxborderw=10, escape_text=True, fontsize=30, font="OpenSansEmoji")
    stream = ffmpeg.drawtext(stream, text="Tweet: " + str(i + 1), x=450, y=300, box=1, boxborderw=10, escape_text=True, fontsize=30, font="OpenSansEmoji")
    
    fomattedTweet = wrap(tweet, 30)
    for j, line in enumerate(fomattedTweet):
        stream = ffmpeg.drawtext(stream, text=line, x=500, y=350 + (50*j), box=1, boxborderw=10, escape_text=True, fontsize=30, font="OpenSansEmoji")

    stream = ffmpeg.output(stream, 'img/' + str(hash) + "_" + str(i) + '.mp4')
    ffmpeg.run(stream)

#start generating slides in parallel with different threads
def initThreads(numberTweets, status, handle, hash):
    threads = []
    for i in range(0,numberTweets):
        threads.append(threading.Thread(target=createSlide, args=(i,status, handle, hash)))

    for i in range(0,numberTweets):
        threads[i].start()

    for i in range(0,numberTweets):
        threads[i].join() 

#concatenate all slides into one video
def concatSlides(status, numberTweets, hash):
    allSlides = []
    
    for i in range(0, numberTweets):
        allSlides.append(ffmpeg.input('img/' + str(hash) + "_" + str(i) + '.mp4'))

    (
    ffmpeg
    .concat(*allSlides)
    .overlay(ffmpeg.input(status[0]._json["user"]["profile_image_url_https"][:-11] + ".jpg"))
    .drawbox(0, 0, 400, 400, color='black', thickness=10)
    .output('img/' + str(hash) + "_out" '.mp4')
    .run()
    )


