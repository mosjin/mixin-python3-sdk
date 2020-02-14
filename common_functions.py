# -*- coding: utf-8 -*-
'''
Author: mosjin
Website: jinLab.com
mixin: 1051676
update: 2020-02-14
'''

import inspect
from datetime import datetime, timedelta, time
import random
import traceback
import logging
import os
import json
import re

def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    if name in ( "", None ):
        raise "No name"
        return

    if log_file in ( "", None ):
        raise "No log_file"
        return

    formatter = logging.Formatter(
        fmt = '%(asctime)s.%(msecs)03d %(levelname)s File: "%(pathname)s", line %(lineno)d, in %(module)s - %(funcName)s: %(message)s',
        datefmt= '%Y-%m-%d %H:%M:%S'
    )

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

logError = setup_logger( 'log_error', "mx_error.log" )
logDialog = setup_logger( 'log_dialog', 'mx_dialog.log' )
logUserAuth = setup_logger( 'log_userAuth', 'mx_user_auth.log' )
logMixin = setup_logger( 'log_mixin', 'mx_api.log' )

# get __file __function__ __line
# https://stackoverflow.com/questions/6810999/how-to-determine-file-function-and-line-number
def getFFLine():
    callerframerecord = inspect.stack()[2]    # 0 represents this line
                                            # 1 represents line at caller

    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)

    ffl = 'File "{}", line {}, in {} '.format(  info.filename, info.lineno, info.function )
    #print(info.filename)                      # __FILE__     -> Test.py
    #print(info.function)                      # __FUNCTION__ -> Main
    #print(info.lineno)                        # __LINE__     -> 13
    return ffl

def datetimeStampString():
    return datetime.now().isoformat(timespec='microseconds')

def myPrint( value, *args, sep=' ', end='\n', file = None, flush = True, ffl = getFFLine ):
    errStr = "{} {} {}".format( datetimeStampString(), ffl(), str( value ) )
    print( errStr, *args, sep, end, file, flush )

# 打印错误, 堆栈, 并输出到错误日志
def myPrintErrorAndLog2File( value, *args, sep=' ', end='\n', file = None, flush = True, ffl = getFFLine ):
    errStr = "{} {} {}\ntraceback:{}".format(datetimeStampString(), ffl(), str(value), traceback.format_exc())
    print( errStr, *args, sep, end, file, flush )
    logError.critical( errStr )

# 从json文件中读取配置文件
def load_robot_info_by_file( fileName = "" ): # 'keystore-7000102000.json'
    fn = os.path.dirname( os.path.abspath( __file__ ) ) + "/config/{}".format( fileName )
    with open( fn, 'r', encoding= 'utf-8' ) as f:
        data = json.load( f )
        return data

#################################### 链接处理 部分 #############################
    # 将有网址的文字非网址化
    # 返回无网址化的文字
def get_no_link_text(  inputText ):
    if inputText in ("", None):
        return inputText

    if not if_link_text( inputText ):
        return inputText

    # cmd_detail = "你好mIxin://www.abc.com好"
    # 因为 mixin 机器人目前聊天框中: www.abc.com 会可点, abc.com 则不可点. 但这里替换成: wwwabccom
    # \1: mixin   \2: ://  \3: www  \4: abc \5: com
    txt = inputText.strip()
    retTxt = re.sub( "(http|https|mixin)(:\/\/)([a-zA-Z0-9]*)\.{0,1}([a-zA-Z0-9]*)\.{0,1}([a-zA-Z0-9]*)", r"\3\4\5",
                     txt, 0, flags=(re.IGNORECASE | re.MULTILINE) )
    return retTxt

# 是否为有 link 的文字
def if_link_text(  ipnutText ):
    if ipnutText is ("", None):
        return False

    return re.search( "(http|https|mixin):\/\/", ipnutText.strip(), re.IGNORECASE | re.MULTILINE | re.DOTALL )

#################################### 链接处理 部分 end #############################


#################################### 按钮/界面相关 部分 start #############################
# 获取一个 button
def get_1_input_button_str( realLink, text4Link, colorOfLink="#0084ff" ):
    # [{"label": "Mixin Website", "color": "#ABABAB", "action": "https://mixin.one"}, ...]
    btnStr = '{"label":"' + text4Link + '","action":"' + realLink + '","color":"' + colorOfLink + '"}'
    return btnStr

def get_input_button_real_link(  cmd, inputText="", para1="", para2="", para3="" ):
    str3 = "input:{} {} {} {} {}".format( cmd, inputText, para1, para2, para3 ).rstrip()
    return str3

def get_input_cmd_btn_str_with_text(  cmd, ipnutText ):
    str = "input:{} {}".format( cmd, ipnutText )
    return str


#################################### 按钮/界面相关 部分 end #############################

#
# 时间 昨天
def get_datetime_yesterday():
    yesterday = datetime.today() - timedelta( days = 1 )
    return yesterday

# 时间 明天
def get_datetime_tomorrow():
    tomorrow = datetime.today() + timedelta( days=1 )
    return tomorrow

# 今天的 00:00:00
def get_today_time_min():
    dt = datetime.combine( datetime.today(), time.min )
    return dt

# 今天的 23:59:59
def get_today_time_max():
    dt = datetime.combine( datetime.today(), time.max )
    return dt

def tostr( value ):
    if value is None:
        return  None

    v = "{}".format( value )
    return v

# mixin://users/uuid
def get_clickable_user_mixin_link( uuid ):
    return "mixin://users//{}".format( uuid )

# mixin://codes/uuid
def get_clickable_codes_mixin_link( uuid ):
    return "mixin://codes//{}".format( uuid )

# 是否为管理员: mixinId: 为uuid
def if_am_admin( mixinId ):
    return mixinId == get_admin_mixin_id()

def if_am_developer( mixinId ):
    return mixinId == get_admin_mixin_id()

# mosjin: 1051676
def get_admin_mixin_id():
    mosjin_mixin_id = 'b33b8e1a-ac41-40f4-8172-1fb5591f0895'
    return mosjin_mixin_id

# mixin://users/3ca12333-0222-3333-a44e-fec757fdde33
def get_mixin_click_link_by_uuid( uuid ):
    return "mixin://users/{}".format( uuid )

def readline_from_file( fileName ):
    lines = []
    try:
        with open( fileName, "r", encoding="utf-8", errors='ignore' ) as fo:
            lines = fo.readlines()

        return lines
    except OSError as e:
        return lines

def random_a_color():
    color = "#"
    for i in range( 0, 6 ):
        color += "{0:x}".format( random.randint( 0, 15 ) )

    return color.upper()

# get interval secs of wss send msg: current
def get_interval_secs_wss_send_msg():
    if interval_wss_send_msg:
        return interval_wss_send_msg

    return 0.6

# get short nick name: 大于30的话, 返回 ...
def get_short_nick_name( nickName, maxLength = 30, replaceStr = "..." ):
    if len( nickName ) < maxLength:
        return nickName

    reStr = "{}{}".format( nickName[ : maxLength - len( replaceStr ) - 1 ], replaceStr )
    return reStr

# websocket 发送消息间隔
interval_wss_send_msg = 0.6