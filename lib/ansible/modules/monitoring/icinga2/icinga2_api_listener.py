#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (c) 2017, Wolfgang Felbermeier <wolfgang@ventx.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: icinga2_api_listener
short_description: Manage icinga2 api listener endpoints over API
description:
    - ApiListener objects are used for distributed monitoring setups and API usage specifying 
      the certificate files used for ssl authorization and additional restrictions.
      While Icinga 2 and the underlying OpenSSL library use sane and secure defaults, 
      the attributes cipher_list and tls_protocolmin can be used to increase communication security. 
      A good source for a more secure configuration is provided by the Mozilla Wiki 
      (U(https://wiki.mozilla.org/Security/Server_Side_TLS)). 
      Ensure to use the same configuration for both attributes on all endpoints to avoid 
      communication problems which requires to use cipher_list compatible with the endpoint 
      using the oldest version of the OpenSSL library. If using other tools to connect 
      to the API ensure also compatibility with them as this setting affects not only 
      inter-cluster communication but also the REST API. 
version_added: "2.4"
author:
  - Wolfgang Felbermeier, @f3lang
requirements: [ "requests" ]
options:
  ticket_salt:
    type: string
    description: 'Private key for CSR auto-signing. Required for a signing master instance.'
  crl_path:
    type: string
    description: 'Path to the CRL file.'
  bind_host:
    type: string
    default: 0.0.0.0
    description: 'The IP address the api listener should be bound to. Defaults to 0.0.0.0.'
  bind_port:
    type: int
    default: '5665'
    description: 'The port the api listener should be bound to. Defaults to 5665.'
  accept_config:
    type: bool
    default: 'false'
    description: 'Accept zone configuration. Defaults to false.'
  accept_commands:
    type: bool
    default: 'false'
    description: 'Accept remote commands. Defaults to false.'
  cipher_list:
    type: string
    default: 'ALL:!LOW:!WEAK:!MEDIUM:!EXP:!NULL'
    description: 'Cipher list that is allowed. For a list of available ciphers run openssl ciphers. Defaults to ALL:!LOW:!WEAK:!MEDIUM:!EXP:!NULL.'
  tls_protocolmin:
    type: string
    default: TLSv1
    description: 'Minimum TLS protocol version. Must be one of TLSv1, TLSv1.1 or TLSv1.2. Defaults to TLSv1.'
  access_control_allow_origin:
    type: list
    description: 'Specifies an array of origin URLs that may access the API. U(https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS#Access-Control-Allow-Origin)'
  access_control_allow_credentials:
    type: bool
    default: 'true'
    description: 'Indicates whether or not the actual request can be made using credentials. Defaults to true. U(https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS#Access-Control-Allow-Credentials)'
  access_control_allow_headers:
    type: string
    default: Authorization
    description: 'Used in response to a preflight request to indicate which HTTP headers can be used when making the actual request. Defaults to Authorization. U(https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS#Access-Control-Allow-Headers)'
  access_control_allow_methods:
    type: string
    default: 'GET, POST, PUT, DELETE'
    description: 'Used in response to a preflight request to indicate which HTTP methods can be used when making the actual request. Defaults to GET, POST, PUT, DELETE. U(https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS#Access-Control-Allow-Methods)'
      
extends_documentation_fragment:
    - icinga2
notes:
    - "Further details here: U(https://www.icinga.com/docs/icinga2/latest/doc/09-object-types/#apilistener)"
'''

EXAMPLES = '''
# Create a simple hostgroup
- name: Create the hostgroup webserver
  icinga2_hostgroup:
    name: webserver
    state: present

# Create a simple hostgroup
- name: Create the hostgroup WEBSERVER
  icinga2_hostgroup:
    name: webserver
    display_name: WEBSERVER
    groups:
      - linux
      - http
    state: present

# Remove a hostgroup
- name: Create the hostgroup webserver
  icinga2_hostgroup:
    name: webserver
    state: absent
'''

RETURN = '''
status:
    description: The HTTP status of the icinga2 API reply
    type: int
results:
    description: The results returned by the icinga2 API. If you queried the API, contains an array with all available hostgroups
    type: complex
    contains:
        attrs:
            description: The attributes of the hostgroup
            type: complex
            contains:
                action_url:
                    description: URL for actions for the host (for example, an external graphing tool) 
                    type: string
                display_name:
                    description: A short description of the host group.
                    type: string
                groups:
                    description: An array of nested group names.
                    type: list
                ha_mode:
                    description: 
                    type: int
                name:
                    description: The name of the hostgroup
                    type: string
                notes:
                    description: Notes for the host
                    type: string
                notes_url:
                    description: URL for notes for the host (for example, in notification commands)
                    type: string
                original_attributes:
                    description: Original values of object attributes modified at runtime
                    type: complex
                package:
                    description: Configuration package name this object belongs to. Local configuration is set to _etc, runtime created objects use _api
                    type: string
                paused:
                    description: Object has been paused at runtime (e.g. IdoMysqlConnection. Defaults to false
                    type: boolean
                source_location:
                    description: Location information where the configuration files are stored
                    type: complex
                    contains:
                        first_column:
                            type: int
                        first_line:
                            type: int
                        last_column:
                            type: int
                        last_line:
                            type: int
                        path:
                            description: The path of the configuration file
                            type: string
                templates:
                    description: Templates imported on object compilation
                    type: list
                type:
                    description: The type of the element. In this case "HostGroup"
                vars:
                    description: A dictionary containing custom attributes that are available globally
                    type: complex
                version:
                    description: Timestamp when the object was created or modified. Synced throughout cluster nodes
                    type: int
                zone:
                    description: Optional. The zone this object is a member of. Please read the distributed monitoring chapter (U(https://www.icinga.com/docs/icinga2/latest/doc/06-distributed-monitoring/#distributed-monitoring))for details
                    type: string
        joins:
            description: Icinga 2 knows about object relations. For example it can optionally return information about the host when querying service objects
            type: complex
        meta:
            description: Enable meta information using ?meta=used_by (references from other objects) and/or ?meta=location (location information) specified as list. Defaults to disabled
            type: complex
        name:
            description: The name of the hostgroup
            type: string
        type:
            description: The type of the element. In this case "HostGroup"
            type: string
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.icinga2_api import icinga2_common_argument_spec, \
    icinga2_filter_argument_spec, icinga2_options_argument_spec, create_icinga2_api_client


def run_module():
    module_args = dict(
        object_name=dict(type='str', required=True),
        display_name=dict(type='str', required=False),
        groups=dict(type='list', required=False, default=[]),
        state=dict(type='str', required=True, choices=['present', 'absent'])
    )
    module_args.update(icinga2_filter_argument_spec())
    module_args.update(icinga2_options_argument_spec())
    module_args.update(icinga2_common_argument_spec())

    result = dict(
        status=0,
        results=dict()
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    connection = create_icinga2_api_client(module)
    if module.params['state'] == 'present':
        attrs = dict(
            display_name=module.params['display_name'],
            groups=module.params['groups']
        )
        attrs = dict((k, v) for k, v in attrs.iteritems() if v)
        api_result = connection.create_object(object_class='hostgroups', object_name=module.params['object_name'],
                                              attrs=attrs)
        if api_result.code == 200:
            api_result = connection.get_object('hostgroups', module.params['object_name'])
    else:
        api_result = connection.delete_object('hostgroups', module.params['object_name'])

    result['status'] = api_result.code
    result['results'] = api_result.results
    result['changed'] = api_result.changed

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
