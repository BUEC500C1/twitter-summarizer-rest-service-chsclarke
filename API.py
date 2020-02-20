from google.cloud import vision
import os
import tweepy
import json


class Twitter:
   """
   Initializes a TwitterAPI class that can acces the twitter api with the
   tweepy libaray

   USAGE:
   test = Twitter('../auth/twitterAuth.json')
   test.get_user_timeline('markwahlberg')
   """
   def __init__(self, authKey):
      with open(authKey) as json_file:
         data = json.load(json_file)
      
      # pulling auth data
      self.consumer_secret = data["consumer_secret"]
      self.consumer_key = data["consumer_key"]
      self.access_token = data["access_token"]
      self.access_token_secret = data["access_token_secret"]

      # Setting up tweepy auth
      auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
      auth.set_access_token(self.access_token, self.access_token_secret)

      self.api = tweepy.API(auth)
   
   def get_user_timeline(self, id, count):
      self.status = self.api.user_timeline(id=id, count=count)
      return self.status

   def get_image(self, status):
      return status._json["entities"]["media"][0]["media_url_https"] if ("media" in status._json["entities"]) else "NA"

      # return status._json["entities"]["media"][0]["media_url_https"]

   def get_user_profile(self, status):
      return status._json["user"]


class Google:
   """
   Initializes a GoogleAPI class that can acces the google api

   USAGE:
   google = Google('../auth/key.json')
   google.get_image_description('gs://cloud-samples-data/vision/using_curl/shanghai.jpeg')
   """
   def __init__(self, authKey):
      os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = authKey

      self.client = vision.ImageAnnotatorClient()
      self.image = vision.types.Image()

   def get_image_description(self, imageURL):
      image_uri = imageURL
      self.image.source.image_uri = image_uri
      response = self.client.label_detection(image=self.image)

      labels = []
      for label in response.label_annotations:
         labels.append((label.description, label.score*100))

      return labels
