#
# Created on Thu Feb 20 2020
#
# Copyright (c) 2020 Chase Clarke cfclarke@bu.edu
#
from flask import render_template
from flask import Flask
from flask import request
import API
import time
import ffmpeg
import json
import re
from textwrap import wrap
from flask import send_file
import ffmpegWrapper
import os
from flask import abort
import uuid
import threading
from threading import Thread
from worker import workerDispatcher
from worker import workerQ
import worker

app = Flask(__name__, template_folder='./static/')
workerDispatcherThread = Thread(target=workerDispatcher, daemon=True)
workerDispatcherThread.start()
worker.init()

"""handles all incoming requests"""
@app.route('/<page>')
def index(page):
    if (page == 'get_video'):
        if (request.args.get('username')):
            hash = uuid.uuid4().hex
            worker.statusQueue[hash] = False
            handle = request.args.get('username')
            workerQ.put((hash, handle))
            return {"callback" : hash}

        else:
            return "{\"ERROR\" : \"you must enter a username\"}"

    elif page in worker.statusQueue:
        if worker.statusQueue[page] == True:
            videoFile = send_file('./img/' + str(page) + '_out.mp4', 
                    attachment_filename='movie.mp4')
            os.system('rm -r -f img/' + str(page) + '*')
            del worker.statusQueue[page]
            return videoFile

        else:
            return {"status"  : "in_progress"}

    else:
        abort(404)

"""handling 404 error"""
@app.errorhandler(404)
def not_found(e): 
    if request.user_agent.browser in \
        ["camino","chrome","firefox","galeon","kmeleon","konqueror",
        "links","lynx","msie","msn","netscape","opera","safari",
        "seamonkey","webkit" ]:
        return render_template('404.html')
    else:
        return "{\"ERROR\" : \"404\"}"


"""handling 500 error"""
@app.errorhandler(500)
def internal_error(e): 
    return "{\"ERROR\" : \"500\"}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port='80')
