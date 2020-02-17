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

app = Flask(__name__)

google = API.Google('auth/googleAuth.json')
twitter = API.Twitter('auth/twitterAuth.json')

"""get last tweet given username"""
@app.route('/get_tweet')
def get_last_tweet():
    result = {}
    imgDescription = None
    status = None

    #if user provided a username
    if (request.args.get('username')):
        username = request.args.get('username')
        status = twitter.get_user_timeline(username, 1)

        #check if there is an image in tweet
        try:
            imgURL = twitter.get_image(status[0])
            imgDescription = google.get_image_description(imgURL)
            result["img"] = {"url" : imgURL, "tags" : [imgDescription[0], imgDescription[1], imgDescription[2]] if len(imgDescription) > 3 else "NA"}
        except:
            imgDescription = False
        
        #wait for api data to return
        while (status is None or imgDescription is None):
            time.sleep(.1)

        result["tweet"] = status[0].text if status[0].text else "NA"

        return result
    else:
        return "{\"ERROR\" : \"you must enter a username\"}"


"""get profile info given username"""
@app.route('/get_profile')
def get_user_profile():
    result = {}
    imgDescription = None
    status = None

    #if user provided a username
    if (request.args.get('username')):
        username = request.args.get('username')
        status = twitter.get_user_timeline(username, 1)
        profile = twitter.get_user_profile(status[0])
        imgDescription = google.get_image_description(profile["profile_image_url_https"])
        print(profile["profile_background_image_url_https"])

        #wait for api data to return
        while (status is None or imgDescription is None):
            time.sleep(.1)

        result["created_at"] = profile["created_at"] if "created_at" in profile else "NA"
        result["description"] = profile["description"] if "description" in profile else "NA"
        result["urls"] = profile["entities"]["url"]["urls"] if "url" in profile["entities"] and "urls" in profile["entities"]["url"] else "NA"
        result["followers_count"] = profile["followers_count"] if "followers_count" in profile else "NA"
        result["id"] = profile["id"] if "id" in profile else "NA"
        result["location"] = profile["location"] if "location" in profile else "NA"
        result["name"] = profile["name"] if "name" in profile else "NA"
        result["screen_name"] = profile["screen_name"] if "screen_name" in profile else "NA"
        result["img"] = {"url" : profile["profile_image_url_https"], "tags" : [imgDescription[0], imgDescription[1], imgDescription[2]] if len(imgDescription) > 3 else "NA"}
        return result
    else:
        return "{\"ERROR\" : \"you must enter a username\"}"

@app.route('/get_video')
def get_user_video():

    if (request.args.get('username')):
        os.system('./clear.sh')
        numberTweets = 3
        handle = request.args.get('username')
        globalStatus = twitter.get_user_timeline(handle, numberTweets)

        ffmpegWrapper.initThreads(numberTweets, globalStatus, handle)
        ffmpegWrapper.concatSlides(globalStatus, numberTweets)
        return send_file('./img/out.mp4', attachment_filename='movie.mp4')
    else:
        return "{\"ERROR\" : \"you must enter a username\"}"



"""handling 404 error"""
@app.errorhandler(404) 
def not_found(e): 
    return "{\"ERROR\" : \"404\"}"

"""handling 500 error"""
@app.errorhandler(500)
def internal_error(e): 
    return "{\"ERROR\" : \"500\"}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)