FROM debian:jessie

MAINTAINER Marcell Jusztin <hello@morcmarc.com>

ENV GRAFANA_VERSION 3.1.1-1470047149
ENV GRAFANA_SCR /opt/grafana/

RUN apt-get update && \
    apt-get -y install libfontconfig wget adduser openssl ca-certificates python python-pip && \
    apt-get clean && \
    pip install requests && \
    wget https://grafanarel.s3.amazonaws.com/builds/grafana_${GRAFANA_VERSION}_amd64.deb -O /tmp/grafana.deb && \
    dpkg -i /tmp/grafana.deb && \
    rm /tmp/grafana.deb

COPY ./files/start.py ${GRAFANA_SCR}start.py
RUN chmod +x ${GRAFANA_SCR}start.py

EXPOSE 3000

ENTRYPOINT ["/opt/grafana/start.py"]
#ENTRYPOINT ["env"]