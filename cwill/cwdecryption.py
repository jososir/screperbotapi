import requests,json,random,time,re,os
import base64
from base64 import b64decode
import concurrent.futures
from config import API_KEY

class WrongCredentialsError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)
class ForbiddenError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class cwdecryption:  
    def __init__(self):
        self.u=['okhttp/5.0.0-alpha.1','okhttp/5.0.0-alpha.2','okhttp/5.0.0-alpha.3','okhttp/5.0.0-alpha.4','okhttp/5.0.0-alpha.5','okhttp/5.0.0-alpha.6','okhttp/5.0.0-alpha.7','okhttp/5.0.0-alpha.8','okhttp/5.0.0-alpha.9','okhttp/5.0.0-alpha.10']
        self.headers = {
            'authority': 'elearn.crwilladmin.com',
            'accept': 'application/json',
            'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://web.careerwill.com',
            'origintype': 'web',
            'referer': 'https://web.careerwill.com/',
            'user-agent': 'okhttp/5.0.0-alpha.2',
        }
        self.headers2=self.headers
        self.batchids=[]
        # headers2['token']=token
        
    def data(self,email,password,batchid,lessonext,lessonurl,classid):
        # print("data")
        token=self.gettoken(email,password)
        time.sleep(1)
        # headers2=self.headers
        self.headers2['token']=token
        # print(self.headers2)
        idvarification=self.ChackBatchId(email,password,batchid)
        # print(idvarification)
        if idvarification:
           return self.videotype(email,password,lessonext,lessonurl,classid)
        else:
            raise ForbiddenError('Batch Validity has Expired')     
    
    def gettoken(self,email,password):
        # print("gettoken")
        data1 = {
        'email': email,
        'password': password,
        'deviceType': 'web',
        'deviceVersion': 'Chrome 113',
        'deviceModel': 'chrome',
        }
        headers1=self.headers
        response1 = requests.post('https://elearn.crwilladmin.com/api/v3/login-other', headers=headers1, data=data1)
        # print(response1.json)
        resp1=response1.text
        token=json.loads(resp1)
        # print(token)
        if (response1.status_code==200):
            # print('Login success...')
            resp1=response1.text
            token=json.loads(resp1)['data']['token']
            # print(token)
            return token
            # self.headers2['token']=token
        elif (response1.status_code==400):
            raise WrongCredentialsError('wrong credentials')
            # exit()
        else:
            self.headers['user-agent']=random.choice(self.u)
            self.gettoken(email,password)
            
    def ChackBatchId(self,email,password,batchid):
        # print("ChackBatchId")
        # print('ChackBatchId')
        response2 = requests.get('https://elearn.crwilladmin.com/api/v3/my-batch', headers=self.headers2)
        if (response2.status_code==200):
            resp2=response2.text
            l=len(json.loads(resp2)['data']['batchData'])
            for i in range(l):
                batchid_=json.loads(resp2)['data']['batchData'][i]['id']
                self.batchids.append(batchid_)
            if batchid in self.batchids:
                return True
            else:
                raise ForbiddenError('Batch Validity has Expired') 
        elif (response2.status_code==401):
                token=self.gettoken(email,password)
                time.sleep(1)
                # headers2=self.headers
                self.headers2['token']=token
                self.batchtopic(email,password,batchid)  
        else:
                self.headers2['user-agent']=random.choice(self.u)
                time.sleep(0.8)
                self.batchtopic(email,password,batchid)        
                        
    def videotype(self,email,password,lessonext,lessonurl,classid):
        # print("videotype")
        # print(email)
        # lessonext=str(lessonext.strip())
        # lessonext="youtube"
        # print(password)
        # print(lessonext)
        # print("lessonurl",lessonurl)
        # print(classid)
        # print("videotype")
        # print(type(lessonext))
        # print((lessonext=='brightcove'))
        # print((lessonext=='youtube'))
        if (lessonext=='brightcove'):
            return self.reqq1(email,password,classid,lessonurl)
        if (lessonext=='youtube'):
            # print("youtube")
            # global links
            # self.links=f'https://www.youtube-nocookie.com/embed/{lessonurl}\n'
            # print(f'{topicname}-{lessonname}::https://www.youtube-nocookie.com/embed/{lessonurl}\n')
            return f'https://www.youtube-nocookie.com/embed/{lessonurl}'


    def reqq1(self,email,password,classid,lessonurl):
        # print("reqq1")
        # token=self.gettoken(email,password)
        # time.sleep(1)
        # # headers2=self.headers
        # self.headers2['token']=token
        response5=requests.get(f'https://elearn.crwilladmin.com/api/v3/livestreamToken?base=web&module=batch&type=brightcove&vid={classid}',headers=self.headers2)
        if (response5.status_code==200):
            tokenn=json.loads(response5.text)['data']['token']
            return self.brightcove(email,password,classid,lessonurl,tokenn)
        elif (response5.status_code==401):
            token=self.gettoken(email,password)
            time.sleep(1)
            # headers2=self.headers
            self.headers2['token']=token
            self.reqq1(email,password,classid,lessonurl)
        elif (response5.status_code==403):
            raise ForbiddenError('Batch Validity has Expired')
        else:
            self.headers2['user-agent']=random.choice(self.u)
            time.sleep(0.8)
            self.reqq1(email,password,classid,lessonurl)

    def brightcove(self,email,password,classid,lessonurl,tokenn):
        # print("brightcove")
        headers3 = {
        'authority': 'edge-auth.api.brightcove.com',
        'accept': 'application/json',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhY2NpZCI6IjYyMDY0NTkxMjMwMDEiLCJleHAiOjE2ODU0NzAyMjksImlhdCI6MTY4NTM4MzgyOSwiY29uaWQiOiI2MzE5NjM3NTc0MTEyIiwibWF4aXAiOjF9.WBGjmwsbCMxxBOcyyX-ngr903-RPRiq_3CLY3ro91wQHsYyxkwui9ct8Zhy3g0OBdVqxq4LX2Q6j1OJbXt3K0hAqHEHsklEdF1QNKSbno6epAJvYPl49mRGlL1-IeUt87gxWHXOtnxQFgSGitE84mQmGfqf8B2IT1u2IQpmi4HpoyS1RlyMsECpKUwOMhhcHILFRq1pQnYzrOiS2iSN6rwzgasp5Umajn9auIQz8e72nBV8eMYFdfEskXw402uvKRS9cty2rcHiO-rckXjgl-6I7humDTHAqUUPYg_AMraPsjyT6NJpxKXqqGKltOPBQVtfAsx_POvbvkYzonHzdfg',
        'origin': 'https://web.careerwill.com',
        'referer': 'https://web.careerwill.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        }
        tokval=f'Bearer {tokenn}'
        headers3['authorization']=tokval
        datan=re.findall(r'.(ey.+)\.',tokenn)
        accountid=json.loads(b64decode(datan[0]))['accid']
        time.sleep(1)
        response6=requests.get(f'https://edge-auth.api.brightcove.com/playback/v1/accounts/{accountid}/videos/{lessonurl}',headers=headers3)
        if (response6.status_code==200):
            src=json.loads(response6.text)['sources'][-1]['src']
            m3u8=src+f'&bcov_auth={tokenn}'
            #print(f'{topicname}-{lessonname}::{m3u8}\n')
            # global links,namex
            # self.links=self.links+f'{topicname}-{lessonname}::{m3u8}\n'
            return m3u8
        elif (response6.status_code==401):
            # print('Someone logged in..token changed')
            # exit()
            self.reqq1(email,password,classid,lessonurl)
        elif (response6.status_code==403):
            raise ForbiddenError('Batch Validity has Expired')
        else:
            headers3['user-agent']=random.choice(self.u)
            time.sleep(0.8)
            self.brightcove(lessonurl,tokenn)
            
    
        
                
        
        
        
    
        
            

    