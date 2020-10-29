
access_key_me="bff70b7593486e9cb3c33bf077d35f50"
access_secret_me="psSTZibBHkToNacyEYly1ZYB5MNx3V4mK8TOnutf"


import sys
import os
import urllib
import urllib.request as urlopen
import requests
import base64
import hmac
import hashlib
import time

urllib2=urlopen

# Replace "###...###" below with your project's host, access_key and access_secret.
requrl = "http://identify-ap-southeast-1.acrcloud.com/v1/identify"
access_key = access_key_me
access_secret =access_secret_me
urllib2=urlopen
file="./"+"Hiroyuki Sawano aLIEz.mp3"
# suported file formats: mp3,wav,wma,amr,ogg, ape,acc,spx,m4a,mp4,FLAC, etc
# File size: < 1M , You'de better cut large file to small file, within 15 seconds data size is better
f = open(file, "rb")
sample_bytes = os.path.getsize(file)
content = f.read()
f.close()
print(type(content))
print("run")
http_method = "POST"
http_uri = "/v1/identify"
data_type = "audio"
signature_version = "1"
timestamp = time.time()

string_to_sign = http_method+"\n"+http_uri+"\n"+access_key+"\n"+data_type+"\n"+signature_version+"\n"+str(timestamp)

sign = base64.b64encode(hmac.new(bytes(access_secret , 'utf-8'), bytes(string_to_sign, 'utf-8'), digestmod=hashlib.sha1).digest())
test_data = {'access_key':access_key,
            'sample_bytes':sample_bytes,
            'sample':base64.b64encode(content),
            'timestamp':str(timestamp),
            'signature':sign,
            'data_type':data_type,
            "signature_version":signature_version}

test_data_urlencode = urllib.parse.urlencode(test_data)



#req = urllib2.Request(url = requrl,data =test_data_urlencode)
req=requests.get(url = requrl,data =test_data_urlencode)
res = req.text
print(res)