from django.shortcuts import render
import base64
import json

# Create your views here.
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .cwencryption import cwencryption
from .cwdecryption import cwdecryption
class CwEncryption(APIView):
    def get(self, request):
        try:
            email = request.GET.get('email')
            print("email",email)
            password = request.GET.get('password')
            print("password",password)
            token = request.GET.get('token')
            print("token",token)
            batchid = request.GET.get('batchid')
            print("batchid",batchid)
            cw=cwencryption(token)
            data=cw.start(email,password,batchid)
            # Process 'data' and return a response
            # You can format the data as needed and return it in the API response
            
            return Response({'data': data})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
class CwDcryption(APIView):
    def get(self, request ,data):
        try:
            print(data)
            # Process 'data' and return a response
            # You can format the data as needed and return it in the API response
            
            
            
                # Encryption key (this should be kept secret)
            encryption_key = 0xA5  # You can choose any byte value as the key

        # Add padding to the URL if needed
            while len(data) % 4 != 0:
                data += "="
            # Decoding:
            decoded_data = base64.urlsafe_b64decode(data)
            # Decryption:
            decrypted_data = self.xor_decrypt(decoded_data, encryption_key)
            # Convert decrypted bytes to JSON string and then to dictionary
            decrypted_dict = json.loads(decrypted_data.decode('utf-8'))
            # print("=============================================")
            print(decrypted_dict)
            # print("=============================================")
            email_value = decrypted_dict['email']
            print(email_value)
            password_value = decrypted_dict['password']
            print(password_value)
            batchid_value = decrypted_dict['batchid']
            print(batchid_value)
            classid_value = decrypted_dict['classid']
            print(classid_value)
            lessonext_value = decrypted_dict['lessonext']
            print(lessonext_value)
            lessonurl_value = decrypted_dict['lessonurl']
            print(lessonurl_value)
            cw=cwdecryption()
            url=cw.data(email=email_value,password=password_value,batchid=batchid_value,classid=classid_value,lessonext=lessonext_value,lessonurl=lessonurl_value)
            # print(url)

            return Response(url)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


    # Function to decrypt the data using XOR
    def xor_decrypt(self,encrypted_data, key):
        decrypted_data = bytearray(len(encrypted_data))
        for i in range(len(encrypted_data)):
            decrypted_data[i] = encrypted_data[i] ^ key
        return decrypted_data