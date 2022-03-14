#!/usr/bin python3
# -*- coding: utf-8 -*-
# @file       : demo.py
# @create time: 2022/03/10
# @说明       : 本文件提供了调起ui的测试用例
#               本测试环境为python3.7.3
#               可通过执行 python setup.py install 安装xassetsdk包
#               也可通过自行打包，推荐使用虚拟环境后freeze获取依赖包版本，使用setuptools打包，注意setup.py依赖
#               install xassetsdk 成功后，执行本文件即可

from xassetsdk.client.xasset import Xasset
from xassetsdk.auth.account import XassetAccount

import time
from xassetsdk.util.utils import Util

'''
配置
'''
UI = ""
AppID = 0
AK = ""
SK = ""

'''
资产和碎片状态
'''
AssetStatusPublished = 4
ShardStatusOnChain = 0
ShardsStatusConsumed = 6

def test():
    xasset = Xasset(UI, AppID, AK, SK)

    account_a_json = {
        'addr': 'TeyyPLpp9L7QAcxHangtcHTu7HUZ6iydY',
        'sk': '{"Curvname":"P-256","X":36505150171354363400464126431978257855318414556425194490762274938603757905292,"Y":79656876957602994269528255245092635964473154458596947290316223079846501380076,"D":111497060296999106528800133634901141644446751975433315540300236500052690483486}',
    }
    account_a = XassetAccount(account_a_json['addr'], account_a_json['sk'])

    account_b_json = {
        'addr': 'SmJG3rH2ZzYQ9ojxhbRCPwFiE9y6pD1Co',
        'sk': '{"Curvname":"P-256","X":12866043091588565003171939933628544430893620588191336136713947797738961176765,"Y":82755103183873558994270855453149717093321792154549800459286614469868720031056,"D":74053182141043989390619716280199465858509830752513286817516873984288039572219}',
    }       

    # create asset
    create_param = {
        'price': 10010,
        'amount': 100,
        'asset_info': {
            'asset_cate': 1,
            'title': '我是一个小画家',
            'thumb': ["bos_v1://bucket/object/1000_500"],
            'short_desc': '我是一个小画家',
            'img_desc': ["bos_v1://bucket/object/1000_500"],
            'asset_url': ["bos_v1://bucket/object/1000_500"],
        },
        'account': {
            'addr': account_a_json['addr'],
            'sk': account_a_json['sk'],
        },
    }
    print("------- test create asset -------")
    asset_id = xasset.create_asset(create_param)
    if asset_id is None:
        return None
    
    # publish asset
    publish_param = {
        'asset_id': asset_id,
        'account': {
            'addr': account_a_json['addr'],
            'sk': account_a_json['sk'],
        },
    }
    print("------- test publish asset -------")
    errno = xasset.publish_asset(publish_param)
    if errno is None:
        return None

    # query asset
    print("------- check asset published -------")
    query_param = {
        'asset_id': asset_id,
    }
    meta = xasset.query_asset(query_param)

    if meta is None:
        return None
    while meta['status'] != AssetStatusPublished:
        time.sleep(30)
        meta = xasset.query_asset(query_param)

    # grant shard
    grant_param = {
        'asset_id': asset_id,
        'price': 10020,
        'shard_id': Util.gen_nonce(),
        'to_addr': 'SmJG3rH2ZzYQ9ojxhbRCPwFiE9y6pD1Co',
        'account': {
            'addr': account_a_json['addr'],
            'sk': account_a_json['sk'],
        },
    }
    print("------- grant asset -------")
    resp = xasset.grant_shard(grant_param)
    if resp is None:
        return None
    shard_id = resp['shard_id']

    # query shard
    print("------- check shard on chain -------")
    querysrd_param = {
        'asset_id': asset_id,
        'shard_id': shard_id,
    }
    shard_info = xasset.query_shard(querysrd_param)
    if shard_info is None:
        return None
    while shard_info['status'] != ShardStatusOnChain:
        time.sleep(30)
        shard_info = xasset.query_shard(querysrd_param)
    
    # transfer shard
    transfer_param = {
        'asset_id': asset_id,
        'shard_id': shard_id,
        'to_addr': account_a_json['addr'],
        'account': {
            'addr': account_b_json['addr'],
            'sk': account_b_json['sk'], 
        },
    }
    print("------- test transfer shard -------")
    resp = xasset.transfer_shard(transfer_param)
    if resp is None:
        return None
    
    # query shard
    print("------- check shard on chain -------")
    querysrd_param = {
        'asset_id': asset_id,
        'shard_id': shard_id,
    }
    shard_info = xasset.query_shard(querysrd_param)
    if shard_info is None:
        return None
    while shard_info['status'] != ShardStatusOnChain:
        time.sleep(30)
        shard_info = xasset.query_shard(querysrd_param)
    
    # consume shard
    nonce = Util.gen_nonce()
    creator_signMsg = '%d%d' % (asset_id, nonce)
    creator_sign = account_a.sign_ecdsa(creator_signMsg)

    consume_param = {
        'asset_id': asset_id,
        'shard_id': shard_id,
        'create_account': {
            'addr': account_a_json['addr'],
            'sk': account_a_json['sk'],
        },
        'user_addr': account_a_json['addr'],
        'nonce': nonce,
        'user_sign': creator_sign,
        'user_pkey': account_a.public_key(),

    }
    print("------- test consume shard -------")
    resp = xasset.consume_shard(consume_param)
    if resp is None:
        return None
    
    # query shard
    print("------- check shard consumed -------")
    querysrd_param = {
        'asset_id': asset_id,
        'shard_id': shard_id,
    }
    shard_info = xasset.query_shard(querysrd_param)
    if shard_info is None:
        return None
    while shard_info['status'] != ShardsStatusConsumed:
        time.sleep(30)
        shard_info = xasset.query_shard(querysrd_param)
    
    # freeze asset
    freeze_param = {
        'asset_id': asset_id,
        'account': {
            'addr': account_a_json['addr'],
            'sk': account_a_json['sk'],
        },
    }
    print("------- test freeze asset -------")
    print(xasset.freeze_asset(freeze_param))

    # browser
    print("------- test browser srdscir -------")
    print(xasset.browser_srdscir(asset_id))
    print("------- test browser query asset -------")
    print(xasset.browser_query_asset(asset_id, 1, 50))

if __name__ == '__main__':
    test()