#!/usr/bin/env python

# Copyright (C) 2013 SignalFuse, Inc.

# Start script for ElasticSearch.
# Requires python-yaml for configuration writing.

import os
import re
import sys
import yaml

if __name__ != '__main__':
    sys.stderr.write('This script is only meant to be executed.\n')
    sys.exit(1)

os.chdir(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..'))

ELASTICSEARCH_CONFIG_FILE = 'config/elasticsearch.yml'

# Get container/instance name.
CONTAINER_NAME = os.environ.get('CONTAINER_NAME', '')
assert CONTAINER_NAME, 'Container name is missing!'
CONFIG_BASE = re.sub(r'[^\w]', '_', CONTAINER_NAME).upper()

# Get container's host IP address/hostname.
CONTAINER_HOST_ADDRESS = os.environ.get('CONTAINER_HOST_ADDRESS', '')
assert CONTAINER_HOST_ADDRESS, 'Container host address is required for ElasticSearch discovery!'

# Gather configuration settings from environment.
ELASTICSEARCH_CLUSTER_NAME = os.environ.get('ELASTICSEARCH_CLUSTER_NAME', 'local-elasticsearch')
ELASTICSEACRH_ZOOKEEPER_BASE = os.environ.get('ELASTICSEACRH_ZOOKEEPER_BASE', '/local/elasticsearch')
ELASTICSEARCH_PEER_PORT = int(os.environ.get('ELASTICSEARCH_{}_PEER_PORT'.format(CONFIG_BASE), 9300))
ELASTICSEARCH_HTTP_PORT = int(os.environ.get('ELASTICSEARCH_{}_HTTP_PORT'.format(CONFIG_BASE), 9200))

# Build ZooKeeper node list with host and client port for each node.
ZOOKEEPER_NODE_LIST = []
for k, v in os.environ.iteritems():
    m = re.match(r'^ZOOKEEPER_(\w+)_HOST$', k)
    if not m: continue
    ZOOKEEPER_NODE_LIST.append(
        '%s:%d' % (v, int(os.environ['ZOOKEEPER_%s_CLIENT_PORT' % m.group(1)])))
assert ZOOKEEPER_NODE_LIST, 'ZooKeeper nodes are required for ElasticSearch discovery!'

# Prepare the YAML configuration and write it.
with open(ELASTICSEARCH_CONFIG_FILE, 'w+') as conf:
    yaml.dump({
        'cluster.name': ELASTICSEARCH_CLUSTER_NAME,
        'node.name': CONTAINER_NAME,
        'path.data': '/var/lib/elasticsearch',
        'transport.tcp.port': ELASTICSEARCH_PEER_PORT,
        'http.port': ELASTICSEARCH_HTTP_PORT,
        'network.publish_host': CONTAINER_HOST_ADDRESS,
        'discovery': {
                'type': 'com.sonian.elasticsearch.zookeeper.discovery.ZooKeeperDiscoveryModule',
                'zen.multicast.enabled': False,
        },
        'sonian.elasticsearch.zookeeper': {
                'settings.enabled': False,
                'client.host': ','.join(ZOOKEEPER_NODE_LIST),
                'discovery.state_publishing.enabled': True,
        },
        'zookeeper.root': ELASTICSEACRH_ZOOKEEPER_BASE,
    }, conf, default_flow_style=False)

# Start ElasticSearch
os.execl('bin/elasticsearch', 'elasticsearch', '-f')
