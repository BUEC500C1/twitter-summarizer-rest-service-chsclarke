import pytest
import API

"""test imports for APIs"""
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
test API access classes - can only be done locally as auth keys are not pushed to git
"""
# does an api call to google return something
def test_google_api():
	google = API.Google('../auth/key.json')
	assert google.get_image_description('gs://cloud-samples-data/vision/using_curl/shanghai.jpeg') != None

# does an api call to twitter return anything
def test_twitter_api():
	twitter = API.Twitter('../auth/twitterAuth.json')
	assert twitter.get_user_timeline('markwahlberg', 1) != None


#test /get_profile endpoint




