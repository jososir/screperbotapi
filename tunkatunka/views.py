from django.shortcuts import render
import pymongo 
from config import MOGO_URI

# Create your views here.
from django.shortcuts import render

# Create your views here.
# views.py
import asyncio
from rest_framework.views import APIView
from rest_framework.response import Response
from .tunkatunka import TunkaAPI

class FetchTunkatunkaunData(APIView):
    def get(self, request):
        try:
            host = request.GET.get('host')
            print("host",host)
            userid = request.GET.get('userid')
            print("userid",userid)
            token = request.GET.get('authorization')
            print("token",token)
            courseid = request.GET.get('courseid')
            print("batchid",courseid)
            tunka_api=TunkaAPI()
            tunka_api.set_parameters(host=host, userid=userid, token=token, courseid=courseid)
            final_data = tunka_api.start()
            # TO SAVE HOST API URL IN DB
            self.inserthost(host)
            
            
            # Process 'data' and return a response
            # You can format the data as needed and return it in the API response
            
            return Response({'data':final_data})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    # function for saving host in mopgodb
    def inserthost(self, host):
        try:
            mongo = pymongo.MongoClient(MOGO_URI)
            db = mongo['GURGERBOT']
            dbcol = db["APPXHOST"]
            bot_data = {"_id":host,"app":"appx"}
            dbcol.insert_one(bot_data)
        except:
            pass