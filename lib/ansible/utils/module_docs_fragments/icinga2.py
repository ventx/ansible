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
  url:
    description:
      - The Base URL of the icinga API
    required: false
    default: https://127.0.0.1:5665/v1
  username:
    description:
      - The APIUser for the icinga2 API if BaseAuth is enables. Either I(user) and I(password) 
        or I(x509cert) must be submitted
  password:
    description:
      - The password for the APIUser of the icinga2 API
  client_cert:
    description:
      - The path to the client certificate to use for authentication against the icinga API. Either I(user) 
        and I(password) or I(x509cert) must be submitted
  client_cert_pem:
    description:
      - The path to the client certificate pem key.
  server_ca:
    description:
      - If you have a self signed certificate on the server, you can supply the path to the ca 
        to validate the server certificate
  ignore_server_certificate_errors:
    description:
      - Ignore errors with the server certificate
    default: False
'''
