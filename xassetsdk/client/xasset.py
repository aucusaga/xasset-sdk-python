#!/usr/bin python3
# -*- coding: utf-8 -*-
# @file       : xasset.py
# @create time: 2022/03/10
# @说明       : 本文件实现了请求xasset-ui的逻辑

import os, sys
sys.path.append(os.getcwd())

import json
from xassetsdk.client.conn import Conn
from xassetsdk.util.utils import Util
from xassetsdk.auth.account import XassetAccount

Browser_Srdscir_URI = '/xasset/browser/v1/srdscir'
Browser_QueryAsset_URI =  '/xasset/browser/v1/queryasset'

QueryAsset_URI =  '/xasset/horae/v1/query'
CreateAsset_URI = '/xasset/horae/v1/create'
PublishAsset_URI = '/xasset/horae/v1/publish'
FreezeAsset_URI =  '/xasset/horae/v1/freeze'
GrantAsset_URI =  '/xasset/horae/v1/grant'

QueryShard_URI = '/xasset/horae/v1/querysds'
TransferShard_URI =  '/xasset/damocles/v1/transfer'
ConsumeShard_URI = '/xasset/horae/v1/consume'

def sign_msg(asset_id, account_json):
    nonce = Util.gen_nonce()
    addr = account_json['addr']
    sk = account_json['sk']
    account = XassetAccount(addr, sk)
    signMsg = '%d%d' % (asset_id, nonce)
    sign = account.sign_ecdsa(signMsg)
    data = {
        'nonce': nonce,
        'addr': addr,
        'pkey': account.public_key(),
        'sign': sign,
    }
    return data

class Xasset(object):
    def browser_srdscir(self, asset_id):
        data = {}
        data['asset_id'] = asset_id
        return self._conn.post(Browser_Srdscir_URI, data)

    def browser_query_asset(self, asset_id, page, limit):
        data = {}
        data['asset_id'] = asset_id
        data['page'] = page
        data['limit'] = limit
        return self._conn.post(Browser_QueryAsset_URI, data)

    def query_asset(self, param):
        asset_id = param['asset_id']
        data = {
            'asset_id': asset_id,
        }
        resp = self._conn.sign_post(QueryAsset_URI, data)
        if 'errno' not in resp.keys():
            print("panic, resp: %s" % resp)
            return None
        if resp['errno'] != 0:
            print("error, resp: %s" % resp)
            return None
        print("query succ. resp: %s" % resp)
        return resp['meta']

    def query_shard(self, param):
        data = {
            'asset_id': param['asset_id'],
            'shard_id': param['shard_id'],
        }
        resp = self._conn.sign_post(QueryShard_URI, data)
        if 'errno' not in resp.keys():
            print("panic, resp: %s" % resp)
            return None
        if resp['errno'] != 0:
            print("error, resp: %s" % resp)
            return None
        print("query shard succ. resp: %s" % resp)
        return resp['meta']

    def create_asset(self, param):
        asset_id = Util.gen_asset_id(self._conn.app_id())
        data = sign_msg(asset_id, param['account'])
       
        data['asset_info'] = json.dumps(param['asset_info'])
        data['asset_id'] = asset_id
        if 'price' in param.keys():
            data['price'] = param['price']
        if 'amount' in param.keys():
            data['amount'] = param['amount']
        if 'user_id' in param.keys():
            data['user_id'] = param['user_id']

        resp = self._conn.sign_post(CreateAsset_URI, data)
        if 'errno' not in resp.keys():
            print("panic, resp: %s" % resp)
            return None
        if resp['errno'] != 0:
            print("error, resp: %s" % resp)
            return None
        print("create succ. resp: %s" % resp)
        return resp['asset_id']

    def publish_asset(self, param):
        asset_id = param['asset_id']
        data = sign_msg(asset_id, param['account'])
       
        data['asset_id'] = asset_id
        if 'is_evidence' in param.keys():
            data['is_evidence'] = param['is_evidence']
        
        resp = self._conn.sign_post(PublishAsset_URI, data)
        if 'errno' not in resp.keys():
            print("panic, resp: %s" % resp)
            return None
        if resp['errno'] != 0:
            print("error, resp: %s" % resp)
            return None
        print("publish succ. resp: %s" % resp)
        return 0

    def freeze_asset(self, param):
        asset_id = param['asset_id']
        data = sign_msg(asset_id, param['account'])
        data['asset_id'] = '%d' % asset_id
    
        resp = self._conn.sign_post(FreezeAsset_URI, data)
        if 'errno' not in resp.keys():
            print("panic, resp: %s" % resp)
            return None
        if resp['errno'] != 0:
            print("error, resp: %s" % resp)
            return None
        print("freeze succ. resp: %s" % resp)
        return 0
        
    def grant_shard(self, param):
        asset_id = param['asset_id']
        data = sign_msg(asset_id, param['account'])

        data['asset_id'] = param['asset_id']
        if 'shard_id' in param.keys():
            data['shard_id'] = param['shard_id']
        else:
            data['shard_id'] = Util.gen_nonce()

        data['to_addr'] = param['to_addr']

        if 'price' in param.keys():
            data['price'] = param['price']
        if 'to_userid' in param.keys():
            data['to_userid'] = param['to_userid']

        resp = self._conn.sign_post(GrantAsset_URI, data)
        if 'errno' not in resp.keys():
            print("panic, resp: %s" % resp)
            return None
        if resp['errno'] != 0:
            print("error, resp: %s" % resp)
            return None
        print("grant succ. resp: %s" % resp)
        return resp

    def transfer_shard(self, param):
        asset_id = param['asset_id']
        data = sign_msg(asset_id, param['account'])
        
        data['asset_id'] = asset_id
        data['shard_id'] = param['shard_id']
        data['to_addr'] = param['to_addr']
        if 'price' in param.keys():
            data['price'] = param['price']
        if 'to_userid' in param.keys():
            data['to_userid'] = param['to_userid']

        resp = self._conn.sign_post(TransferShard_URI, data)
        if 'errno' not in resp.keys():
            print("panic, resp: %s" % resp)
            return None
        if resp['errno'] != 0:
            print("error, resp: %s" % resp)
            return None
        print("transfer succ. resp: %s" % resp)
        return 0

    def consume_shard(self, param):
        asset_id = param['asset_id']
        nonce = param['nonce']
        create_account_json = param['create_account']
        create_addr = create_account_json['addr']
        create_sk = create_account_json['sk']
        create_account = XassetAccount(create_addr, create_sk)
        signMsg = '%d%d' % (asset_id, nonce)
        create_sign = create_account.sign_ecdsa(signMsg)
        data = {
            'asset_id': asset_id,
            'shard_id': param['shard_id'],
            'nonce': nonce,
            'addr': create_addr,
            'pkey': create_account.public_key(),
            'sign': create_sign,
            'user_addr': param['user_addr'],
            'user_sign': param['user_sign'],
            'user_pkey': param['user_pkey'],
        }
        
        resp = self._conn.sign_post(ConsumeShard_URI, data)
        if 'errno' not in resp.keys():
            print("panic, resp: %s" % resp)
            return None
        if resp['errno'] != 0:
            print("error, resp: %s" % resp)
            return None
        print("consume shard succ. resp: %s" % resp)
        return 0

    def __init__(self, ui, app_id, ak, sk):
        self._conn = Conn(ui, app_id, ak, sk)

