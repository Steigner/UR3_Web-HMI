# UR3 Web - HMI

In this project, the digital twin solution was based on technology accessible through a web browser. The technology consists of several containers for easy access.

```javascript
Software
------------------------------------
|
+ ---------
|
|   - FLASK-SERVER
|   -   based on Python(3.10)
|   --   ur-rtde
|
|   - SERVER
|   -   based on Node(latest)
|   --   vite
|   --   three
```

Data from the client side is sent via **SSE (Server Sent Events)** to the Flask server side, where there is a simple API that can communicate with the real UR3 robot or with UR3 in the UR Polyscope simulation using **RTDE (Real-Time Data Exchange)** communication.


## How to run

The whole application is based on a containerized application. Docker Compose was used, where containers for visualization and communication with the robot are solved, in the container itself also the unpacking of the whole scene for visualization is solved. In the unzip container, the package is loaded and then decompressed with the volumes linked for access from the visualization container to the client.

**Dependencies: Docker || Docker Compose || Docker Desktop**

```bash
$ docker compose up --build
```

The application then runs on the host computer, so it is possible to connect to it on port 3000.

```bash
http://ip-adress-of-host:3000/
```

**Note:** The application can run on any OS with x86 architecture. Not yet optimized for ARM architecture.

## Visual

![ex1](/docs/example_1.png)

![ex2](/docs/example_2.png)