#!/usr/bin python3          
# -*- coding: utf-8 -*-
# @file       : account.py
# @create time: 2022/03/10
# @说明       : 本文件实现了xchain账户签名功能

import json
import hashlib
from ecdsa.util import sigencode_der, sigdecode_der
from ecdsa import ellipticcurve, NIST256p, SigningKey, VerifyingKey

class XassetAccount(object):
    def sha256(a, data):
        return hashlib.sha256(data)

    def double_sha256(data):
        s1 = hashlib.sha256(data).digest()
        return hashlib.sha256(s1)

    def sign_ecdsa(self, msg):
        msg = bytes(msg, "utf-8")
        sign = self._sk.sign(data=msg, hashfunc=self.sha256, sigencode=sigencode_der)
        return sign.hex()

    def public_key(self):
        return self._pk_json

    # sk_json格式目前仅支持NIST256p
    def __init__(self, addr, sk_json):
        self._addr = addr
        sk_obj = json.loads(sk_json)
        X = int(sk_obj['X'])
        Y = int(sk_obj['Y'])
        D = int(sk_obj['D'])

        pk_obj = {}
        pk_obj['X'] = sk_obj['X']
        pk_obj['Y'] = sk_obj['Y']
        pk_obj['Curvname'] = 'P-256'
        self._pk_json = json.dumps(pk_obj)
        
        self._pk = VerifyingKey.from_public_point(ellipticcurve.Point(NIST256p.curve, X, Y), NIST256p, self.double_sha256)
        self._sk = SigningKey.from_secret_exponent(D, NIST256p, self.double_sha256)

