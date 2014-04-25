# Dockerfile for ElasticSearch

FROM yandex/ubuntu:14.04
MAINTAINER Nikolay Bryskin <devel.niks@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

# Install maestro-ng
RUN curl https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py | python && rm *.zip && python -m easy_install -H *.python.org git+git://github.com/signalfuse/maestro-ng

# Get the latest stable version of ElasticSearch
RUN wget -O - http://packages.elasticsearch.org/GPG-KEY-elasticsearch | apt-key add -
RUN echo 'deb http://packages.elasticsearch.org/elasticsearch/1.1/debian stable main' > /etc/apt/sources.list.d/elasticsearch.list
RUN apt-get update

# Python YAML is required to generate ElasticSearch's configuration. Maven is
# needed to build the elasticsearch-zookeeper plugin.
RUN apt-get install -y --no-install-recommends maven elasticsearch=1.1.0 openjdk-7-jdk

# Install the ZooKeeper discovery plugin
RUN git clone https://github.com/kpruden/elasticsearch-zookeeper.git /tmp/elasticsearch-zookeeper
RUN cd /tmp/elasticsearch-zookeeper && mvn package -Dmaven.test.skip=true -Dzookeeper.version=3.4.6
RUN /usr/share/elasticsearch/bin/plugin -v                                                 		\
  -u file:///tmp/elasticsearch-zookeeper/target/releases/elasticsearch-zookeeper-1.1.0-SNAPSHOT.zip	\
  -i elasticsearch-zookeeper-1.1.0-SNAPSHOT
RUN rm -rf /tmp/elasticsearch-zookeeper

# Install Marvel plugin
RUN /usr/share/elasticsearch/bin/plugin -v -i elasticsearch/marvel/latest

ADD run.py /etc/elasticsearch/.docker/
ADD mapping.json /etc/elasticsearch/

WORKDIR /opt/elasticsearch-1.1.0
VOLUME /var/lib/elasticsearch
VOLUME /var/log/elasticsearch
CMD ["python", "/etc/elasticsearch/.docker/run.py"]
