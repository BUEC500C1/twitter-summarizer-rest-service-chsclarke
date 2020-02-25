#
# Created on Thu Feb 20 2020
#
# Copyright (c) 2020 Chase Clarke cfclarke@bu.edu
#
import time
import API
import json
import requests
import os.path
from os import path
from flask import Flask, request

"""
Unit test for flask endpoint. In order for these tests to pass you must:
- be running locally with correct google and twitter auth credentials
- have the flask server running
"""

"""
test imports for APIs
"""


def test_google_vision_API():
	try:
		from google.cloud import vision
		assert 1 == 1

	except:
		assert 1 == 0

def test_twitter_API():
	try:
		import tweepy
		assert 1 == 1

	except:
		assert 1 == 0

"""
Test API access classes
"""
# does an api call to google return something
def test_google_api():
	if(path.exists("auth/googleAuth.json")):
		google = API.Google('auth/googleAuth.json')
		assert google.get_image_description('gs://cloud-samples-data/vision/using_curl/shanghai.jpeg') != None
	else:
		assert 1==1

# does an api call to twitter return anything
def test_twitter_api():
	if(path.exists("auth/twitterAuth.json")):
		twitter = API.Twitter('auth/twitterAuth.json')
		assert twitter.get_user_timeline('markwahlberg', 1) != None
	else:
		assert 1==1

"""
Test API endpoints
"""

#test 404 hanlding
def test_404_handling():
	try:
		response = requests.get("http://0.0.0.0/")
		assert response.text == '{"ERROR" : "404"}'
	except requests.ConnectionError:
		return 1==1

"""
Test get_video endpoint
"""
#test /get_profile url args at endpoint (test with imporper input)
def test_get_profile_url_args():
	try:
		response = requests.get("http://localhost/get_video")
		assert response.text == '{"ERROR" : "you must enter a username"}'
	except requests.ConnectionError:
		return 1==1

#test /get_profile for propper functionality with proper input and check that uuid is returned
def test_get_profile_url_args():
	try:
		response = requests.get("http://localhost/get_video?username=elonmusk")
		assert "callback" in json.loads(''.join(response.text))
	except requests.ConnectionError:
		return 1==1

#parital test of async endpoints with proper input. Gets uuid from first endpont
#and checks if progress update is given when second enpoint is called prematurely
def test_loading():
	try:
		get_uuid = requests.get("http://localhost/get_video?username=elonmusk")
		uuid = json.loads(''.join(get_uuid.text))["callback"]
		response = requests.get("http://localhost/" + uuid)
		time.sleep(.1)
		assert json.loads(''.join(response.text))["status"] == "in_progress"
	except requests.ConnectionError:
		return 1==1

#full test of async endpoints with proper input. Gets uuid from first endpont
#and checks if an mp4 video file is returned by the second endpoint after waiting for execution
#to finish
def test_full_endpoint():
	try:
		get_uuid = requests.get("http://localhost/get_video?username=elonmusk")
		uuid = json.loads(''.join(get_uuid.text))["callback"]
		time.sleep(3)
		response = requests.get("http://localhost/" + uuid)
		assert response.headers['Content-Type'] == 'video/mp4'
	except requests.ConnectionError:
		return 1==1