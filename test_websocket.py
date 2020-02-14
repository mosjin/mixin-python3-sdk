# -*- coding: utf-8 -*-

"""
Test Mixin Messenger Robot Websocket methods
Base on: https://github.com/includeleec/mixin-python3-sdk,
Author: leec
env: python 3.x

Modified by mosjin.
I just changed initWebsocket stuff, caused it can NOT reconnect server,
in case connection closed by server every hour.
Website: jinLab.com
mixin: 1051676
update: 2020-02-14
"""

from mixin_ws_api import MIXIN_WS_API
from mixin_api import MIXIN_API
from config import robot_config

import json
import time
from io import BytesIO
import base64
import gzip
import random
import logging
from common_functions import  myPrint, get_admin_mixin_id
from config import mixin_asset_lists


#logging.basicConfig( filename='example.log',level=logging.DEBUG )
logging.basicConfig( level=logging.DEBUG )

try:
    import thread
except ImportError:
    import _thread as thread


def on_message(ws, message):

    inbuffer = BytesIO(message)

    f = gzip.GzipFile(mode="rb", fileobj=inbuffer)
    rdata_injson = f.read()
    rdata_obj = json.loads(rdata_injson)
    action = rdata_obj["action"]

    myPrint( action )
    if action not in ["ACKNOWLEDGE_MESSAGE_RECEIPT", "CREATE_MESSAGE", "LIST_PENDING_MESSAGES"]:
        myPrint("unknow action", action  )
        return

    if action == "ACKNOWLEDGE_MESSAGE_RECEIPT":
        myPrint( "ACKNOWLEDGE_MESSAGE_RECEIPT, return"  )
        return

    if action == "CREATE_MESSAGE":
        data = rdata_obj["data"]
        msgid = data["message_id"]
        typeindata = data["type"]
        categoryindata = data["category"]
        userId = data["user_id"]
        conversationId = data["conversation_id"]
        dataindata = data["data"]
        created_at = data["created_at"]
        updated_at = data["updated_at"]

        realData = base64.b64decode(dataindata)
        MIXIN_WS_API.replayMessage(ws, msgid)

        message_instring = json.dumps( data )
        myPrint( message_instring )

        if 'error' in rdata_obj:
            err = "".format( "error occcur: {}", rdata_obj[ 'error'] )
            myPrint( err )
            return

        if categoryindata not in ["SYSTEM_ACCOUNT_SNAPSHOT", "PLAIN_TEXT", "SYSTEM_CONVERSATION", "PLAIN_STICKER", "PLAIN_IMAGE", "PLAIN_CONTACT"]:
            info = "".format( "unknow category: {}", categoryindata )
            myPrint( info  )
            return

        if categoryindata == "PLAIN_TEXT" and typeindata == "message":
            realData = realData.lower().decode('utf-8')

            if realData in [ "hi", "?", "help" ]:
                introductionContent = 'welcome.\n[hihi] reply n times text\n[c] send a contact card\n[b] send a link button\n[p] you need to pay\n[t] transfer to you'
                MIXIN_WS_API.sendUserText(ws, conversationId, userId, introductionContent)
                return

            if 'hihi' == realData:
                introductionContent = '你好呀 '
                for i in range(3):
                    MIXIN_WS_API.sendUserText(ws, conversationId, userId, introductionContent + str(i))
                    time.sleep(1)
                return

            if 'c' == realData:
                myPrint('send a contact card')
                MIXIN_WS_API.sendUserContactCard(ws, conversationId, userId, get_admin_mixin_id() )
                return

            if 'b' == realData:
                myPrint('send a link button')
                MIXIN_WS_API.sendUserAppButton(ws, conversationId, userId, mixin_api.getRobotHrefLink( 'JinLab' ), mixin_api.getRobotDesc( 'JinLab' ) )
                return

            if 'p' == realData:
                myPrint('you need to pay')
                money = random.randint( 5, 23 ) / 100000
                toPay = "打赏作者: {}".format( money )
                MIXIN_WS_API.sendUserPayAppButton(ws, conversationId, userId, "打赏机器人", mixin_asset_lists.CNB_ASSET_ID,  money, userId )
                return

            if 't' == realData:
                # 机器人 转给 userId
                myPrint('transfer to you')
                myPrint( "userId: %s, jinId: %s" % ( userId, get_admin_mixin_id() ) )
                money = random.randint( 1, 5 ) / 100000
                mxUuid =  "mixin://users/{}".format( robot_config.client_id )
                mixin_api.transferTo( userId, mixin_asset_lists.CNB_ASSET_ID, money, mxUuid )
                txt = "{} 打赏你 {} ".format( mxUuid, money )
                MIXIN_WS_API.sendUserText( ws, conversationId, userId, txt )
                return

        elif categoryindata == "PLAIN_TEXT":
            myPrint("PLAIN_TEXT but unkonw:")


if __name__ == "__main__":
    myPrint("main")
    mixin_api = MIXIN_API(robot_config)
    mixin_ws = MIXIN_WS_API( on_message=on_message )
    mixin_ws.run()

