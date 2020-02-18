# video-chsclarke 

## Asignment

__Main Exercise__:  Using the twitter feed, construct a daily video summarizing a twitter handle on a given day.

* Convert text into an image in a frame.
* Do a sequence of all texts and images in chronological order.
* Display each video frame for 3 seconds.

## Requirements 
none! the app is containerized so there is no need

## Installation

### Enable [google](https://cloud.google.com/vision/docs/before-you-begin) and [twitter](https://developer.twitter.com/en/docs/basics/getting-started) API's

Once you have your API keys, add them to the [auth](https://github.com/BUEC500C1/twitter-summarizer-chsclarke/tree/master/auth) folder. Be sure to remove `[template]` from the file names.

### Build Docker image locally

Build image from Dockerfile:  
`docker build -t <your_username>/python-endpoint .`

Expose image to port 80:
`docker run -p 80:5000 <your_username>/python-endpoint`

Done!

### If your image breaks
Delete all images and containers in the case of an error:  
`docker rm -vf $(docker ps -a -q);docker rmi -f $(docker images -a -q)`

## Usage

There is one active enpoints on the REST service `/get_video`.

`/get_video` is an async endpoint that takes a twitter handle as an input and returns a hash.

Example: 

http://localhost/get_video?username=elonmusk returns, 

```
{
  "callback": "7cb7e2c29c18460bb69f58bd6cebd59f"
}
```

After getting the hash you need to make a request to a new endpoint at the given hash (this way the endpoint can be truly async).

Example:

http://localhost/7cb7e2c29c18460bb69f58bd6cebd59f returns,

```
movie.mp4
```


