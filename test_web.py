#!/usr/bin/env python
# --*-- coding: utf-8 --*--

'''
mixin 用户认证 和 保存数据
'''

from flask import Flask, redirect, request, render_template
import requests

from config import robot_config
from mixin_api import MIXIN_API
from common_functions import myPrint, logError, logUserAuth, myPrintErrorAndLog2File, get_admin_mixin_id

mixin_api = MIXIN_API(robot_config)

# 启动 Flask
app = Flask(__name__)


@app.route('/')
def index():
    # 1. 获得用户的授权 Request Authorization Code

    #scope = 'PROFILE:READ+PHONE:READ+CONTACTS:READ+ASSETS:READ'
    scope = 'PROFILE:READ'

    get_auth_code_url = 'https://mixin.one/oauth/authorize?client_id='+ robot_config.client_id+'&scope='+ scope +'&response_type=code'
    return redirect(get_auth_code_url)


@app.route('/user')
def user():

    # 2. 取得 Authorization Token
    auth_token = get_auth_token()
    if auth_token in ( "", None ):
        strTmp = "<b>Failed</b> to do authorization, or you have already authorized. Please try again later. Thanks!"
        myPrint( strTmp )
        logUserAuth.critical( strTmp )
        return strTmp

    data = mixin_api.getMyProfile(auth_token)

    data_friends = mixin_api.getMyFriends(auth_token)

    data_asset = mixin_api.getMyAssets(auth_token)

    # 返回数据中没有 conversationId.
    if 'user_id' in data:
        print( data[ 'user_id'], data[ 'full_name' ], data[ 'identity_number'] )
        logUserAuth.info( data )
    else:
        str = "read user info failed: {}".format( data )
        myPrint( str )
        logError.critical( str )
        return "<b>Failed</b> to authorization. Try again. Later. Thanks."

    welcome = '<html>Welcome back, <b>{}</b><br><p></p></html>'.format( data['full_name'] )
    return welcome


# 取得 Authorization Token
def get_auth_token():
    get_auth_token_url = 'https://api.mixin.one/oauth/token'

    # 从 url 中取到 code
    auth_code = request.args.get('code')

    post_data = {
        "client_id": robot_config.client_id,
        "code": auth_code,
        "client_secret": robot_config.client_secret,
    }

    r = requests.post(get_auth_token_url, json=post_data)
    r_json = r.json()
    myPrint(r_json)
    logUserAuth.info( r_json )

    auth_token = ""
    if r_json is None:
        return auth_token

    if "data" in r_json and "access_token" in r_json[ 'data' ]:
            auth_token = r_json['data']['access_token']

    return auth_token

def run_server():
    myPrint("main")
    app.run( host="0.0.0.0", port=5000, debug = True )

if __name__ == '__main__':
    run_server()
