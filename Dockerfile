# Dockerfile for ElasticSearch

FROM mpetazzoni/sf-base

MAINTAINER Maxime Petazzoni <max@signalfuse.com>

# Python YAML is required to generate ElasticSearch's configuration
RUN apt-get update
RUN apt-get -y install python-yaml maven

RUN wget -q -O - https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-0.90.5.tar.gz \
  | tar -C /opt -xz

# Install the ZooKeeper discovery plugin
RUN git clone https://github.com/laigood/elasticsearch-zookeeper.git /tmp/elasticsearch-zookeeper
RUN cd /tmp/elasticsearch-zookeeper && mvn package -Dmaven.test.skip=true -Dzookeeper.version=3.4.5
RUN /opt/elasticsearch-0.90.5/bin/plugin -v         \
  -u file:///tmp/elasticsearch-zookeeper/target/releases/elasticsearch-zookeeper-0.90.5.zip \
  -i elasticsearch-zookeeper-0.90.5
RUN rm -rf /tmp/elasticsearch-zookeeper

ADD run.py /opt/elasticsearch-0.90.5/.docker/

WORKDIR /opt/elasticsearch-0.90.5
CMD ["python", "/opt/elasticsearch-0.90.5/.docker/run.py"]
