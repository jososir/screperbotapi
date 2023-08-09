import aiohttp
import asyncio
import json
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


class TunkaAPI:
    def __init__(self):
        self.host = None
        self.userid = None
        self.token = None
        self.courseid = None
        self.finaldata = {
            'message': 'Done',
            'data': {}
        }

    def set_parameters(self, host, token, userid, courseid):
        print("set_parameters")
        self.host = host
        self.userid = userid
        self.token = token
        self.courseid = courseid

    async def fetch_subjects(self, session):
        print('fetch_subjects')
        url = f'{self.host}/get/allsubjectfrmlivecourseclass?courseid={self.courseid}&start=-1'
        async with session.get(url, headers=self._get_headers()) as response:
            if response.status == 200:
                resp_data = await response.json()
                tasks = [self.fetch_topics(session, data['subjectid'], data['subject_name']) for data in resp_data['data']]
                await asyncio.gather(*tasks)

    async def fetch_topics(self, session, subject_id, subject_name):
        print("fetch_topics")
        url = f'{self.host}/get/alltopicfrmlivecourseclass?courseid={self.courseid}&subjectid={subject_id}&start=-1'
        async with session.get(url, headers=self._get_headers()) as response:
            if response.status == 200:
                resp_data = await response.json()
                tasks = [self.fetch_concepts(session, subject_id, subject_name, data['topicid'], data['topic_name']) for data in resp_data['data']]
                await asyncio.gather(*tasks)

    async def fetch_concepts(self, session, subject_id, subject_name, topic_id, topic_name):
        print("fetch_concepts")
        url = f'{self.host}/get/allconceptfrmlivecourseclass?courseid={self.courseid}&subjectid={subject_id}&topicid={topic_id}&start=-1'
        async with session.get(url, headers=self._get_headers()) as response:
            if response.status == 200:
                resp_data = await response.json()
                tasks = []
                for data in resp_data['data']:
                    concept_id = data['conceptid']
                    concept_name = data['concept_name']
                    tasks.append(self.fetch_videos(session, subject_id, subject_name, topic_id, topic_name, concept_id, concept_name))
                await asyncio.gather(*tasks)

    async def fetch_videos(self, session, subject_id, subject_name, topic_id, topic_name, concept_id, concept_name):
        print("fetch_videos")
        url = f'{self.host}/get/livecourseclassbycoursesubtopconceptapiv3?courseid={self.courseid}&subjectid={subject_id}&topicid={topic_id}&conceptid={concept_id}&start=-1'
        async with session.get(url, headers=self._get_headers()) as response:
            if response.status == 200:
                resp_data = await response.json()
                if 'data' in resp_data:
                    for data in resp_data['data']:
                        try:
                            titlex = data['Title'].strip()
                            urlx = data['download_link'] if data['download_link'] else (data['encrypted_links'][0]['path'] if data['encrypted_links'] else data['video_key'])
                            urlx = data['download_link'] if data['download_link'] else (data['encrypted_links'][0]['path'] if data['encrypted_links'] else data['video_key'])
                            print(urlx)
                            enc = urlx.replace(":ZmVkY2JhOTg3NjU0MzIxMA==", "").strip()
                            enc = b64decode(enc)
                            key = '638udh3829162018'.encode('utf-8')  # Must Be 16 char for AES128
                            iv = 'fedcba9876543210'.encode('utf-8')  # 16 char for AES128
                            cipher = AES.new(key, AES.MODE_CBC, iv)
                            plaintext = unpad(cipher.decrypt(enc), AES.block_size)
                            vurl = plaintext.decode('utf-8')
                            self.finaldata['data'][titlex] = vurl
                        except:
                                 pass

    def _get_headers(self):
        return {
            'authority': self.host,
            'auth-key': 'appxapi',
            'client-service': 'Appx',
            'Auth-Key': 'appxapi',
            'User-Id': self.userid,
            'authorization': self.token
        }

    async def fetch_all_data(self):
        async with aiohttp.ClientSession() as session:
            await self.fetch_subjects(session)

    def get_final_data(self):
        
        return self.finaldata

# Usage:
if __name__ == "__main__":
    tunka_api = TunkaAPI()
    host="https://rozgarapinew.teachx.in"
    userid="1648482"
    token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjE2NDg0ODIiLCJlbWFpbCI6ImFuc2h1bHRvbWFyNjJAZ21haWwuY29tIiwidGltZXN0YW1wIjoxNjkxMzA3NDk3fQ.GcccxikNN-YXJ3PNC7gXCCZw-gX3McTcK1NW8sb2pK0'
    course_id="90"
    tunka_api.set_parameters(host='your_host', userid='your_userid', token='your_token', course_id='your_cid')
    # Run the asynchronous event loop
    asyncio.run(tunka_api.fetch_all_data())
    final_data = tunka_api.get_final_data()
    print(json.dumps(final_data, indent=4))
