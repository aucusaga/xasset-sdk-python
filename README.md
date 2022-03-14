# xasset-sdk-python

## 概述

本项目提供Xasset Python语言版的开发者工具包（SDK），开发者可以基于该SDK使用Python语言接入到Xasset平台。

## 使用说明

- 1.从平台申请获得到API准入AK/SK。注意AK/SK是准入凭证，不要泄露，不要下发或配置在客户端使用。
- 2.安装xassetsdk包
- 3.导入lib，主要是 xassetsdk.client.xasset.Xasset / xassetsdk.auth.account.XassetAccount
- 4.具体使用方法请参考demo.py


### 运行环境

Python SDK运行Python3环境

请先从Python2升级至Python3

- 若python环境已为3.7.3
    - python setup.py install 通过 setuptools 安装包
    - python demo.py 执行demo文件即可

- 通过源代码安装
    - 推荐使用虚拟环境，安装 setuptools
    - 依照 setup.py 指定依赖包版本号
    - python setup.py install 安装包即可

### 使用示例

请参考demo.py的使用方法。

'''

    '''
    首先初始化Xasset对象，包括需访问的UI地址，分配的APPID/AK/SKs
    '''
    xasset = Xasset(UI, AppID, AK, SK)

    '''
    初始化一个XassetAccount
    需要导入addr和json格式的私钥
    '''
    account_a_json = {
        'addr': 'TeyyPLpp9L7QAcxHangtcHTu7HUZ6iydY',
        'sk': '{"Curvname":"P-256","X":36505150171354363400464126431978257855318414556425194490762274938603757905292,   "Y":79656876957602994269528255245092635964473154458596947290316223079846501380076,"D":111497060296999106528800133634901141644446751975433315540300236500052690483486}',
    }
    account_a = XassetAccount(account_a_json['addr'], account_a_json['sk'])


'''
