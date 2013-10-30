# Dockerfile for ElasticSearch

FROM mpetazzoni/sf-base

MAINTAINER Maxime Petazzoni <max@signalfuse.com>

# Python YAML is required to generate ElasticSearch's configuration
RUN apt-get update
RUN apt-get -y install python-yaml

RUN wget -q -O - https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-0.90.5.tar.gz \
  | tar -C /opt -xz

ADD run.py /opt/elasticsearch-0.90.5/.docker/

WORKDIR /opt/elasticsearch-0.90.5
CMD ["python", "/opt/elasticsearch-0.90.5/.docker/run.py"]
