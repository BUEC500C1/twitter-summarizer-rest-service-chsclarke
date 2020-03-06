# video-chsclarke 

## Usage

There is one active enpoint on the REST service `/get_video`.

`/get_video` is an async endpoint that takes a twitter handle as an input and returns a hash.

Example: 

http://ec2-34-221-127-83.us-west-2.compute.amazonaws.com/get_video?username=elonmusk returns, 

```
{
  "callback": "7cb7e2c29c18460bb69f58bd6cebd59f"
}
```

After getting the hash you need to make a request to a new endpoint at the given hash (this way the endpoint can be truly async).

Example:

http://ec2-34-221-127-83.us-west-2.compute.amazonaws.com/7cb7e2c29c18460bb69f58bd6cebd59f would return `movie.mp4`. This is the requested video summary of the twitter user @elonmusk.

If you hit the hash endpoint before the video is done processing you will be given a status update on the videos creation.

Example:
```
{
  "status" : "in_progress"
}
```

