from flask import Flask, request, abort
import requests
from bs4 import BeautifulSoup
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models  import *
import json
from acrcloud.sound_find import find_music

app = Flask(__name__)


#need
line_key="<<<you>>>"
line_key_secret="<<<you>>>"
acrcloud_key="<<<you>>>"
acrcloud_key_secret="<<<you>>>"
host="identify-ap-southeast-1.acrcloud.com"

# Channel Access Token
line_bot_api = LineBotApi(line_key)
# Channel Secret
handler = WebhookHandler(line_key_secret)



@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
last_code=""

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #message = TextSendMessage(text=event.message.text)
    global last_code
    input_type=event.message.type
    message_id=event.message.id
    input_text=event.message.text
    output=""
    output+=input_type
    output+="\n"
    print(event.message)

    if input_text == "help" or input_text=="Help":
        output+="https://github.com/lanx06/line_bot_song_recognizer_Public"
        print("ok")

    else:
        output="A"
        print("ok")
    last_code=event
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=output))
    
@handler.add(MessageEvent, message=AudioMessage)
def voice(event):
    input_type=event.message.type
    message_id=event.message.id
    output=""
    #output+=event.message.id+"\n"
    output+=event.message.type+"\n\n"

    if input_type == "file" or input_type == "audio" :
        print("file")
        message_content = line_bot_api.get_message_content(message_id)
        with open("./input_file.mp3", 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)
                pass
            pass
        pass
    setting={
        "access_key":acrcloud_key,
        "access_secret":acrcloud_key_secret
    }
    gg=find_music(setting)
    return_data =gg.sound_find("./input_file.mp3")
    if return_data !=False:
        
        print(json.dumps(return_data))
        return_data= gg.find_result(return_data)
        #plwone
        for x in return_data:
            data_plw= return_data[x]
            #data
            output+=x+":\n"
            for y in data_plw:
                #print(data_plw[y])
                output+=y+":"+str(data_plw[y])+"\n"
                pass
            pass
            output+="\n"
    else:
        output+="False"
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=output))


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
