FROM locustio/locust:2.14.2

USER root

RUN apt-get update \
 && apt-get install -y --no-install-recommends curl openjdk-17-jre-headless

COPY . /mnt/locust
RUN python3 -m pip install -r /mnt/locust/requirements.txt
