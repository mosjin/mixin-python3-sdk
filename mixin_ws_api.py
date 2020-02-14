"""
Mixin Python3 Websocket SDK
base on https://github.com/myrual/mixin_client_demo/blob/master/home_of_cnb_robot.py

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
import json
import uuid
import gzip
import time
import traceback
from io import BytesIO
import base64
import websocket    # library websocket_client: https://github.com/websocket-client/websocket-client
from config import robot_config
from mixin_api import MIXIN_API
from common_functions import  myPrint, logError, logMixin, myPrintErrorAndLog2File

try:
    import thread
except ImportError:
    import _thread as thread

class MIXIN_WS_API:
    #auth_token_me  = ""
    def __init__(self, on_message, on_open=None, on_error=None, on_close=None, on_data=None):
        MIXIN_WS_API.__on_message = on_message
        self.ws = self.initAWebSocket( on_message, on_open, on_error, on_close, on_data )

    def getAuthToken(self):
        mixin_api = MIXIN_API(robot_config)
        authToken = mixin_api.genGETJwtToken('/', "", str(uuid.uuid4()))
        return authToken

    def get_websocket( self ):
        return self.ws

    # added init a web socket function to do reconnect server logic.
    def initAWebSocket(self, on_message = None, on_open=None, on_error=None, on_close=None, on_data=None, url = "wss://blaze.mixin.one/", subprotocols = "Mixin-Blaze-1" ):

        if on_message is None:
            on_message = MIXIN_WS_API.__on_message

        if on_open is None:
            on_open = MIXIN_WS_API.__on_open

        if on_close is None:
            on_close = MIXIN_WS_API.__on_close

        if on_error is None:
            on_error = MIXIN_WS_API.__on_error

        if on_data is None:
            on_data = MIXIN_WS_API.__on_data

        #websocket.enableTrace( True )
        ws = websocket.WebSocketApp( url = url,
                                         on_message=on_message,
                                         on_error=on_error,
                                         on_close=on_close,
                                         header=["Authorization:Bearer " + self.getAuthToken().decode() ],
                                         subprotocols= [ subprotocols ],
                                         on_data=on_data
                                 )
        ws.on_open = on_open
        return ws

    """
    run websocket server forever
    """
    def run(self):
        myPrint( " run " )
        while True:
            try:
                # reconnect server logic
                self.ws = self.initAWebSocket()
                # ping/pong logic.
                self.ws.run_forever( ping_interval=30, ping_timeout=10 )
                str3 = "running, or reconnected server."
                myPrint( str3 )
                logMixin.info( str3 )
            except Exception as e:
                # refers to: https://github.com/websocket-client/websocket-client/issues/95
                excepStr = "Try reconnect to the server. exception: {}".format( e )
                myPrint( excepStr )
                logError.error( excepStr )
                pass

    """
    ========================
    WEBSOCKET DEFAULT METHOD
    ========================
    """

    """
    on_open default
    """
    @staticmethod
    def __on_open(ws):

        def run(*args):
            myPrint( "###### ws open ######" )
            Message = {"id": str(uuid.uuid1()), "action": "LIST_PENDING_MESSAGES"}
            Message_instring = json.dumps(Message)

            fgz = BytesIO()
            gzip_obj = gzip.GzipFile(mode='wb', fileobj=fgz)
            gzip_obj.write(Message_instring.encode())
            gzip_obj.close()
            # https: // github.com / websocket - client / websocket - client  # long-lived-connection
            ws.send(fgz.getvalue(), opcode=websocket.ABNF.OPCODE_BINARY)
            while True:
                time.sleep( 1 )

        thread.start_new_thread(run, ())

    """
    on_data default
    """
    @staticmethod
    def __on_data(ws, readableString, dataType, continueFlag):
        myPrint( "###### on data ######" )
        return

    """
    on_exit default
    """
    @staticmethod
    def on_exit( ws ):
        myPrint( "###### on exit ###### ws!")
        ws.close()
        thread.exit()
        return


    """
    on_close default
    """

    @staticmethod
    def __on_close(ws):
        str = "###### on close ######. \n traceback deatails: {}".format( traceback.format_exc() )
        myPrint( str )
        logError.error( str )
        # for long-lived connection. on_close(). just a print.
        # refers to: https://github.com/websocket-client/websocket-client#long-lived-connection
        return

    """
    on_error default
    """

    @staticmethod
    def __on_error(ws, error):
        strErr = " ###### on error ######: {}. \ntraceback details: {}".format( error, traceback.format_exc() )
        myPrint(  strErr )
        logError.error( strErr )
        return


    """
    =================
    REPLY USER METHOD
    =================
    """

    """
    generate a standard message base on Mixin Messenger format
    """

    @staticmethod
    def writeMessage(websocketInstance, action, params):

        message = {"id": str(uuid.uuid1()), "action": action, "params": params}
        message_instring = json.dumps(message)

        fgz = BytesIO()
        gzip_obj = gzip.GzipFile(mode='wb', fileobj=fgz)
        gzip_obj.write(message_instring.encode())
        gzip_obj.close()
        try:
            s = "value: {}, size: {}".format( fgz.getvalue(), len( fgz.getvalue() ) )
            myPrint( s )
            websocketInstance.send(fgz.getvalue(), opcode=websocket.ABNF.OPCODE_BINARY)
        except Exception as e:
            myPrintErrorAndLog2File( e )


    """
    when receive a message, must reply to server
    ACKNOWLEDGE_MESSAGE_RECEIPT ack server received message
    """
    @staticmethod
    def replayMessage(websocketInstance, msgid):
        parameter4IncomingMsg = {"message_id": msgid, "status": "READ"}
        Message = {"id": str(uuid.uuid1()), "action": "ACKNOWLEDGE_MESSAGE_RECEIPT", "params": parameter4IncomingMsg}
        Message_instring = json.dumps(Message)
        fgz = BytesIO()
        gzip_obj = gzip.GzipFile(mode='wb', fileobj=fgz)
        gzip_obj.write(Message_instring.encode())
        gzip_obj.close()
        websocketInstance.send(fgz.getvalue(), opcode=websocket.ABNF.OPCODE_BINARY)
        return

    """
    reply a button to user
    """
    @staticmethod
    def sendUserAppButton(websocketInstance, in_conversation_id, to_user_id, realLink, text4Link, colorOfLink="#0084ff"):
        btn = '[{"label":"' + text4Link + '","action":"' + realLink + '","color":"' + colorOfLink + '"}]'
        btn = base64.b64encode(btn.encode('utf-8')).decode(encoding='utf-8')
        params = {"conversation_id": in_conversation_id, "recipient_id": to_user_id, "message_id": str(uuid.uuid4()),
                   "category": "APP_BUTTON_GROUP", "data": btn, "status": "SENT" }
        return MIXIN_WS_API.writeMessage(websocketInstance, "CREATE_MESSAGE", params)

    """
    reply a contact card to user
    """

    @staticmethod
    def sendUserContactCard(websocketInstance, in_conversation_id, to_user_id, to_share_userid):

        btnJson = json.dumps({"user_id": to_share_userid})
        btnJson = base64.b64encode(btnJson.encode('utf-8')).decode('utf-8')
        params = {"conversation_id": in_conversation_id, "recipient_id": to_user_id, "message_id": str(uuid.uuid4()),
                  "category": "PLAIN_CONTACT", "data": btnJson}
        return MIXIN_WS_API.writeMessage(websocketInstance, "CREATE_MESSAGE", params)

    """
    reply a text to user
    """
    @staticmethod
    def sendUserText(websocketInstance, in_conversation_id, to_user_id, textContent):

        textContent = textContent.encode('utf-8')
        textContent = base64.b64encode(textContent).decode(encoding='utf-8')

        params = {"conversation_id": in_conversation_id, "recipient_id": to_user_id, "status": "SENT",
                  "message_id": str(uuid.uuid4()), "category": "PLAIN_TEXT",
                  "data": textContent}
        return MIXIN_WS_API.writeMessage(websocketInstance, "CREATE_MESSAGE", params)

    """
     reply a markdown text to user : mixin added markdown message category: PLAIN_POST
     """
    @staticmethod
    def sendUserMarkdownText( websocketInstance, in_conversation_id, to_user_id, textContent ):

        textContent = textContent.encode( 'utf-8' )
        textContent = base64.b64encode( textContent ).decode( encoding='utf-8' )

        params = { "conversation_id": in_conversation_id, "recipient_id": to_user_id, "status": "SENT",
                   "message_id": str( uuid.uuid4() ), "category": "PLAIN_POST",
                   "data": textContent }
        return MIXIN_WS_API.writeMessage( websocketInstance, "CREATE_MESSAGE", params )


    """
    send user a pay button
    """
    @staticmethod
    def sendUserPayAppButton(webSocketInstance, in_conversation_id, to_user_id, inAssetName, inAssetID, inPayAmount,  memoReceiver, linkColor="#0CAAF5" ):
        payLink = "https://mixin.one/pay?recipient=" + robot_config.client_id + "&asset=" + inAssetID + "&amount=" + str(
            inPayAmount) + '&trace=' + str(uuid.uuid1()) + '&memo=' + memoReceiver
        btn = '[{"label":"' + inAssetName + '","action":"' + payLink + '","color":"' + linkColor + '"}]'

        btn = base64.b64encode(btn.encode('utf-8')).decode(encoding='utf-8')

        gameEntranceParams = {"conversation_id": in_conversation_id, "recipient_id": to_user_id,
                              "message_id": str(uuid.uuid4()), "category": "APP_BUTTON_GROUP", "data": btn}

        if memoReceiver in ( "", None ):
            errStr = "Require Pay button must have memo as the receiver uuid.\nDetails: {}".format( traceback.format_exc() )
            logError.critical( errStr )
            raise Exception( errStr )

        MIXIN_WS_API.writeMessage(webSocketInstance, "CREATE_MESSAGE", gameEntranceParams)

    @staticmethod
    def sendAppCard(websocketInstance, in_conversation_id, to_user_id, asset_id, amount, icon_url, title, description, color="#0080FF", memo=""):
        payLink = "https://mixin.one/pay?recipient=" + to_user_id + "&asset=" + asset_id + "&amount=" + \
                str( amount  ) + "&trace=" + str(uuid.uuid4()) + "&memo=" + memo
        card =  '{"icon_url":"' + icon_url + '","title":"' + title + \
                '","description":"' + description + '","action":"'+ payLink + '"}'
        enCard = base64.b64encode(card.encode('utf-8')).decode(encoding='utf-8')
        params = {"conversation_id": in_conversation_id,  "message_id": str(uuid.uuid4()),
                  "category": "APP_CARD", "status": "SENT", "data": enCard}
        return MIXIN_WS_API.writeMessage(websocketInstance, "CREATE_MESSAGE", params)

    @staticmethod
    def sendAppButtonGroup(websocketInstance, in_conversation_id, to_user_id, buttons):
        buttonsStr = '[' + ','.join(str(btn) for btn in buttons) +']'
        enButtons = base64.b64encode(buttonsStr.encode('utf-8')).decode(encoding='utf-8')
        params = {"conversation_id": in_conversation_id,  "recipient_id": to_user_id,
                "message_id": str(uuid.uuid4()),
                "category": "APP_BUTTON_GROUP", "status": "SENT", "data": enButtons}
        return MIXIN_WS_API.writeMessage(websocketInstance, "CREATE_MESSAGE", params)

    @staticmethod
    def payButtonString(receiver_id, asset_id, amount, label, memo="", color="#FF8000" ):
        payLink = "https://mixin.one/pay?recipient=" + receiver_id + "&asset=" + asset_id + "&amount=" + \
                  str( amount ) + "&trace=" + str(uuid.uuid4()) + "&memo=" + memo
        button  = '{"label":"' + label + '","color":"' + color + '","action":"' + payLink + '"}'
        return button


