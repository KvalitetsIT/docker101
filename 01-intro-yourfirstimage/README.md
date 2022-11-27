# Building and running your first Docker based application


## Building your first image
Let's create a simple Docker image.

We will create a Dockerfile to define our image. As a base image we use python:3.11.0-alpine3.15

Alpine is a lightweight Linux distribution and we will create a simple python application to learn about Docker images and containers.

```
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
```

You can lookup the different instructions in https://docs.docker.com/engine/reference/builder/ to see the details about them and explore all the possibilities

Let's build the image and watch the output of the build process:
```
$ docker build -t my/first:1 .
Sending build context to Docker daemon  10.75kB
Step 1/11 : FROM python:3.11.0-alpine3.15
 ---> c692f3b79c36
Step 2/11 : RUN apk update && apk add libcap
 ---> Running in 1ed0eb83cefa
fetch https://dl-cdn.alpinelinux.org/alpine/v3.15/main/x86_64/APKINDEX.tar.gz
fetch https://dl-cdn.alpinelinux.org/alpine/v3.15/community/x86_64/APKINDEX.tar.gz

... a lot of loglines related to the installation of libraries - we will ignore these for now ...

Removing intermediate container e2a85e50d99c
 ---> b22b618ca631
Step 4/11 : ENV GREETER DefaultGreeter
 ---> Running in f47db2adc718
Removing intermediate container f47db2adc718
 ---> ab16c159d28d
Step 5/11 : WORKDIR /usr/src/app
 ---> Running in 0b28af7c2c02
Removing intermediate container 0b28af7c2c02
 ---> fc5530f8fbb7
Step 6/11 : ENV GREETER DefaultGreeter
 ---> Running in 9702ab00d747
Removing intermediate container 9702ab00d747
 ---> 28de3cce1118
Step 7/11 : ENV FLASK_APP app
 ---> Running in 5eb616aa1d98
Removing intermediate container 5eb616aa1d98
 ---> d9fefb5eaa92
Step 8/11 : COPY app.py app.py
 ---> d9d6e4383100
Step 9/11 : COPY greetings/hello/greeting.txt /data/hello/greeting.txt
 ---> 91c8cf9ca83c
Step 10/11 : RUN echo Hello, $GREETER
 ---> Running in 3540464c93ae
Hello, DefaultGreeter
Removing intermediate container 3540464c93ae
 ---> 18a70c54715c
Step 11/11 : CMD { echo $GREETER; flask run --host=0.0.0.0; }
 ---> Running in 3866861588b7
Removing intermediate container 3866861588b7
 ---> 0045bdbc0751
Successfully built 0045bdbc0751
Successfully tagged my/first:1
```

Each instruction line in the Dockerfile adds a 'layer' in the filesystem of the resulting image.
The output of 'Hello, DefaultGreeter' shows how the execution of the 'echo' command is a part of the build phase. It will not have any effect on the resulting image as it does not add/remove anything to the layers.


## Running the image

Let's try and run the image:
```
$ docker run my/first:1
DefaultGreeter
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
Press CTRL+C to quit
```

The container is now running. You can see all your running containers:
```
$ docker ps
CONTAINER ID   IMAGE        COMMAND                  CREATED         STATUS         PORTS     NAMES
7a13fa1e44be   my/first:1   "/bin/sh -c '{ echo …"   5 seconds ago   Up 4 seconds             fervent_murdock
```

The Docker engine defines a Docker Network. Each container gets an IP address in this network. We can't reach the endpoint of the running container from our host machine without defining a portmapping.

Let's run with a portmapping:
```
$ docker run -p 5000:5000 my/first:1
DefaultGreeter
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
Press CTRL+C to quit


$ docker ps
CONTAINER ID   IMAGE        COMMAND                  CREATED         STATUS         PORTS                                       NAMES
94cfbde47286   my/first:1   "/bin/sh -c '{ echo …"   8 seconds ago   Up 7 seconds   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp   competent_lamport
```

Notice that we now have a mapping of the port 5000 on the host machine to the port 5000 of the running docker container.

We can now reach our application from our host machine:
```
$ curl http://localhost:5000/hello
Hi - From DefaultGreeter
```

We can supply configuration on runtime by using environment variables:
```
$ docker run -e GREETER=RunningGreeter -p 5000:5000 -t my/first:1
RunningGreeter
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
Press CTRL+C to quit

$ curl http://localhost:5000/hello
Hi - From RunningGreeter

$ curl http://localhost:5000/birthday
<!doctype html>
<html lang=en>
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>
``
Notice how the greeter name has changed with our redefinition of the environment variable GREETER. If we try to access the birthday URL the application will give us an error. 

We can also supply configuration on runtime by using volume mounts (mounting files into the filesystem of the running container):

```
$ docker run -e GREETER=RunningGreeter -p 5000:5000 -v $(pwd)/greetings/birthday:/data/birthday my/first:1
RunningGreeter
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
Press CTRL+C to quit

$ curl http://localhost:5000/birthday
Happy Birthday - From RunningGreeter
```

Our python application allows for configuration of different greetings by using volume mounts. 

It is in fact also vulnerable to a serious issue of OS command injection attacks - can you see how?
