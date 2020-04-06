# video-chsclarke 

## server

The server is run on an AWS EC2 instance using a nginx webserver and a gunicorn app server that serves my flask application.
Gunicorn runs 4 instances of my app on 4 threads. It is production ready and scalable if traffic is expected to increase.

Usage for the endpoint is detailed below.

init server from ec2 instance:

`$ sudo /etc/init.d/nginx restart`

`$ gunicorn wsgi:app --bind 0.0.0.0:8000 --daemon`

## Usage

There is one active enpoint on the REST service `/get_video`.

`/get_video` is an async endpoint that takes a twitter handle as an input and returns a hash.

Example: 

`$ curl http://ec2-18-237-107-102.us-west-2.compute.amazonaws.com/get_video?username=elonmusk` returns, 

```
{
  "callback": "7cb7e2c29c18460bb69f58bd6cebd59f"
}
```

After getting the hash you need to make a request to a new endpoint at the given hash (this way the endpoint can be truly async).

Example:

`$ curl http://ec2-18-237-107-102.us-west-2.compute.amazonaws.com/7cb7e2c29c18460bb69f58bd6cebd59f --output movie.mp4` will return `movie.mp4`. This is the requested video summary of the twitter user @elonmusk.

If you hit the hash endpoint before the video is done processing you will be given a status update on the videos creation.

Example:
```
{
  "status" : "in_progress"
}
```

