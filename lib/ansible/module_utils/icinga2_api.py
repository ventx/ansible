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
#
# (c) 2017 Wolfgang Felbermeier (@f3lang)
#

import requests
import json
from requests.auth import HTTPBasicAuth
from argparse import ArgumentError


class Icinga2APIError(Exception):
    def __init__(self, message, api_response):
        super(Icinga2APIError, self).__init__(message)
        self.api_response = api_response


class Icinga2APIAuthenticationError(Icinga2APIError):
    pass


class Icinga2APIAccessError(Icinga2APIError):
    pass


class Icinga2APINotFoundError(Icinga2APIError):
    pass


class Icinga2APIServerSideError(Icinga2APIError):
    pass


class Icinga2APIClassError(Exception):
    pass


class Icinga2Object:
    def __init__(self, response_data, status_code):
        if (len(response_data) == 1) & ("code" in response_data.results[0]):
            self.code = response_data.results[0].code
            self.status = response_data.results[0].status
        else:
            self.code = status_code
            self.results = response_data.results


class Icinga2APIClient:
    def __init__(self, url="https://127.0.0.1:5665/v1", username="", password="", cert_path="", cert_key_path="",
                 ignore_server_cert_errors=False):
        if (username == "") & (password == "") & (cert_path == ""):
            raise ArgumentError(username, "Either a username/password combination or the "
                                          "path to a client certificate must be specified.")
        self.url = url
        self.username = username
        self.password = password
        self.cert_path = cert_path
        self.cert_key_path = cert_key_path
        self.ignore_server_cert_errors = ignore_server_cert_errors
        self.basicAuth = (username != "")

    def create_object(self, object_class, object_name=None, attrs=None, templates=None, filter=None,
                      advanced_filter=None,
                      advanced_filter_vars=None):
        url = "objects/" + object_class + (("/" + object_name) if object_name is not None else "")
        if filter is not None:
            url += Icinga2APIClient.create_simple_filter_url(filter)
        payload = Icinga2APIClient.create_payload(attrs, templates, advanced_filter, advanced_filter_vars)
        try:
            self.get_object(object_name)
            result = self.make_api_request(url, "post", payload)
        except Icinga2APINotFoundError:
            result = self.make_api_request(url, "put", payload)
        return result

    def get_object(self, object_class, object_name=None, filter=None, advanced_filter=None, advanced_filter_vars=None):
        url = "objects/" + object_class + (("/" + object_name) if object_name is not None else "")
        if filter is not None:
            url += Icinga2APIClient.create_simple_filter_url(filter)
        payload = None
        if advanced_filter is not None:
            payload = Icinga2APIClient.create_payload(None, None, advanced_filter, advanced_filter_vars)
        return self.make_api_request(url, "get", payload)

    def delete_object(self, object_class, object_name=None, filter=None, advanced_filter=None,
                      advanced_filter_vars=None):
        url = "objects/" + object_class + (("/" + object_name) if object_name is not None else "")
        if filter is not None:
            url += Icinga2APIClient.create_simple_filter_url(filter)
        payload = None
        if advanced_filter is not None:
            payload = Icinga2APIClient.create_payload(None, None, advanced_filter, advanced_filter_vars)
        return self.make_api_request(url, "delete", payload)

    def make_api_request(self, path, request_type, payload=None):
        headers = {
            "Accept": "application/json"
        }
        if self.basicAuth:
            basic_auth = HTTPBasicAuth(self.username, self.password)
            if request_type == "get":
                if payload is not {}:
                    headers["X-HTTP-Method-Override"] = "GET"
                    return Icinga2APIClient.handle_api_response(
                        requests.post(self.url + "/" + path,
                                      headers=headers,
                                      auth=basic_auth,
                                      data=json.dumps(payload),
                                      verify=not self.ignore_server_cert_errors))
                else:
                    return Icinga2APIClient.handle_api_response(
                        requests.post(self.url + "/" + path,
                                      headers=headers,
                                      auth=basic_auth,
                                      verify=not self.ignore_server_cert_errors))

            elif request_type == "put":
                return Icinga2APIClient.handle_api_response(
                    requests.put(self.url + "/" + path,
                                 headers=headers,
                                 auth=basic_auth,
                                 data=json.dumps(payload),
                                 verify=not self.ignore_server_cert_errors))
            elif request_type == "post":
                return Icinga2APIClient.handle_api_response(
                    requests.post(self.url + "/" + path,
                                  headers=headers,
                                  auth=basic_auth,
                                  data=json.dumps(payload),
                                  verify=not self.ignore_server_cert_errors))
            elif request_type == "delete":
                return Icinga2APIClient.handle_api_response(
                    requests.delete(self.url + "/" + path,
                                    headers=headers,
                                    auth=basic_auth,
                                    verify=not self.ignore_server_cert_errors))
        else:
            client_ca = (self.cert_path, self.cert_key_path)
            if request_type == "get":
                if payload is not {}:
                    headers["X-HTTP-Method-Override"] = "GET"
                    return Icinga2APIClient.handle_api_response(
                        requests.post(self.url + "/" + path,
                                      headers=headers,
                                      cert=client_ca,
                                      data=json.dumps(payload),
                                      verify=not self.ignore_server_cert_errors))
                else:
                    return Icinga2APIClient.handle_api_response(
                        requests.post(self.url + "/" + path,
                                      headers=headers,
                                      cert=client_ca,
                                      verify=not self.ignore_server_cert_errors))
            elif request_type == "put":
                return Icinga2APIClient.handle_api_response(
                    requests.put(self.url + "/" + path,
                                 headers=headers,
                                 cert=client_ca,
                                 data=json.dumps(payload),
                                 verify=not self.ignore_server_cert_errors))
            elif request_type == "post":
                return Icinga2APIClient.handle_api_response(
                    requests.post(self.url + "/" + path,
                                  headers=headers,
                                  cert=client_ca,
                                  data=json.dumps(payload),
                                  verify=not self.ignore_server_cert_errors))
            elif request_type == "delete":
                return Icinga2APIClient.handle_api_response(
                    requests.delete(self.url + "/" + path,
                                    headers=headers,
                                    cert=client_ca,
                                    verify=not self.ignore_server_cert_errors))
        raise Icinga2APIClassError("Error invoking make_api_request. Either the authentication is not set "
                                   "or you tried to make an unsupported request.")

    @staticmethod
    def handle_api_response(r):
        if r.status_code > 299:
            Icinga2APIClient.handle_api_error(r.text)
        else:
            return Icinga2Object(r.json, r.status_code)

    @staticmethod
    def handle_api_error(r):
        if r.status_code == 401:
            raise Icinga2APIAuthenticationError("Authentication towards icinga2 API failed", r.text)
        elif r.status_code == 404:
            raise Icinga2APINotFoundError("Target not found in icinga2 API", r.text)
        elif r.status_code == 503:
            raise Icinga2APIAccessError("The specified API User does not have the permission "
                                        "to perform the requested API action", r.text)
        elif r.status_code > 499:
            raise Icinga2APIServerSideError("The icinga2 API returned a server error", r.text)
        else:
            raise Icinga2APIError("There was an error with the request to the icinga2 API", r.text)

    @staticmethod
    def create_simple_filter_url(filter):
        params = []
        for key, value in filter.items():
            params.append(key + "=" + value)
        return "?" + "&".join(params)

    @staticmethod
    def create_payload(attrs=None, templates=None, filter=None, filter_vars=None):
        payload = {}
        if attrs is not None:
            payload.attrs = attrs
        if templates is not None:
            payload.templates = templates
        if filter is not None:
            payload.filter = payload
        if filter_vars is not None:
            payload.filter_vars = filter_vars
        return payload


def icinga2_common_argument_spec():
    return dict(
        url=dict(type='string', required=True),
        user=dict(type='string', required=False, default=''),
        password=dict(type='string', required=False),
        client_cert=dict(type='string', required=False),
        client_cert_pem=dict(type='string', required=False),
        server_ca=dict(type='string', required=False),
        ignore_server_certificate_errors=dict(type='bool', required=False, default=False)
    )


def icinga2_filter_argument_spec():
    return dict(
        simple_filter=dict(type='dict', require=False, default={}),
        advanced_filter=dict(type='dict', require=False, default={}),
        advanced_filter_vars=dict(type='dict', required=False, default={})
    )


def icinga2_options_argument_spec():
    return dict(
        cascade_remove=dict(type='bool', required=False, default=False)
    )
