ElasticSearch on Docker
=======================

This `Dockerfile` creates a Docker image that can be used as the base for
running ElasticSearch within a Docker container. The run script is responsible
for creating the ElasticSearch configuration based on the container's
environment and starting the ElasticSearch service.

The version of ElasticSearch used is defined in the `Dockerfile` and generally
points to the latest stable release of ElasticSearch.

Environment variables
---------------------

The following environment variables are understood by the startup script to
seed the service's configuration:

  - `ELASTICSEARCH_CONFIG_CLUSTER_NAME`, the ElasticSearch cluster name,
    driving the `cluster.name` configuration setting. Defaults to
    `ElasticSearch cluster`;
  - `ELASTICSEARCH_CONFIG_NODE_NAME`, the name of this ElasticSearch node,
    driving the `node.name` configuration setting. Defaults to `Local node`;
  - `ELASTICSEARCH_CONFIG_DATA_PATH`, a path, or comma-separated list of paths,
    to where ElasticSearch will store the persistent node data. Defaults to
    `/var/lib/elasticsearch`;
  - `ELASTICSEARCH_CONFIG_PEER_PORT`, the TCP port used by node-to-node
    communications, driving the `transport.tcp.port` setting. Defaults to 9300;
  - `ELASTICSEARCH_CONFIG_HTTP_PORT`, the HTTP port for the ElasticSearch REST
    API, driving the `http.port` setting. Defaults to 9200.

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
