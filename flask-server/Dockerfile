FROM python:3.10

WORKDIR /app

RUN apt-get update -y

RUN pip install Flask
RUN pip install flask_cors
RUN pip install --user ur_rtde

EXPOSE 5000