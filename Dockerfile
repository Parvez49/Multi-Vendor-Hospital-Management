FROM python:3.9-alpine3.13
LABEL maintainer="phcloud.com"

#RUN apk add --no-cache libmagic

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./Multi-Vendor-Hospital-System /Multi-Vendor-Hospital-System
WORKDIR /Multi-Vendor-Hospital-System
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = true ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \ 
    fi && \
    rm -rf /tmp 

ENV PATH="/py/bin:$PATH"
