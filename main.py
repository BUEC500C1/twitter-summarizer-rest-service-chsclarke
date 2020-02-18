from flask import Flask
from flask import request
import API
import time
import ffmpeg
import json
import re
from textwrap import wrap
from flask import send_file
import threading 
import ffmpegWrapper
import os
from flask import abort
import uuid
import threading 

app = Flask(__name__)

google = API.Google('auth/googleAuth.json')
twitter = API.Twitter('auth/twitterAuth.json')

queue = {}

def create_video(hash, handle):
    numberTweets = 3
    globalStatus = twitter.get_user_timeline(handle, numberTweets)
    ffmpegWrapper.initThreads(numberTweets, globalStatus, handle, hash)
    ffmpegWrapper.concatSlides(globalStatus, numberTweets, hash)
    queue[hash] = True
    exit()

@app.route('/<page>')
def index(page):
    if (page == 'get_video'):
        if (request.args.get('username')):
            hash = uuid.uuid4().hex
            queue[hash] = False
            handle = request.args.get('username')
            threading.Thread(target=create_video, args=(hash,handle,)).start()

            return {"callback" : hash}

        else:
            return "{\"ERROR\" : \"you must enter a username\"}"

    elif (page in queue):
        if queue[page] == True:
            videoFile = send_file('./img/' + str(page) + '_out.mp4', attachment_filename='movie.mp4')
            os.system('rm -r -f img/' + str(page) + '*')
            del queue[page]
            return videoFile

        else:
            return {"status"  : "in_progress"}

    else:
        abort(404)

"""handling 404 error"""
@app.errorhandler(404) 
def not_found(e): 
    return "{\"ERROR\" : \"404\"}"

"""handling 500 error"""
@app.errorhandler(500)
def internal_error(e): 
    return "{\"ERROR\" : \"500\"}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port='80')