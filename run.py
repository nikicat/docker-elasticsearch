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
ELASTICSEARCH_CONFIG_CLUSTER_NAME = os.environ.get('ELASTICSEARCH_CONFIG_CLUSTER_NAME', 'ElasticSearch cluster')
ELASTICSEARCH_CONFIG_NODE_NAME = os.environ.get('ELASTICSEARCH_CONFIG_NODE_NAME', 'Local node')
ELASTICSEARCH_CONFIG_PEER_PORT = int(os.environ.get('ELASTICSEARCH_CONFIG_PEER_PORT', 9300))
ELASTICSEARCH_CONFIG_HTTP_PORT = int(os.environ.get('ELASTICSEARCH_CONFIG_HTTP_PORT', 9200))

# Prepare the YAML configuration and write it.
with open(ELASTICSEARCH_CONFIG_FILE, 'w+') as conf:
    yaml.dump({
        'cluster.name': ELASTICSEARCH_CONFIG_CLUSTER_NAME,
        'node.name': ELASTICSEARCH_CONFIG_NODE_NAME,
        'transport.tcp.port': ELASTICSEARCH_CONFIG_PEER_PORT,
        'http.port': ELASTICSEARCH_CONFIG_HTTP_PORT,
        'discovery.zen.multicast.enabled': False
    }, conf, default_flow_style=False)

# Start ElasticSearch
os.execl('bin/elasticsearch', 'elasticsearch', '-f')
