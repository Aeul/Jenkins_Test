FROM ubuntu:14.04

CMD ["echo", "Aaron's Docker Image"]

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y git

CMD ["echo", "Installed Git"]
