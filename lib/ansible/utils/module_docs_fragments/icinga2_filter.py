#
# (c) 2017, Wolfgang Felbermeier <@f3lang>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.


class ModuleDocFragment(object):

    DOCUMENTATION = '''
---
options:
  filter:
    type: dict
    description:
      - A simple dictionary of filters to apply to your requests. The filters will be decoded in the get URL
    required: false
  advanced_filter:
    type: list
    description:
      - You can either apply the regular filters or the supercharged advanced filters. 
        For more details, how they work, visit U(https://www.icinga.com/docs/icinga2/latest/doc/12-icinga2-api/#advanced-filters)
        To use them in this module, just a define them as a list of strings here. If you need to use the filter_vars, use
        I(advanced_filter_vars)
  advanced_filter_vars:
    type: dict
    description:
      - If you used advanced_filters, the probability is high, that you also need to use filter_vars. Soo.. here you go.
        Define the filters as a dictionary. 
'''
