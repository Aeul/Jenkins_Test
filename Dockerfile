FROM alpine

CMD ["echo", "Aaron's Docker Image"]

RUN apk add git

CMD ["echo", "Installed Git"]
