from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import Http404
from polls.scrap import getData
from polls.model import mlModel2
from polls.alltogether import Intervals

@api_view(['POST','GET'])
def calc(request):
    if request.method == 'POST':
        try:
            print("request.data")
            print(request.data)
            token=request.data['token']
            years=int(request.data['years'])
            score=int(request.data['score'])
            #consider=int(request.data['years'])
            consider=["divida/pib eua","Relacao divida/pib Brasil","dxy","brent",'gold','bovespa','vix','usd_cny','usd_cop','usd_mxn','usd_brl',"Fed interest rate decisions","Selic"]
            considerModels=["xg","en","gb","svr"]
            score="r2"
            normType=["MinMaxScaler","StandardScaler","MaxAbsScaler","RobustScaler","QuantileTransformerNormal","QuantileTransformerUniform","PowerTransformer"]
            #considerModels=["svr"]
            sevendaysPredict,sevendaysdfY,higherData,lowerData,pinterval,r2,mse,residual=Intervals(years,consider,considerModels,normType,score)
            if token=="11111":
                print("in")
                return JsonResponse({"sevendaysPredict":sevendaysPredict,sevendaysdfY:sevendaysdfY})
        except:
            return JsonResponse({"ERROR":"ERROR"})
    if request.method == 'GET':
        print("in")
        return JsonResponse({"test":"[l1_ratio,r2,mse]"})


    
