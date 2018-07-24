FROM alpine

CMD ["echo", "Aaron's Docker Image"]

RUN apk update
RUN apk add git

CMD ["echo", "Installed Git"]

RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev && \
    apk add --no-cache --update python3 && \
    pip3 install --upgrade pip setuptools
RUN pip3 install pendulum service_identity

CMD ["echo", "Installed python3"]
