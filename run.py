#!/usr/bin/env python

# Start script for ElasticSearch

import os
import re
import sys
import yaml

os.chdir(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..'))

ELASTICSEARCH_CONFIG_FILE = 'config/elasticsearch.yml'

CONTAINER_NAME = os.environ.get('CONTAINER_NAME', '')
assert CONTAINER_NAME, 'Container name is missing!'
ELASTICSEARCH_CONFIG_BASE = re.sub(r'[^\w]', '_', CONTAINER_NAME).upper()

CONTAINER_HOST_ADDRESS = os.environ.get('CONTAINER_HOST_ADDRESS', '')
assert CONTAINER_HOST_ADDRESS, 'Container host address is required for ElasticSearch discovery!'

ELASTICSEARCH_CONFIG_CLUSTER_NAME = os.environ.get('ELASTICSEARCH_CONFIG_CLUSTER_NAME', 'local-elasticsearch')
ELASTICSEACRH_CONFIG_ZOOKEEPER_BASE = os.environ.get('ELASTICSEACRH_CONFIG_ZOOKEEPER_BASE', '/local/elasticsearch')
ELASTICSEARCH_CONFIG_PEER_PORT = int(os.environ.get('ELASTICSEARCH_%s_PEER_PORT' % ELASTICSEARCH_CONFIG_BASE, 9300))
ELASTICSEARCH_CONFIG_HTTP_PORT = int(os.environ.get('ELASTICSEARCH_%s_HTTP_PORT' % ELASTICSEARCH_CONFIG_BASE, 9200))

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
        'cluster.name': ELASTICSEARCH_CONFIG_CLUSTER_NAME,
        'node.name': CONTAINER_NAME,
        'path.data': '/var/lib/elasticsearch',
        'transport.tcp.port': ELASTICSEARCH_CONFIG_PEER_PORT,
        'http.port': ELASTICSEARCH_CONFIG_HTTP_PORT,
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
        'zookeeper.root': ELASTICSEACRH_CONFIG_ZOOKEEPER_BASE,
    }, conf, default_flow_style=False)

# Start ElasticSearch
os.execl('bin/elasticsearch', 'elasticsearch', '-f')
