
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
            get_data= insjson[key]
            output[key]=get_data
            pass
        except (KeyError,IndentationError):
            pass
    return output
def error_json_value(insjson,key):
    output={}
    
    try:
        get_data= insjson[key]
        output=get_data
        pass
    except (KeyError,IndentationError):
        return None
        
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


    def find_result(self,find_data):
        return_data={}
        for x in find_data:
            currnt_data=find_data[x]
            data={}
            #try:

            if x=="youtube":
                vid= currnt_data["vid"]

                url="https://www.youtube.com/watch?v="+vid
                data={
                    "url": url,
                    "vid":vid
                }

                pass
            elif x=="deezer":
                album= error_json_value(currnt_data,"album")
                if album!=None:
                    album_data=error_json(album,"id","name")
                    pass
                for y in album_data:
                    if y=="id":
                        data["album_id"]=album_data[y]
                        pass
                    elif y=="name":
                        data["album_name"]=album_data[y]
                        pass
                    else:
                        data[y]=album_data[y]
                        pass
                track= error_json_value(currnt_data,"track")
                if track!=None:
                    track_data=error_json(track,"id","name")
                    pass
                for y in track_data:
                    if y=="id":
                        data["song_id"]=track_data[y]
                        pass
                    elif y=="name":
                        data["song_name"]=track_data[y]
                        pass
                    else:
                        data[y]=track_data[y]
                        pass
                    
                #album_id= currnt_data["album"]["id"]  
                
                pass
            elif x=="spotify":
                album_data={}
                album= error_json_value(currnt_data,"album")
                if album!= None:
                    album_data=error_json(album,"id","name")
                    pass
                track_data={}
                track= error_json_value(currnt_data,"track")
                if track!= None:
                    track_data=error_json(track,"id","name")
                    pass
                for y in album_data:
                    if y=="id":
                        data["album_id"]=album_data[y]
                        pass
                    else:
                        data[y]=album_data[y]
                        pass
                for y in track_data:
                    if y=="id":
                        data["song_id"]=track_data[y]
                        pass
                    else:
                        data[y]=track_data[y]
                        pass
                if error_json_value(album_data,"id")!= None and error_json_value(track_data,"id"):
                    url="https://open.spotify.com/album/"+error_json_value(album_data,"id")+"?highlight=spotify:track:"+error_json_value(track_data,"id")
                    data["url"]=url    
                    pass
                
                pass
            elif x=="musicbrainz":
                pass
            else:
                pass
            pass
            return_data[x]=data
            """  
            except :
                return_data[x]=data
                print("error")
                pass

            """
        return return_data



if __name__ == '__main__':
    find=find_music({})
    data=find.sound_find("./Hiroyuki Sawano aLIEz.mp3")
    result=find.find_result(data)

    print(json.dumps(result))