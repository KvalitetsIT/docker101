FROM python:3.11.0-alpine3.15

# Installing exta dependencies needed in our application
RUN apk update && apk add libcap
RUN pip install flask flask_bootstrap requests

# Settings some defaults
ENV GREETER DefaultGreeter

# Installing our app
WORKDIR /usr/src/app
ENV GREETER DefaultGreeter
ENV FLASK_APP app
COPY app.py app.py
COPY greetings/hello/greeting.txt /data/hello/greeting.txt

# Executed during build but really has no effect on the image (or on the running containers for that matter)
RUN echo Hello, $GREETER

# Defines what happens when the container starts
CMD { echo $GREETER; flask run --host=0.0.0.0; }
