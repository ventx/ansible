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
module: icinga2_hostgroup

short_description: Manage icinga2 hostgroup over API

version_added: "2.4"

description:
    - Manages hostgroups in icinga2 via API.

requirements:
    - "requests >= 2.18"

options:
    object_name:
        description:
            - The object name of the hostgroup, that should be created 
        required: true
    display_name:
        description:
            - A short description of the host group
    groups:
        description:
            - An array of nested group names
    state:
        description:
            - If C(present), the hostgroup will be created, if not already existent. If C(absent), 
              the hostgroup will be removed, if existent
        choices: [ absent, present ]
        required: true
    cascade_remove:
        description:
            - When you remove a hostgroup, delete all depending objects, too ()

extends_documentation_fragment:
    - icinga2

author:
    - Wolfgang Felbermeier (@f3lang)
'''

EXAMPLES = '''
# Create a simple hostgroup
- name: Create the hostgroup webserver
  icinga2_hostgroup:
    object_name: webserver
    state: present

# Create a simple hostgroup
- name: Create the hostgroup WEBSERVER
  icinga2_hostgroup:
    object_name: webserver
    display_name: WEBSERVER
    groups:
      - linux
      - http
    state: present

# Remove a hostgroup
- name: Create the hostgroup webserver
  icinga2_hostgroup:
    object_name: webserver
    state: absent
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
message:
    description: The output message that the sample module generates
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.icinga2_api import Icinga2APIClient, icinga2_common_argument_spec, \
    icinga2_filter_argument_spec, icinga2_options_argument_spec


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

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        status=0,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        return result

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
