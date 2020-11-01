# line bot sound or song recognizer
## can get youtube and spotify and deezer ....
![](https://i.imgur.com/iNRkyYY.jpg =200x)


## reference
line bot  https://blackmaple.me/line-bot-tutorial/
acrcloud  https://github.com/acrcloud/acrcloud_sdk_python
## require
line 
acrcloud
heroku
## code 
app.py
line
```python=
# Channel Access Token
line_bot_api = LineBotApi('')
# Channel Secret
handler = WebhookHandler('')
```
sound_find.py
acrcloud
```python=
access_key_me=""
access_secret_me=""
host="identify-ap-southeast-1.acrcloud.com"
```
