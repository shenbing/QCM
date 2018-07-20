# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: ZentaoParser.py
@time: 2018/6/8 14:30
"""

import time
from app.common.ZentaoParser import ZentaoParser
from app import Config

newlybugdic = {}
bugstatusdic = {}

def get_zentao_bug_info():
    while True:
        global newlybugdic
        global bugstatusdic
        newlybugdic = ZentaoParser(Config.ZENTAO_LOGINURL,Config.ZENTAO_USERNAME,Config.ZENTAO_PASSWORD).getNewlyBug()
        bugstatusdic = ZentaoParser(Config.ZENTAO_LOGINURL,Config.ZENTAO_USERNAME,Config.ZENTAO_PASSWORD).getBugStatus()
        time.sleep(300)