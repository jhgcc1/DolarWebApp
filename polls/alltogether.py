
from polls.scrap import getData
from polls.model import mlModel2
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from polls.preprocessClass import PreProcess
import xgboost as xgb
from polls.datas import get_dates
import pandas as pd

def Intervals(df,gm_cv,betspar,r2,mse,residual,estimator,norm,X_train, y_train,NumberOfyears):

    initialDate, finalDate,dateRange = get_dates(NumberOfyears,"isoRange")
    dateRange=dateRange[-40:].tolist()
    print(df)
    print(gm_cv)
    print(betspar)
    print(r2)
    print(mse)
    print(residual)
    print(estimator)
    print(norm)
    print(X_train)
    print(y_train)
    
    sevendaysdf=df.loc[df.index >= len(df.index)-40, df.columns!="usd_brl"]
    sevendaysdfY=df.loc[df.index >= len(df.index)-40, df.columns=="usd_brl"]
    sevendaysdfY=sevendaysdfY["usd_brl"].tolist()
    sevendaysPredict=gm_cv.predict(sevendaysdf)

    
    norm__classifier_type=betspar["norm__classifier_type"]
    clf__estimator=betspar["clf__estimator"]
    
    higherData=[]
    lowerData=[]
    sevendaysdfNorm = norm.transform(sevendaysdf)
    pinterval=[]
    x = list(range(len(sevendaysdfNorm)))
    if type(clf__estimator)==type(GradientBoostingRegressor()):
        clf__estimator__learning_rate=betspar['clf__estimator__learning_rate']
        mid=sevendaysPredict
        lower = Pipeline([('norm', PreProcess(norm__classifier_type)), ('clf', GradientBoostingRegressor(alpha=0.1,learning_rate=clf__estimator__learning_rate,loss="quantile"))])
        lower.fit(X_train, y_train)
        higher = Pipeline([('norm', PreProcess(norm__classifier_type)), ('clf', GradientBoostingRegressor(alpha=0.9,learning_rate=clf__estimator__learning_rate,loss="quantile"))])
        higher.fit(X_train, y_train)
        higherData=higher.predict(sevendaysdf).tolist()
        lowerData=lower.predict(sevendaysdf).tolist()

    elif type(clf__estimator)==type(xgb.XGBRegressor()):
        print("innnn")
        # "XGB P" prediction
    else:
        clf__estimator=clf__estimator.base_estimator
        for m in estimator.estimators_:
            pinterval.append(m.predict(sevendaysdfNorm).tolist())
        UpperLowerBoundDf=pd.DataFrame(pinterval, columns = dateRange)
        higherData = UpperLowerBoundDf.max().tolist()
        lowerData = UpperLowerBoundDf.min().tolist()
    # "Bagging model" prediction

    return {"bestpreprocess":str(norm__classifier_type),"bestestimator":str(type(clf__estimator)),"dateRange":dateRange,"sevendaysPredict":sevendaysPredict.tolist(),"sevendaysdfY":sevendaysdfY,"higherData":higherData,"lowerData":lowerData,"pinterval":pinterval,"score":r2,"mse":mse,"residual":residual}