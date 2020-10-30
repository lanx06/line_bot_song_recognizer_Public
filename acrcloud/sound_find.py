
access_key_me="bff70b7593486e9cb3c33bf077d35f50"
access_secret_me="psSTZibBHkToNacyEYly1ZYB5MNx3V4mK8TOnutf"
host="identify-ap-southeast-1.acrcloud.com"
import os, sys
from acrcloud.recognizer import ACRCloudRecognizer
import json
class find_music():
    def __init__(self,setting):
        if len(setting)!=0:
            self.access_key=setting["access_key"]
            self.access_secret=setting["access_secret"]
            self.host=setting["host"]
        else:
            self.access_key=access_key_me
            self.access_secret=access_secret_me
            self.host=host
        pass
    def sound_find(self,file_path):
        file=file_path
        config = {
            #Replace "xxxxxxxx" below with your project's host, access_key and access_secret.
            'host':self.host,
            'access_key':self.access_key, 
            'access_secret':self.access_secret,
            'timeout':20 # seconds
        }

        '''This module can recognize ACRCloud by most of audio/video file. 
            Audio: mp3, wav, m4a, flac, aac, amr, ape, ogg ...
            Video: mp4, mkv, wmv, flv, ts, avi ...'''
        re = ACRCloudRecognizer(config)

        #recognize by file path, and skip 0 seconds from from the beginning of sys.argv[1].
        #print(re.recognize_by_file(file, 0))
        indata=re.recognize_by_file(file,0)
        indata=str(indata)
        indata=json.loads(indata)
        #print(type(indata))
        #you_id=indata["metadata"]["music"][0]["external_metadata"]["youtube"]["vid"]
        #print("https://www.youtube.com/watch?v="+you_id)
        if indata["status"]["msg"] == "Success":
            return indata["metadata"]["music"][0]["external_metadata"]
        else:
            return False    
        pass
if __name__ == '__main__':
    find=find_music({})
    data=find.sound_find("./Hiroyuki Sawano aLIEz.mp3")
    print(data["youtube"])