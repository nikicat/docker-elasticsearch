ElasticSearch on Docker
=======================

This `Dockerfile` creates a Docker image that can be used as the base for
running ElasticSearch within a Docker container. It uses the ElasticSearch
ZooKeeper discovery plugin instead of the standard Zen multicast discovery to
allow for proper operation in PaaS/IaaS/cloud environments that are
multicast-hostile. The run script is responsible for creating the ElasticSearch
configuration based on the container's environment and starting the
ElasticSearch service.

The version of ElasticSearch used is defined in the `Dockerfile` and generally
points to the latest stable release of ElasticSearch.

Environment variables
---------------------

The following environment variables are understood by the startup script to
seed the service's configuration:

  - `CONTAINER_HOST_ADDRESS` should contain the address of the Docker
    container's host. It's used by the ElasticSearch ZooKeeper-based discovery
    plugin as the advertised address for node discovery and is required for the
    container to start;
  - `ELASTICSEARCH_CONFIG_CLUSTER_NAME`, the ElasticSearch cluster name,
    driving the `cluster.name` configuration setting. Defaults to
    `ElasticSearch cluster`;
  - `ELASTICSEARCH_CONFIG_NODE_NAME`, the name of this ElasticSearch node,
    driving the `node.name` configuration setting. Defaults to `Local node`;
  - `ELASTICSEARCH_CONFIG_PEER_PORT`, the TCP port used by node-to-node
    communications, driving the `transport.tcp.port` setting. Defaults to 9300;
  - `ELASTICSEARCH_CONFIG_HTTP_PORT`, the HTTP port for the ElasticSearch REST
    API, driving the `http.port` setting. Defaults to 9200;
  - `ELASTICSEARCH_CONFIG_ZOOKEEPER_BASE`, the ZooKeeper base zNode path to be
    used by the discovery plugin. Defaults to `/local/elasticsearch`;
  - `ZOOKEEPER_NODE_LIST`, the comma-separated list of ZooKeeper nodes to
    connect to for node discovery.

Volumes
-------

The ElasticSearch image uses the following volumes you way want to bind from
the container's host:

  - `/var/lib/elasticsearch`, for the ElasticSearch indeces storage.

Usage
-----

To build a new image, simply run from this directory:

```
$ docker build -t `whoami`/elasticsearch:0.90.5 .
```

The Docker image will be built and now available for Docker to start a new
container from:

```
$ docker images | grep elasticsearch
mpetazzoni/elasticsearch   0.90.5              aa4827a39a60        23 minutes ago      12.29 kB (virtual 890.2 MB)
```
