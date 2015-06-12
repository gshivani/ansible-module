#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Shivani Gowrishankar <s.gowrishankar@ntoggle.com>
#

# Import Datadog
try:
    from datadog import initialize, api
    HAS_DATADOG = True
except:
    HAS_DATADOG = False

DOCUMENTATION = '''
---
module: datadog_tag
short_description: Manages Datadog tags of hosts
description:
- "Manages tags of hosts within Datadog"
- "Options like described on http://docs.datadoghq.com/api/"
version_added: "2.0"
author: '"Shivani Gowrishankar" <s.gowrishankar@ntoggle.com>'
notes: []
requirements: [datadog]
options:
    api_key:
        description: ["Your DataDog API key."]
        required: true
    app_key:
        description: ["Your DataDog app key."]
        required: true
    host:
        description:["Tags of a particular host"]
        required: False
        default: null
    operation: 
        description: ["The type of operation to handle tags of a host"]
        required: true
        choices: ['get', 'add', 'update', 'remove']
    source:
        description: ["The source of the tags"]
        required: false
        default: null
    by_source:
        description: ["A boolean indicating whether tags returned are grouped by source"]
        required: false
        default: False
    tags: 
        description: ["Comma separated list of tags to apply to the host"]
        required: true
        default: null
'''

EXAMPLES = '''
# Get tags
datadog_tag:
  host: "Test host"
  operation: "get"
  api_key: "9775a026f1ca7d1c6c5af9d94d9595a4"
  app_key: "87ce4a24b5553d2e482ea8a8500e71b8ad4554ff"

# Deletes all tags 
datadog_tag:
  host: "Test host"
  operation: "remove"
  api_key: "9775a026f1ca7d1c6c5af9d94d9595a4"
  app_key: "87ce4a24b5553d2e482ea8a8500e71b8ad4554ff"

# Adds the list of tags
datadog_tag:
  host: "Test host"
  operation: "add"
  tags:['tag1']
  api_key: "9775a026f1ca7d1c6c5af9d94d9595a4"
  app_key: "87ce4a24b5553d2e482ea8a8500e71b8ad4554ff"
  
 # Updates the list of tags
datadog_tag:
  host: "Test host"
  operation: "update"
  tags:['tag1']
  api_key: "9775a026f1ca7d1c6c5af9d94d9595a4"
  app_key: "87ce4a24b5553d2e482ea8a8500e71b8ad4554ff"
  
'''

def main():
    module = AnsibleModule(
        argument_spec=dict(
            api_key=dict(required=True),
            app_key=dict(required=True),
            host=dict(required=False),
            operation=dict(required=True, choices=['get', 'add', 'update', 'remove']),
            source=dict(required=False, default=None),
            by_source=dict(required=False, default=False, choices=BOOLEANS),
            tags=dict(required=False)
        )
    )
    
    # Prepare Datadog
    if not HAS_DATADOG:
        module.fail_json(msg='datadogpy required for this module')

    options = {
        'api_key': module.params['api_key'],
        'app_key': module.params['app_key']
    }
    
    initialize(**options)
    
    
    if module.params['operation'] == 'add':
        create_tags (module)
    elif module.params['operation'] == 'remove':
        delete_tags(module)
    elif module.params['operation'] == 'update':
        update_tags(module)
    elif module.params['operation'] == 'get':
        get_tags(module)
   
def get_tags(module):
    try:
        hosts = api.Infrastructure.search(q=module.params['host'])
        msg = api.Tag.get(hosts['results']['hosts'][0], by_source=module.boolean(module.params['by_source']), 
        source=module.params['source'])
        if 'errors' in msg:
            module.fail_json(msg=str(msg['errors']))
        else:
            module.exit_json(msg=msg)
    except Exception, e:
        module.fail_json(msg=str(e))
              
def create_tags(module):
    try:
        hosts = api.Infrastructure.search(q=module.params['host'])
        msg = api.Tag.create(hosts['results']['hosts'][0], tags=module.params['tags'].split(), 
        source=module.params['source'])
        if 'errors' in msg:
            module.fail_json(msg=str(msg['errors']))
        else:
            module.exit_json(changed=True, msg=msg)
    except Exception, e:
        module.fail_json(msg=str(e))

def update_tags(module):
    try:
        msg = api.Tag.update(module.params['host'], tags=module.params['tags'].split(), 
        source=module.params['source'])
        if 'errors' in msg:
            module.fail_json(msg=str(msg['errors']))
        else:
            module.exit_json(changed=True, msg=msg)
    except Exception, e:
        module.fail_json(msg=str(e))

def delete_tags(module):
    try:
        msg = api.Tag.delete(module.params['host'], source=module.params['source'])
        module.exit_json(changed=True, msg=msg)
    except Exception, e:
        module.fail_json(msg=str(e))


from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
main()
