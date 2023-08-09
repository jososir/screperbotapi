import requests,json,random,time
import base64
from config import API_KEY

class WrongCredentialsError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)
class ForbiddenError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)
        
class cwencryption:
    
    def __init__(self,token):
        self.token =token 
        self.u=['okhttp/5.0.0-alpha.1','okhttp/5.0.0-alpha.2','okhttp/5.0.0-alpha.3','okhttp/5.0.0-alpha.4','okhttp/5.0.0-alpha.5','okhttp/5.0.0-alpha.6','okhttp/5.0.0-alpha.7','okhttp/5.0.0-alpha.8','okhttp/5.0.0-alpha.9','okhttp/5.0.0-alpha.10']
        # self.lessonext_l=[ ]
        # self.lessonname_l=[]
        # self.lessonurl_l=[]
        # self.topicname_l=[]
        # self.classid_l=[]
        # self.link=''
        # self.name=''
        self.topicname=''
        self.data=[]
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
        self.headers2['token']=token
    
    def start(self,email,password,batchid):
        # print("data")
        self.batchtopic(email,password,batchid)
        return(self.data)
        
    def batchtopic(self,email,password,batchid):
        # print("batchtopic")
        response3=requests.get(f'https://elearn.crwilladmin.com/api/v3/batch-topic/{batchid}?type=class',headers=self.headers2)
        if (response3.status_code==200):
            resp3=response3.text
            ll=len(json.loads(resp3)['data']['batch_topic'])
            for i in range (ll):
                topicid=json.loads(resp3)['data']['batch_topic'][i]['id']
                topicname=json.loads(resp3)['data']['batch_topic'][i]['topicName']
                self.reqq(email,password,topicid,topicname,batchid)
        elif (response3.status_code==401):
            token=self.gettoken(email,password)
            time.sleep(1)
            # headers2=self.headers
            self.headers2['token']=token
            self.batchtopic(email,password,batchid)  
        else:
            self.headers2['user-agent']=random.choice(self.u)
            time.sleep(0.8)
            self.batchtopic(email,password,batchid) 
               
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
        if (response1.status_code==200):
            # print('Login success...')
            resp1=response1.text
            token=json.loads(resp1)['data']['token']
            return token
            # self.headers2['token']=token
        elif (response1.status_code==400):
            raise WrongCredentialsError('wrong credentials')
            # print('wrong credentials')
            # exit()
        else:
            self.headers['user-agent']=random.choice(self.u)
            self.gettoken(email,password)

    
    def reqq(self,email,password,topicid,topicname,batchid):
        # print("password",password)
        # print("email",email)
        # print("reqq")
        response4=requests.get(f'https://elearn.crwilladmin.com/api/v3/batch-detail/{batchid}?topicId={topicid}',headers=self.headers2)
        if (response4.status_code==200):
            resp4=response4.text
            # resp4=sorted(json.loads(resp4), key=lambda x: x['data']['class_list']['classes'][0]["startDateTime"])
            kk=len(json.loads(resp4)['data']['class_list']['classes'])
            vnl=""
            # for i in range (kk):
            # for video in sorted(json.loads(resp4)["data"]["class_list"]["classes"], key=lambda x: x["startDateTime"]):
            for video in reversed(json.loads(resp4)["data"]["class_list"]["classes"]):
                try:
                    classid=video['id']
                    lessonurl=video['lessonUrl']
                    lessonext=video['lessonExt']
                    lessonname=video['lessonName']
                    # classid=json.loads(resp4)['data']['class_list']['classes'][i]['id']
                    # lessonurl=json.loads(resp4)['data']['class_list']['classes'][i]['lessonUrl']
                    # lessonext=json.loads(resp4)['data']['class_list']['classes'][i]['lessonExt']
                    # lessonname=json.loads(resp4)['data']['class_list']['classes'][i]['lessonName']
                    # self.lessonext_l.append(lessonext)
                    # self.lessonname_l.append(lessonname)
                    # self.lessonurl_l.append(lessonurl)
                    # self.topicname_l.append(topicname)
                    # self.classid_l.append(classid)
                    name=f'{topicname}-{lessonname}'
                    url_to_encrypt={'email':email ,'password':password,'batchid':batchid,'classid':classid,'lessonext':lessonext,'lessonurl':lessonurl}
                    # Convert dictionary to JSON string
                    json_data = json.dumps(url_to_encrypt)
                    # Convert JSON string to bytes
                    data_bytes = json_data.encode('utf-8')
                    # Encryption key (this should be kept secret)
                    encryption_key = 0xA5  # You can choose any byte value as the key
                    #print(len(lessonext_l)) 
                    # Encrypt the data using XOR
                    encrypted_data = self.xor_encrypt(data_bytes, encryption_key)
                    # URL-safe encoding (Base64URL)
                    # API_KEY="http://127.0.0.1:8000/"
                    encoded_data = base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
                    url = f"{API_KEY}/cw/v1/{encoded_data}"
                    # vnl =str(vnl)+f'{topicname}-{lessonname}::{url}\n'
                    self.url=url
                    data={'topicname':topicname,'name':name,'link':url}
                    self.data.append(data)
                except:
                     pass    
            # vnls=vnl.split('\n')
            # for vnldata in reversed(vnls):                     
            #     self.links=self.links+f'{vnldata}'
        elif (response4.status_code==401):
            token=self.gettoken(email,password)
            time.sleep(1)
            # headers2=self.headers
            self.headers2['token']=token
            self.reqq(email,password,topicid,topicname,batchid)
        else:
             self.headers2['user-agent']=random.choice(self.u)
             time.sleep(0.8)
             self.reqq(email,password,topicid,topicname,batchid)
    
    # Function to encrypt the data using XOR
    def xor_encrypt(self,data, key):
        encrypted_data = bytearray(len(data))
        for i in range(len(data)):
            encrypted_data[i] = data[i] ^ key
        return encrypted_data      
    
    
