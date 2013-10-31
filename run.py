#!/usr/bin/env python

# Start script for ElasticSearch

import os
import sys
import yaml

os.chdir(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..'))

ELASTICSEARCH_CONFIG_FILE = 'config/elasticsearch.yml'

# Environment variables that drive ElasticSearch's configuration and their defaults.
ELASTICSEARCH_CONFIG_CLUSTER_NAME = os.environ.get('ELASTICSEARCH_CONFIG_CLUSTER_NAME', 'local-elasticsearch')
ELASTICSEARCH_CONFIG_NODE_NAME = os.environ.get('ELASTICSEARCH_CONFIG_NODE_NAME', 'local-es-node')
ELASTICSEARCH_CONFIG_DATA_PATH = os.environ.get('ELASTICSEARCH_CONFIG_DATA_PATH', '/var/lib/elasticsearch')
ELASTICSEARCH_CONFIG_PEER_PORT = int(os.environ.get('ELASTICSEARCH_CONFIG_PEER_PORT', 9300))
ELASTICSEARCH_CONFIG_HTTP_PORT = int(os.environ.get('ELASTICSEARCH_CONFIG_HTTP_PORT', 9200))
ELASTICSEACRH_CONFIG_ZOOKEEPER_BASE = os.environ.get('ELASTICSEACRH_CONFIG_ZOOKEEPER_BASE', '/local/elasticsearch')

CONTAINER_HOST_ADDRESS = os.environ.get('CONTAINER_HOST_ADDRESS', '')
if not CONTAINER_HOST_ADDRESS:
    sys.stderr.write('Container\'s host address is required for ElasticSearch discovery!\n')
    sys.exit(1)

ZOOKEEPER_NODE_LIST = os.environ.get('ZOOKEEPER_NODE_LIST', '')
if not ZOOKEEPER_NODE_LIST:
    sys.stderr.write('ZooKeeper node list is required for the ElasticSearch discovery configuration (set ZOOKEEPER_NODE_LIST)!\n')
    sys.exit(1)

# Prepare the YAML configuration and write it.
with open(ELASTICSEARCH_CONFIG_FILE, 'w+') as conf:
    yaml.dump({
        'cluster.name': ELASTICSEARCH_CONFIG_CLUSTER_NAME,
        'node.name': ELASTICSEARCH_CONFIG_NODE_NAME,
        'path.data': ELASTICSEARCH_CONFIG_DATA_PATH,
        'transport.tcp.port': ELASTICSEARCH_CONFIG_PEER_PORT,
        'http.port': ELASTICSEARCH_CONFIG_HTTP_PORT,
        'network.publish_host': CONTAINER_HOST_ADDRESS,
        'discovery': {
                'type': 'com.sonian.elasticsearch.zookeeper.discovery.ZooKeeperDiscoveryModule',
                'zen.multicast.enabled': False,
        },
        'sonian.elasticsearch.zookeeper': {
                'settings.enabled': False,
                'client.host': ZOOKEEPER_NODE_LIST,
                'discovery.state_publishing.enabled': True,
        },
        'zookeeper.root': ELASTICSEACRH_CONFIG_ZOOKEEPER_BASE,
    }, conf, default_flow_style=False)

# Start ElasticSearch
os.execl('bin/elasticsearch', 'elasticsearch', '-f')
