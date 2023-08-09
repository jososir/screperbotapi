import requests
from threading import Thread

class penpencil:
    def __init__(self):
        self.batch_id = None
        self.clid = None
        self.token =None
        self.finaldata= []
        self.hs = {
                "content-type": "application/json; charset=UTF-8",
                "randomid": "b9ed6be6ae3e5d2a",
                "user-agent": 'Android',
                "Host":"api.penpencil.xyz",
                "authorization":"Bearer",
                "client-id":self.clid,
                "client-version":"19.0",
                "client-type":"MOBILE",
            }
    
    def set_parameters(self, client_id,token, batch_id):
        # print("set_parameters")
        self.clid = client_id
        self.batch_id =batch_id 
        self.token =token 
        self.hs = {
                "content-type": "application/json; charset=UTF-8",
                "randomid": "b9ed6be6ae3e5d2a",
                "user-agent": 'Android',
                "Host":"api.penpencil.xyz",
                "authorization":f"Bearer {self.token}",
                "client-id":self.clid,
                "client-version":"19.0",
                "client-type":"MOBILE",
            }
    
    def fname(self, name):
        # print("fname")
        newname = name.replace("'","").replace("/","-").replace("%","").replace('"','').replace("[","(").replace("]",")").replace("`","").replace("\n","").replace("\t","").replace(":","-").replace(":", "").replace("||", "")
        return newname

    def nextpage(self, data, url):
        # print("nextpage")
        i = 2
        while True:
            newdata = requests.get(f'{url}{i}',headers=self.hs).json()
            if len(newdata["data"]) == 0:
                break
            for new in newdata["data"]:
                data["data"].append(new)
            i+=1
        return data
    
    def batchdetail(self , batch_id ):
        # print("batchdetail")
        url= f"https://api.penpencil.xyz/v3/batches/{batch_id}/details"
        batchdata= requests.get(f"{url}", headers=self.hs).json()
        return batchdata

    def get_topics(self, batch_id, subject_id):
        # print("get_topics")
        url = f"https://api.penpencil.xyz/v1/batches/{batch_id}/subject/{subject_id}/topics?limit=50&page="
        chpdata =requests.get(f"{url}1",headers=self.hs).json()
        return chpdata

    def getvideos(self, batch_id, subject_id, topic_id):
        # print("getvideos")
        vidurl = f"https://api.penpencil.xyz/v1/batches/{batch_id}/subjects/{subject_id}/videos?contentType=videos&tag={topic_id}&limit=50&page="
        vjson = requests.get(f'{vidurl}1',headers=self.hs).json()
        vjson = self.nextpage(vjson, vidurl)
        return vjson

    def getnotes(self, batch_id, subject_id, topic_id):
        # print("getnotes")
        notes_url = f"https://api.penpencil.xyz/v1/batches/{batch_id}/subjects/{subject_id}/videos?contentType=notes&tag={topic_id}&limit=50&page="
        njson = requests.get(f'{notes_url}1',headers=self.hs).json()
        njson = self.nextpage(njson, notes_url)
        return njson
    
    def getdppnotes(self, batch_id, subject_id, topic_id):
        # print("getdppnotes")
        notes_url = f"https://api.penpencil.xyz/v1/batches/{batch_id}/subjects/{subject_id}/videos?contentType=DppNotes&tag={topic_id}&limit=50&page="
        njson = requests.get(f'{notes_url}1',headers=self.hs).json()
        dnjson = self.nextpage(njson, notes_url)
        return dnjson

    def pdfwriter(self, json, subject_name, topic_name):
        # print("pdfwriter")
        for pdf in sorted(json["data"], key=lambda x: x["startTime"]):
            try:
                nname = self.fname(pdf["homeworkIds"][0]["topic"] + " - " + pdf["date"].split("T")[0])
                try:
                    nlink = pdf["homeworkIds"][0]["attachmentIds"][0]["baseUrl"] + pdf["homeworkIds"][0]["attachmentIds"][0]["key"]
                except:
                    nlink = "Not Available"
                data = {'subjectname':subject_name,'topicname':topic_name,'name':nname,'link':nlink}
                self.finaldata.append(data)
                # data = f"({subject_name})-{topic_name} {nname}:{nlink}\n"
                # if data not in writer:
                #     writer += data
                #     print(data)
            except:
                 pass
        # self.data +=writer

    def videowriter(self, json, subject_name, topic_name):
        # print("videowriter")
        writer = ""
        vlink=''
        for video in sorted(json["data"], key=lambda x: x["startTime"]):
            try:
                vid_name = self.fname(video.get("topic") if video.get("topic") else video.get("videoDetails").get("name"))
                vname = f'{vid_name} - {video["date"].split("T")[0]}'
                if video["urlType"].lower() != "youtube":
                    vlink = str(video.get("url")) if video.get("url") else str(video.get("videoDeatils").get("videoUrl"))
                    try:
                        if len(video["videoDetails"]["types"]) == 2:
                            # vlink.replace("d1d34p8vz63oiq", "d26g5bnklkwsh4").replace("mpd", "m3u8").strip() = vlink.replace("mpd", "m3u8")
                            vlink=vlink.replace("d1d34p8vz63oiq", "d26g5bnklkwsh4").replace("mpd", "m3u8").strip()
                    except:
                        pass
                else:
                    vlink = str(video.get("url")).replace("embed/","watch?v=") if video.get("url") else str(video.get("videoDeatils").get("videoUrl")).replace("embed/","watch?v=")
                    # vlink.replace("d1d34p8vz63oiq", "d26g5bnklkwsh4").replace("mpd", "m3u8").strip()
                # data = f"({subject_name}-{topic_name}) {vname}:{vlink}\n"
                data = {'subjectname':subject_name,'topicname':topic_name,'name':vname,'link':vlink}
                self.finaldata.append(data)
                # print(data)
                # if data not in writer:
                #     writer += data
            except:
                 pass

    
    def start(self):
        # print("start")
        batch_id=self.batch_id
        batchdata =self.batchdetail(batch_id)
        # for batchdata in batchdata["data"]:
        for subjectdata in  batchdata["data"]["subjects"]:
            subid = subjectdata["_id"]
            subject_name = subjectdata["subject"]
            topics = self.get_topics(batch_id,subid)
            total_top = len(topics["data"])
            # print(f'Found {total_top} topics...')
            if str(total_top) == "0":
                continue
            for topic in topics["data"]:
                tp_name = self.fname(topic["name"])
                tp_id = topic["_id"]
                try:
                    videos = self.getvideos( batch_id, subid, tp_id)
                    self.videowriter(videos, subject_name, tp_name,)
                except:
                    pass
                try:
                    notes = self.getnotes(batch_id, subid, tp_id)
                    self.pdfwriter(notes, subject_name, tp_name,)
                except:
                    pass
                try: 
                    dppnotes = self.getdppnotes(batch_id, subid, tp_id)
                    self.pdfwriter(dppnotes, subject_name, tp_name,)
                except:
                    pass
        print('done penpencil api')
        return(self.finaldata)    # print(f'Batch Done :- {name}')


if __name__ == "__main__":
    # client_id = input("Enter client_id: ")
    # token = input("Enter token: ")
    # batch_id= input("Enter batch_id: ")
    client_id='5f5a28cac2bce000182626d6'
    token='889f06118d960e16ed6fe0848da06f91f41fa1689bd219a5167d5d8a3d367f81'
    batch_id='63ef3aa4b158550018bb3412'
    grabber = penpencil()
    grabber.set_parameters(client_id,token,batch_id)
    data=grabber.start()
    print(data)