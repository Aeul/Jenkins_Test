From alpine

CMD ["echo", "Aaron's Docker Image"]

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y git
