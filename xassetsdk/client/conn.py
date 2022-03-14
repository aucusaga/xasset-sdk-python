#!/usr/bin python3
# -*- coding: utf-8 -*-
# @file       : conn.py
# @create time: 2022/03/10
# @说明       : 本文件实现了http通信功能

from email.errors import HeaderParseError
import os, sys

import urllib3
sys.path.append(os.getcwd())

import time
import json
import requests
import hashlib
from xassetsdk.common.config import XassetCliConfig
from xassetsdk.auth.bce import BceCredentials
from xassetsdk.auth.bce import sign

class Conn(object):
    def post(self, uri, data):
        url = self._cfg._url + uri
        response = requests.post(url=url, data=data)
        resp = {}
        try:
            resp = json.loads(response.text)
        except:
            print('resp err, resp: %s' % response)
        return resp
    
    def sign_post(self, path, data):
        host = urllib3.get_host(self._cfg._url)
        md5_msg = json.dumps(data).encode('utf-8')
        md5 = hashlib.md5(md5_msg).hexdigest().lower()
        headers = {
		    'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
		    'content-md5': md5,
            'host': host[1],
            'AppId': '%d' % self._cfg._app_id,
	    }
        headers_to_sign = {
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
		    'content-md5': md5,
            'host': host[1],
        }

        sign = self.sign('POST', path, headers, headers_to_sign)
        headers['Authorization'] = sign
        url = self._cfg._url + path
        response = requests.post(url=url, data=data, headers=headers)
        resp = {}
        try:
            resp = json.loads(response.text)
        except:
            print('resp err, resp: %s' % response)
        return resp

    def app_id(self):
        return self._cfg._app_id

    def ak(self):
        return self._cfg._ak

    def sk(self):
        return self._cfg._sk

    def sign(self, method, uri, headers, headers_to_sign):
        credentials = BceCredentials(self.ak(), self.sk())
        timestamp = int(time.time())
        result = sign(credentials=credentials, http_method=method, path=uri, headers=headers, headers_to_sign=headers_to_sign, params={}, timestamp=timestamp)
        return result

    def __init__(self, ui, app_id, ak, sk):
        config = XassetCliConfig(ui, app_id, ak, sk)
        self._cfg = config


