import os
import API
import json


twitter = API.Twitter('auth/twitterAuth.json')
status = twitter.get_user_timeline('realdonaldtrump', 3)

# profile = twitter.get_user_profile(status[0])

# print(json.dumps(profile, indent=4, sort_keys=True))


# for i in range(0, len(status)):
#     print(twitter.get_image(status[i]), status[i].text)

# print(twitter.get_image(status[0]), status[0].text)

print(json.dumps(status[1]._json["user"]["description"], indent=4, sort_keys=True))


# os.system("open " + status[0]._json["user"]["profile_image_url_https"][:-11] + ".jpg")


# def countChars(strList):
#     count = 0
#     for i in range(0,len(strList)):
#         for j in range(0, len(strList[i])):
#             count+=1
#     return count


# tweet = status[1].text
# tweet = tweet.split(" ")
# slices = len(tweet) // 6
# for j in range(0,slices):
#     startIndex = (len(tweet) // slices) * (j)
#     endIndex = (len(tweet) // slices) * (j + 1)
#     finalLine = " ".join(tweet[startIndex:endIndex])
#     if (30 <= countChars(finalLine) )
#     print( )
