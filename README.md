# video-chsclarke 

## Asignment

__Main Exercise__:  Using the twitter feed, construct a daily video summarizing a twitter handle on a given day.

* Convert text into an image in a frame.
* Do a sequence of all texts and images in chronological order.
* Display each video frame for 3 seconds.


## Installation

### Enable [google](https://cloud.google.com/vision/docs/before-you-begin) and [twitter](https://developer.twitter.com/en/docs/basics/getting-started) API's

Once you have your API keys, add them to the [auth](https://github.com/BUEC500C1/twitter-summarizer-chsclarke/tree/master/auth) folder. Be sure to remove `[template]` from the file names.

### Install dependencies
install [ffpmeg](https://www.ffmpeg.org/).

install python dependencies:

`pip3 install -r requirements.txt`

Done!

## Usage

Start server with `$ python3 main.py`

There is one active enpoint on the REST service `/get_video`.

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

http://localhost/7cb7e2c29c18460bb69f58bd6cebd59f would return `movie.mp4`. This is the requested video summary of the twitter user @elonmusk.

If you hit the hash endpoint before the video is done processing you will be given a status update on the videos creation.

Example:
```
{
  "status" : "in_progress"
}
```

### Testing

Ensure you have properly reviewed the Installation instructions and have started the flask server with `$python3 main.py`.

Run tests with `pytest`


