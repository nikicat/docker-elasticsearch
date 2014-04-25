#!/usr/bin/env python

# Copyright (C) 2013-2014 SignalFuse, Inc.

# Start script for ElasticSearch.
# Requires python-yaml for configuration writing.

import os
import yaml
import subprocess

from maestro.guestutils import *
from maestro.extensions.logging.logstash import run_service

os.chdir(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..'))

# Prepare the YAML configuration and write it.
with open('elasticsearch.yml', 'w+') as conf:
    yaml.dump({
        'cluster.name': os.environ.get('CLUSTER_NAME',
                                       '{}-elasticsearch'.format(get_environment_name())),
        'node': {
            'name': get_container_name(),
            'datacenter': os.environ.get('DATACENTER'),
        },
        'path.data': '/var/lib/elasticsearch',
        'transport.tcp.port': get_port('peer', 9300),
        'http.port': get_port('http', 9200),
        'network.publish_host': get_container_host_address(),
        'discovery': {
                'type': 'com.sonian.elasticsearch.zookeeper.discovery.ZooKeeperDiscoveryModule',
                'zen.multicast.enabled': False,
        } if os.environ.get('DISCOVERY', 'zen') == 'zookeeper' else {
                'type': 'zen',
                'zen.minimum_master_nodes': (len(get_node_list(get_service_name(), ports=['peer'])) + 1) // 2,
                'zen.ping.multicast.enabled': False,
                'zen.ping.unicast.hosts': get_node_list(get_service_name(), ports=['peer']),
        },
        'sonian.elasticsearch.zookeeper': {
                'settings.enabled': False,
                'client.host': ','.join(get_node_list('zookeeper', ports=['client'])),
                'discovery.state_publishing.enabled': True,
        },
        'zookeeper.root': os.environ.get('ZOOKEEPER_BASE',
                                         '/{}/elasticsearch'.format(get_environment_name())),
        'cluster.routing.allocation': {
            'awareness': {
                'force.datacenter.values': os.environ.get('DATACENTERS').replace(' ', ','),
                'attributes': 'datacenter',
            },
            'cluster_concurrent_rebalance': 10,
            'disk.threshold_enabled': True,
            'node_initial_primaries_recoveries': 10,
            'node_concurrent_recoveries': 10,
        },
        'index': {
            'number_of_shards': os.environ.get('NUMBER_OF_SHARDS', 5),
            'number_of_replicas': os.environ.get('NUMBER_OF_REPLICAS', 2),
            'mapper.default_mapping_location': 'mapping.json',
            'query.default_field': 'msg',
            'store.type': 'mmapfs',
            'translog.flush_threshold_ops': 50000,
            'refresh_interval': '10s',
        },
        'indices': {
            'recovery.concurrent_streams': 20,
            'memory.index_buffer_size': '30%',
        },
        'marvel.agent.exporter.es.hosts': ['{}:{}'.format(get_container_internal_address(), get_port('http', 9200))]
    }, conf, default_flow_style=False)

# Start ElasticSearch
#run_service(['bin/elasticsearch'],
# TODO(mpetazzoni): use logtype with next version of Maestro.
#        logtype='elasticsearch',
#        logbase='/var/log/elasticsearch',
#        logtarget='logstash')
subprocess.call(['/usr/share/elasticsearch/bin/elasticsearch'])
