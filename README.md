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

  - `SERVICE_NAME` should contain the logical name of the service this
    container is an instance of;
  - `CONTAINER_NAME` should contain the logical name of the container,
    which will be used for looking up links and ports informations from the
    other environment variables. For this, the name is uppercased and
    non-alphanumeric characters are replaced by underscores. The container name
    will also be used as the ElasticSearch node name;
  - `CONTAINER_HOST_ADDRESS` should contain the address of the Docker
    container's host. It's used by the ElasticSearch ZooKeeper-based discovery
    plugin as the advertised address for node discovery and is required for the
    container to start;

  - `CLUSTER_NAME`, the ElasticSearch cluster name, driving the
    `cluster.name` configuration setting. Defaults to
    `local-elasticsearch`;
  - `ZOOKEEPER_BASE`, the ZooKeeper base zNode path to be
    used by the discovery plugin. Defaults to `/local/elasticsearch`;
  - `<SERVICE_NAME>_<CONTAINER_NAME>_PEER_PORT`, the TCP port used by
    node-to-node communications, driving the `transport.tcp.port`
    setting. Defaults to 9300;
  - `<SERVICE_NAME>_<CONTAINER_NAME>_HTTP_PORT`, the HTTP port for the
    ElasticSearch REST API, driving the `http.port` setting. Defaults to
    9200;

ElasticSearch depends on ZooKeeper for discovery. It thus expects the following
environment variables for each ZooKeeper node to construct the node list:
`ZOOKEEPER_<ZK_NODE_NAME>_HOST` and `ZOOKEEPER_<ZK_NODE_NAME>_CLIENT_PORT`.

Volumes
-------

The ElasticSearch image uses the following volumes you may want to bind from
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
