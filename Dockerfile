FROM alpine

CMD ["echo", "Aaron's Docker Image"]

RUN apk update
RUN apk add git

CMD ["echo", "Installed Git"]
