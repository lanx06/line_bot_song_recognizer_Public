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


# Channel Access Token
line_bot_api = LineBotApi('zC0rCziecO5W7oWBn+i+zjfK4baDrVaWRGHCHrbQ2lvZUsPkDuevOLfw2RJ15lgum9mWZDZznXTZzNt86+woFN5WOWg1wX4XmxaH44JNvzBaSsoBwZaBkKamhJwvfv9qwASRWx+Y82vDYFzV7intkAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('e249894d19ef1c6763c99fdf6bffbf6b')

def get_yahoo():

    get_data=[]
    url = "https://movies.yahoo.com.tw/movie_thisweek.html?page=1"
    r = requests.get(url)
    r.encoding="utf-8"
    html=BeautifulSoup(r.text,"html.parser")
    #data=json.loads(r.text)

    image_url_arr=[]
    items =html.find_all("div","release_info")
    image_arr=html.find_all("div","release_foto")
    #print(items)
    x=0

    for it in items:
        image_it=image_arr[x]
        name=it.find("div","release_movie_name").a.text.strip()
        en=it.find("div","en").a.text.strip()
        time=it.find("div","release_movie_time").text.strip()
        text=it.find("div","release_text").span.text.strip()
        image=image_it.find("img")["src"]
        image_url_arr.append(image)
        image_request = requests.get(image)
        f = open("./"+str(x)+'.png','wb')
        
        f.write(image_request.content)
        f.close()
        pass

        #print(image)
        hap="期待度:"+it.find("div","leveltext").span.text.strip()
        data={
        "name":name,
        "en":en,
        "time":time,
        "image":"./"+str(x)+'.png',
        "text":text,
        "hope":hap

        }
        get_data.append(data)

        x=x+1

    url = "https://movies.yahoo.com.tw/movie_thisweek.html?page=2"
    r = requests.get(url)
    r.encoding="utf-8"
    html=BeautifulSoup(r.text,"html.parser")
    items =html.find_all("div","release_info")
    image_arr=html.find_all("div","release_foto")


    for it in items:

        image_it=image_arr[x-10]
        name=it.find("div","release_movie_name").a.text.strip()
        en=it.find("div","en").a.text.strip()
        time=it.find("div","release_movie_time").text.strip()
        text=it.find("div","release_text").span.text.strip()
        image=image_it.find("img")["src"]
        image_url_arr.append(image)
        image_request = requests.get(image)
        f = open("./"+str(x)+'.png','wb')

        f.write(image_request.content)
        f.close()
        #print(image)
        hap="期待度"+it.find("div","leveltext").span.text.strip()

        data={
        "name":name,
        "en":en,
        "time":time,
        "image":"./"+str(x)+'.png',
        "text":text,
        "hope":hap

        }
        get_data.append(data)
        x=x+1
        pass

    return get_data
# 監聽所有來自 /callback 的 Post Request


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
def save(indata):
    global last_code
    last_code=indata

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #message = TextSendMessage(text=event.message.text)
    global last_code
    input_type=event.message.type
    message_id=event.message.id
    input_text=event.message.text
    data=get_yahoo()
    output=""
    output+=message_id
    output+="\n"
    output+=input_type
    output+="\n"
    print(event.message)

    if input_text == "all" or input_text=="All":
        output=""
        for x in data:
            output+=x["name"]+"\n"
        print("ok")

    elif event.message.text=="old":
        output+="https://linex06lan.herokuapp.com/log"
        output+="\n"
        pass
    elif event.message.text=="indata":
        save=last_code.message
        output+=json.dumps(save)
        output+="\n"
        pass
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
    output+=event.message.id+"\n"
    output+=event.message.type+"\n"

    if input_type == "file" or input_type == "audio" :
        print("file")
        message_content = line_bot_api.get_message_content(message_id)
        with open("./input_file.mp3", 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)
                pass
            pass
        pass
    gg=find_music({})
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






@app.route('/log',methods=['GET'])
def show_last_code():
    return last_code




import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
