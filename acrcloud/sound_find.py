
access_key_me="bff70b7593486e9cb3c33bf077d35f50"
access_secret_me="psSTZibBHkToNacyEYly1ZYB5MNx3V4mK8TOnutf"
host="identify-ap-southeast-1.acrcloud.com"
import os, sys
from acrcloud.recognizer import ACRCloudRecognizer
import json
def error_json(insjson,*keys):
    output={}
    for key in keys :
        try:
            get_data= output[key]
            output[key]=get_data
            pass
        except (KeyError,IndentationError):
            pass
    return output
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
            'timeout':60 # seconds
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

    def error_json(self,insjson,*keys):
        output={}
        for key in keys :
            try:
                get_data= output[key]
                output[key]=get_data
                pass
            except (KeyError,IndentationError):
                pass
        return output

    def find_result(self,find_data):
        return_data={}
        for x in find_data:
            currnt_data=find_data[x]
            data={}
            try:

                if x=="youtube":
                    vid= currnt_data["vid"]

                    url="https://www.youtube.com/watch?v="+vid
                    data={
                        "url": url,
                        "vid":vid
                    }
                    return_data[x] = data

                    pass
                elif x=="deezer":
                    data={
                        "song_id":currnt_data["track"]["id"],
                        "song_name":currnt_data["track"]["name"], 
                        #"album_id":album_id

                    }
                    album= error_json(currnt_data,"album")
                    if len(album)!=0:
                        data["id"]=album["id"]
                        pass
                    #album_id= currnt_data["album"]["id"]  
                    
                    return_data[x] = data
                    pass
                elif x=="spotify":
                    album= currnt_data["album"]["id"]
                    track=currnt_data["track"]["id"]
                    song_name=currnt_data["track"]["name"]

                    url="https://open.spotify.com/album/"+album+"?highlight=spotify:track:"+track
                    data={
                        "song_name":song_name,
                        "url": url,
                        #"artists":currnt_data["artist"]
                    }
                    return_data[x] = data
                    pass
                elif x=="musicbrainz":
                    pass
                else:
                    pass
                pass
            except :
                return_data[x]=data
                print("error")
                pass
        return return_data



if __name__ == '__main__':
    find=find_music({})
    data=find.sound_find("./Hiroyuki Sawano aLIEz.mp3")
    result=find.find_result(data)

    print(json.dumps(result))