if __name__ == "__main__":
    # email = input("Enter email: ")
    # password = input("Enter password: ")
    # token= input("Enter token: ")
    # batchid= input("Enter batch_id: ")
    email="8948392421"
    password="Yaduvansh"
    batchid="1852"
    token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE2OTE1MzU0MTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiY0VORll6QTVNMWhJUW1kRlUwaGlVV2x5VW0xeGR6MDkiLCJmaXJzdF9uYW1lIjoiVEZsYWEySlFhMjVrTVRSQlVYWlRiRVZwWWs5QmR6MDkiLCJlbWFpbCI6ImVGcHpRVkYwYkdwU01FUkhRVFpwTWtKWVMyNU9WMHBDUlhWVVRqWXdhbFUyTkdSd1VIaFNSVWRRVVQwPSIsInBob25lIjoiUWtvNE9VOUVjVlE0VjFnelJYbElSbkptZEU5bVp6MDkiLCJyZWZlcnJhbF9jb2RlIjoiYW5aNk9XbE1aMjAyWTFrM09UQnhVM01yV1daYVp6MDkifX0.HHo1xGtYHrnUBEUmRd8PK2CwklIwgJmiH82L2ot5xJQlDKV90thS07pML5ib461W_QfmNy5TL8QRH3rplG6gdtcuhRqYY9KzIAHZC5ZhwGTdP1Io3EUBYMDxv5BhI87byRDyP8hAlFqY7w91uAyn1GgoTQImymEtvyPgiYHFRLcwNrlSbp5E8hKWrX1xocqEoIhaepgQwuEmNZ5GEa0Y3nvKq02zD7KazIpfKfAIjB-EU971OF__7gqG2Uf8DfWc0PDpri5N3EUKqnHIDlezTUbcry8qlshwLH52O_vYCV2lQm2kU1Bv3qUuhYsDufjoVeEbVyi3c4j9P0QAFWvFag"
    cw=cwencryption(token)
    data=cw.start(email,password,batchid)
    