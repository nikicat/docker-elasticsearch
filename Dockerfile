# Dockerfile for ElasticSearch

FROM quay.io/signalfuse/maestro-base:0.1.7
MAINTAINER Maxime Petazzoni <max@signalfuse.com>

ENV DEBIAN_FRONTEND noninteractive

# Python YAML is required to generate ElasticSearch's configuration. Maven is
# needed to build the elasticsearch-zookeeper plugin.
RUN apt-get update
RUN apt-get -y install python-yaml python-setuptools maven

# Get the latest stable version of ElasticSearch
RUN wget -q -O - https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.1.0.tar.gz \
  | tar -C /opt -xz

# Install the ZooKeeper discovery plugin
RUN git clone https://github.com/kpruden/elasticsearch-zookeeper.git /tmp/elasticsearch-zookeeper
RUN cd /tmp/elasticsearch-zookeeper && mvn package -Dmaven.test.skip=true -Dzookeeper.version=3.4.5
RUN /opt/elasticsearch-1.1.0/bin/plugin -v                                                 		\
  -u file:///tmp/elasticsearch-zookeeper/target/releases/elasticsearch-zookeeper-1.1.0-SNAPSHOT.zip	\
  -i elasticsearch-zookeeper-1.1.0-SNAPSHOT
RUN rm -rf /tmp/elasticsearch-zookeeper

# Install Marvel plugin
RUN /opt/elasticsearch-1.1.0/bin/plugin -v -i elasticsearch/marvel/latest

ADD run.py /opt/elasticsearch-1.1.0/.docker/

WORKDIR /opt/elasticsearch-1.1.0
VOLUME /var/lib/elasticsearch
VOLUME /var/log/elasticsearch
CMD ["python", "/opt/elasticsearch-1.1.0/.docker/run.py"]
