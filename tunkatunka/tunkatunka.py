import requests
import json
# import pymongo
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class TunkaAPI:
    def __init__(self):
        self.host = None
        self.userid = None
        self.token = None
        self.courseid = None
        self.finaldata = []
        self.hs = None

    def set_parameters(self, host, token,userid, courseid):
        print("ajayset_parameters")
        self.host = host
        print("host==",self.host)
        self.userid = userid
        print("useris==",self.userid)
        self.token = token
        print("token=", self.token)
        self.courseid =courseid
        print("courseid=",self.courseid)
        self.hs = {
            'authority': f'{self.host}',
            'auth-key': 'appxapi',
            'client-service': 'Appx',
            'Auth-Key': 'appxapi',
            'User-Id': self.userid,
            'authorization': self.token
        }
        

    def fetch_subjects(self):
        print("fetch_subject")
        response = requests.get(f'{self.host}/get/allsubjectfrmlivecourseclass?courseid={self.courseid}&start=-1', headers=self.hs)
        if response.status_code == 200:
            resp_data = json.loads(response.text)['data']
            for data in resp_data:
                sid = data['subjectid']
                sname = data['subject_name']
                self.fetch_topics(sid, sname)

    def fetch_topics(self, subject_id, subject_name):
        print("fetch_topic")
        response = requests.get(f'{self.host}/get/alltopicfrmlivecourseclass?courseid={self.courseid}&subjectid={subject_id}&start=-1', headers=self.hs)
        if response.status_code == 200:
            resp_data = json.loads(response.text)['data']
            for data in resp_data:
                tid = data['topicid']
                tname = data['topic_name']
                self.fetch_concepts(subject_id, subject_name, tid, tname)

    def fetch_concepts(self, subject_id, subject_name, topic_id, topic_name):
        print("fetch_concepts")
        response = requests.get(f'{self.host}/get/allconceptfrmlivecourseclass?courseid={self.courseid}&subjectid={subject_id}&topicid={topic_id}&start=-1', headers=self.hs)
        if response.status_code == 200:
            resp_data = json.loads(response.text)['data']
            if resp_data:
                for data in resp_data:
                    concept_id = data['conceptid']
                    concept_name = data['concept_name']
                    self.fetch_videos(subject_id, subject_name, topic_id, topic_name, concept_id, concept_name)
            else:
                self.fetch_videos(subject_id, subject_name, topic_id, topic_name, "", "")

    def fetch_videos(self, subject_id, subject_name, topic_id, topic_name, concept_id, concept_name):
        print("fetch_videos")
        response = requests.get(f'{self.host}/get/livecourseclassbycoursesubtopconceptapiv3?courseid={self.courseid}&subjectid={subject_id}&topicid={topic_id}&conceptid={concept_id}&start=-1', headers=self.hs).json()
        if 'data' in response:
            for data in response['data']:
                titlex = data['Title'].strip()
                urlx = data['download_link'] if data['download_link'] else (data['encrypted_links'][0]['path'] if data['encrypted_links'] else data['video_key'])
                enc = urlx.replace(":ZmVkY2JhOTg3NjU0MzIxMA==", "").strip()
                enc = b64decode(enc)
                key = '638udh3829162018'.encode('utf-8')  # Must Be 16 char for AES128
                iv = 'fedcba9876543210'.encode('utf-8')  # 16 char for AES128
                cipher = AES.new(key, AES.MODE_CBC, iv)
                plaintext = unpad(cipher.decrypt(enc), AES.block_size)
                vurl = plaintext.decode('utf-8')
                data={'subjectname':subject_name,'topicname':topic_name,'conceptname':concept_name,'name':titlex,'link':vurl}
                self.finaldata.append(data)
                # json_string = json.dumps(self.finaldata, indent=4 )
                # print(json_string)

    def start(self):
        self.fetch_subjects()
        return self.finaldata


# Usage:
if __name__ == "__main__":
    tunka_api = TunkaAPI()
    tunka_api.set_parameters(host='your_host', userid='your_userid', token='your_token', courseid='your_courseid')
    final_data = tunka_api.start()
    print(json.dumps(final_data, indent=4))
