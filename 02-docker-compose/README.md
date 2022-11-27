# Tool: Docker-compose

# Introduction
We saw in the previous section that we can configure our application using environment variables and volume mounts.
An easy way to share these configuration (and to do more complex setups involving more than one docker container) is using the tool docker-compose.

As an example we will work on the application from the previous section and add a new feature. 

In this section we will add user authentication for our application. Users are to be maintained in a MariaDB database. The security protocol is basic authentication.

Luckily, Python Flask apps have support for both MariaDB and basic autentication. We just have to use a few libraries. Look at the new app.py to see the improved application.

# The docker-compose YAML File
Docker-compose setups are described in docker-compose yaml files. There are many features, you can use - look at the reference at (https://docs.docker.com/compose/compose-file/)

For our example, we need our application and a database:
```
version: '3.4'

services:      
  db:
    image: mariadb:10.3.16
    environment:
      - MYSQL_ROOT_PASSWORD=rootroot
      - MYSQL_DATABASE=users
      - MYSQL_USER=dbuser
      - MYSQL_PASSWORD=1234
    volumes:
      - ./database/:/docker-entrypoint-initdb.d/:ro
  myservice:
    image: my/first:2
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      - GREETER=TestingDockerCompose
      - MYSQL_HOST=db
      - MYSQL_USER=dbuser
      - MYSQL_PASSWORD=1234
      - MYSQL_DB=users
```

In the documentation for the MariaDB it is documented how to volume mount SQL files for database initialization and generation of data and which environment variables to set in order to configure the database.

# Starting the docker-compose Setup
Lets start the docker-compose setup:
```
$ docker-compose up
WARNING: The Docker Engine you're using is running in swarm mode.

Compose does not use swarm mode to deploy services to multiple nodes in a swarm. All containers will be scheduled on the current node.

To deploy your application across the swarm, use `docker stack deploy`.

Creating 02-docker-compose_myservice_1 ... done
Creating 02-docker-compose_db_1        ... done
Attaching to 02-docker-compose_myservice_1, 02-docker-compose_db_1
myservice_1  | TestingDockerCompose
myservice_1  |  * Serving Flask app 'app'
myservice_1  |  * Debug mode: off
myservice_1  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
myservice_1  |  * Running on all addresses (0.0.0.0)
myservice_1  |  * Running on http://127.0.0.1:5000
myservice_1  |  * Running on http://172.29.0.2:5000
myservice_1  | Press CTRL+C to quit
db_1         | Initializing database
db_1         | 
db_1         | 
db_1         | PLEASE REMEMBER TO SET A PASSWORD FOR THE MariaDB root USER !
db_1         | To do so, start the server, then issue the following commands:
db_1         | 
... many many log lines ..
```

Let's see how many containers are running:
```
$ docker ps
CONTAINER ID   IMAGE             COMMAND                  CREATED              STATUS              PORTS                                       NAMES
74b176e2f6ce   mariadb:10.3.16   "docker-entrypoint.s…"   About a minute ago   Up About a minute   3306/tcp                                    02-docker-compose_db_1
d151b1678372   my/first:2        "/bin/sh -c '{ echo …"   About a minute ago   Up About a minute   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp   02-docker-compose_myservice_1
```

A docker-compose setup will define a network (within the Docker network) in which the individual containers can reference each other by hostname.

We can inspect the list of networks:
```
$ docker network ls
NETWORK ID     NAME                                              DRIVER    SCOPE
b6d79c50686e   02-docker-compose_default                         bridge    local
```

We can find the details about our network:
```
$ docker network inspect 02-docker-compose_default
[
    {
        "Name": "02-docker-compose_default",
        "Id": "b6d79c50686e0ab4742d2a85aa9c67b6e68f417c69847bd38a960dfb06cf19e4",
        "Created": "2022-11-25T19:16:04.759103323+01:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "172.29.0.0/16",
                    "Gateway": "172.29.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": true,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "74b176e2f6ce48c22b3bb306c84aa78d767b78454f03f8fc1f339f382b8ad716": {
                "Name": "02-docker-compose_db_1",
                "EndpointID": "14ca7165733a75398502a119c50272763e9021b46263c0bd4809276122956525",
                "MacAddress": "02:42:ac:1d:00:03",
                "IPv4Address": "172.29.0.3/16",
                "IPv6Address": ""
            },
            "d151b167837217b8eed24c8697425c7bf9ea5938bf3039783e9745e20d5cd86f": {
                "Name": "02-docker-compose_myservice_1",
                "EndpointID": "6f827c13d0553bc430f815705020166897ab7773de88855dde308a71e3330631",
                "MacAddress": "02:42:ac:1d:00:02",
                "IPv4Address": "172.29.0.2/16",
                "IPv6Address": ""
            }
        },
        "Options": {},
        "Labels": {
            "com.docker.compose.network": "default",
            "com.docker.compose.project": "02-docker-compose",
            "com.docker.compose.version": "1.23.2"
        }
    }
]
```

The hostname is the name defined in the docker-compose file services section. The hostname of the database is db and the hostname of our application is myservice.



urlencode 'hello; ls -la /; cat /data/hello'
