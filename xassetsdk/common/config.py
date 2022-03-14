#!/usr/bin python3
# -*- coding: utf-8 -*-
# @file       : config.py
# @create time: 2022/03/10
# @说明       : 本文件实现了配置功能，在本文件可直接配置访问UI参数

# python-sdk flag
UserAgentDefault      = "xasset-sdk-python"
ConnectTimeoutMsDef   = 1000
ReadWriteTimeoutMsDef = 3000

# U联调地址
ui = ""

# 请指定预分配的 AppId, Ak, SK
app_id = 0
ak = ""
sk = ""

class XassetCliConfig(object):
    def __init__(self, ui, app_id, ak, sk):
        self._url = ui
        self._agent = UserAgentDefault
        self._conn_timeout = ConnectTimeoutMsDef
        self._read_timeout = ReadWriteTimeoutMsDef
        self._app_id = app_id
        self._ak = ak
        self._sk = sk
