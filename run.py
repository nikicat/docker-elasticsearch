#!/usr/bin/env python

# Copyright (C) 2013 SignalFuse, Inc.

# Start script for ElasticSearch.
# Requires python-yaml for configuration writing.

import os
import sys
import yaml

from maestro.guestutils import *

os.chdir(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..'))

# Prepare the YAML configuration and write it.
with open(os.path.join('config', 'elasticsearch.yml'), 'w+') as conf:
    yaml.dump({
        'cluster.name': os.environ.get('CLUSTER_NAME',
                                       '{}-elasticsearch'.format(get_environment_name())),
        'node.name': get_container_name(),
        'path.data': '/var/lib/elasticsearch',
        'transport.tcp.port': get_port('peer', 9300),
        'http.port': get_port('http', 9200),
        'network.publish_host': get_container_host_address(),
        'discovery': {
                'type': 'com.sonian.elasticsearch.zookeeper.discovery.ZooKeeperDiscoveryModule',
                'zen.multicast.enabled': False,
        },
        'sonian.elasticsearch.zookeeper': {
                'settings.enabled': False,
                'client.host': ','.join(get_node_list('zookeeper', ports=['client'])),
                'discovery.state_publishing.enabled': True,
        },
        'zookeeper.root': os.environ.get('ZOOKEEPER_BASE',
                                         '/{}/elasticsearch'.format(get_environment_name())),
    }, conf, default_flow_style=False)

# Start ElasticSearch
os.execl('bin/elasticsearch', 'elasticsearch', '-f')
