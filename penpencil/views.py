from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import pymongo 
from config import MOGO_URI
# Create your views here.
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .penpencil import penpencil

class FetchPenPencilData(APIView):
    def get(self, request):
        try:
            client_id = request.GET.get('client_id')
            print("client_id",client_id)
            token = request.GET.get('token')
            print("token",token)
            batch_id = request.GET.get('batch_id')
            print("batch_id",batch_id)
            grabber = penpencil()
            grabber.set_parameters(client_id, token, batch_id)
            data = grabber.start()
            
            self.insertclientid(client_id)
            # Process 'data' and return a response
            # You can format the data as needed and return it in the API response
            
            return Response({'data': data})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    # to insert client id in mogodb
    def insertclientid(self, clientid):
        try:
            mongo = pymongo.MongoClient(MOGO_URI)
            db = mongo['GURGERBOT']
            dbcol = db["APPXHOST"]
            bot_data = {"_id":clientid,"app":"penpencil"}
            dbcol.insert_one(bot_data)
        except:
            pass
