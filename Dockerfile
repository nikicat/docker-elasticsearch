# Dockerfile for ElasticSearch

FROM yandex/ubuntu:14.04
MAINTAINER Nikolay Bryskin <devel.niks@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

# Get the latest stable version of ElasticSearch
RUN wget -O - http://packages.elasticsearch.org/GPG-KEY-elasticsearch | apt-key add -
RUN echo 'deb http://packages.elasticsearch.org/elasticsearch/1.2/debian stable main' > /etc/apt/sources.list.d/elasticsearch.list
RUN apt-get update

# Python YAML is required to generate ElasticSearch's configuration. Maven is
# needed to build the elasticsearch-zookeeper plugin.
RUN apt-get install -y --no-install-recommends maven elasticsearch=1.2.1 openjdk-7-jdk

# Install the ZooKeeper discovery plugin
RUN git clone https://github.com/grmblfrz/elasticsearch-zookeeper.git /tmp/elasticsearch-zookeeper
RUN cd /tmp/elasticsearch-zookeeper && mvn package -Dmaven.test.skip=true -Dzookeeper.version=3.4.6
RUN /usr/share/elasticsearch/bin/plugin -v                                                 		\
  -u file:///tmp/elasticsearch-zookeeper/target/releases/elasticsearch-zookeeper-1.2.0.zip	\
  -i elasticsearch-zookeeper-1.2.0
RUN rm -rf /tmp/elasticsearch-zookeeper

# Install Marvel plugin
RUN /usr/share/elasticsearch/bin/plugin -v -i elasticsearch/marvel/latest

# Install Elasticsearch Head plugin
RUN /usr/share/elasticsearch/bin/plugin -v -i mobz/elasticsearch-head

VOLUME /var/lib/elasticsearch
VOLUME /var/log/elasticsearch
VOLUME /etc/elasticsearch

ADD run.sh /root/

CMD /root/run.sh
