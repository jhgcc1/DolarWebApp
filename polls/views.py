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
from polls.scrap import getData
from django.core.cache import cache



@api_view(['POST'])
def getdataEndPoint(request):
    if request.method == 'POST':
        try:
            cache.clear()
            years=int(request.data['year'][0])
            consider=request.data["dataconsider"]
            df=getData(years,consider)
            cache.set('df', df)
            return JsonResponse({"Success":"true"})
        except:
            return JsonResponse({"error":"Error Crawlling the data"})

@api_view(['POST'])
def trainModel(request):
    if request.method == 'POST':
        try:
            score=request.data['score']
            considerModels=request.data["modelsel"]
            normType=request.data["preprocess"]
            df=cache.get('df')
            gm_cv,betspar,r2,mse,residual,estimator,norm,X_train,y_train=mlModel2(df,score,considerModels,normType)
            cache.set('gm_cv', gm_cv)
            cache.set('betspar', betspar)
            cache.set('r2', r2)
            cache.set('mse', mse)
            cache.set('residual', residual)
            cache.set('estimator', estimator)
            cache.set('norm', norm)
            cache.set('X_train', X_train)
            cache.set('y_train', y_train)
            return JsonResponse({"Success":"true"})
        except:
            return JsonResponse({"error":"Error trainning the model"})

@api_view(['POST'])
def Predict(request):
    if request.method == 'POST':
        try:
            years=int(request.data['year'][0])
            df=cache.get('df')
            gm_cv=cache.get('gm_cv')
            betspar=cache.get('betspar')
            r2=cache.get('r2')
            mse=cache.get('mse')
            residual=cache.get('residual')
            estimator=cache.get('estimator')
            norm=cache.get('norm')
            X_train=cache.get('X_train')
            y_train=cache.get('y_train')
            result=Intervals(df, gm_cv,betspar,r2,mse,residual,estimator,norm,X_train,y_train,years)
            return JsonResponse(result)
        except:
            return JsonResponse({"error":"Error predicting the model"})
        





    
