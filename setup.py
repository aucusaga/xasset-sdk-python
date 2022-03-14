from setuptools import setup, find_packages

setup(
    name="xassetsdk",
    version="1.0",
    author="jintong",
    author_email="aucusaga@hotmail.com",
    description="Learn to use xasset-python-sdk",

    url="http://xuper.baidu.com/", 

    install_requires=[
        'certifi==2021.10.8',
        'charset-normalizer==2.0.12',
        'ecdsa==0.17.0',
        'idna==3.3',
        'numpy==1.21.5',
        'requests==2.27.1',
        'urllib3==1.26.8',
    ],

    python_requires='>=3.7, <3.8',

    packages=find_packages(where='.', exclude=(), include=('*',))
)