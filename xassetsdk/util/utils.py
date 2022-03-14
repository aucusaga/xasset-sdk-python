#!/usr/bin python3
# -*- coding: utf-8 -*-
# @file       : util.py
# @create time: 2022/03/10
# @说明       : 本文件实现了工具包，生成nonce值

from os import stat
import time
import random
import numpy as np
import hashlib
import uuid

class Util(object):
    @staticmethod
    def gen_asset_id(app_id):
        return Util.gen_id_help(app_id, 0)

    @staticmethod
    def gen_random_id():
        t = time.time()
        nano_second = int(round(t * 1000 * 1000 * 1000))
        random.seed(nano_second)
        rand_num_1 = uuid.uuid1().int >> 63
        rand_num_2 = uuid.uuid1().int >> 63
        shift1 = random.randint(1, 16)
        shift2 = random.randint(1, 8)
        tmp1 = (rand_num_1 >> shift1) + (rand_num_2 >> shift2) + (nano_second >> 1)
        randId = tmp1 & 0x7FFFFFFFFFFFFFFF
        randId = np.uint64(randId).item()
        return randId

    @staticmethod
    def str_sign_to_int(content):
        content = str(content).encode('utf-8')
        md5 = hashlib.md5(content).hexdigest().lower()

        seg1 = eval('0x' + md5[0:8])
        seg2 = eval('0x' + md5[8:16])
        seg3 = eval('0x' + md5[16:24])
        seg4 = eval('0x' + md5[24:32])

        sign1 = np.uint64(seg1 + seg3)
        sign2 = seg2 + seg4
        sign3 = sign2 << 32
        sign4 = sign1.item() & np.uint64(0x00000000ffffffff).item()
        sign = sign4 | sign3
        return sign
        
    @staticmethod
    def gen_nonce():
        t = time.time()
        nano_second = int(round(t * 1000 * 1000 * 1000))
        randId1 = Util.gen_random_id()
        randId2 = Util.gen_random_id()
        content = '%d#%d#%d' % (randId1, randId2, nano_second)
        sign = Util.str_sign_to_int(content)
        nonce = sign & 0x7FFFFFFFFFFFFFFF
        return nonce

    @staticmethod
    def gen_id_help(base_id, flag):
        base_id = int(base_id)
        t = time.time()
        nano_second = int(round(t * 1000 * 1000 * 1000))
        content = '%d#%d#%d' % (base_id, flag, nano_second)
        s = Util.str_sign_to_int(content)
        r1 = Util.gen_random_id()
        r2 = Util.gen_random_id()
        lk = base_id

        id = (lk & 0x0000000000fffff)
        id += ((r2 & 0x000000000000fff0 >> 4) << 20)
        if flag == 1:
            id += (0x0000000000000001 << 32)
        
        id += ((r1 & 0x00000000000000ff) << 33)
        id += ((s & 0x000000000000ffff) << 41)
        id += ((r2 & 0x000000000000000f) << 57)
        id = np.uint64(id).item()
        return id

if __name__ == '__main__':
    # print(Util.gen_random_id())
    print(Util.gen_nonce())
    # print(Util.gen_id_help(111, 1))
    print(Util.gen_asset_id(123456))