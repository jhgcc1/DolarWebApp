
from polls.scrap import getData
from polls.model import mlModel2
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from polls.preprocessClass import PreProcess
import xgboost as xgb
from polls.datas import get_dates

def Intervals(df,gm_cv,betspar,r2,mse,residual,estimator,norm,X_train, y_train,NumberOfyears):

    initialDate, finalDate,dateRange = get_dates(NumberOfyears,"-")
    
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


        #plt.plot(x,higherData, color='grey', alpha=0.2, zorder=1)
        #plt.plot(x, lowerData, color='grey', alpha=0.2, zorder=1)
        #plt.plot(x,mid, color='red', zorder=5)
        #plt.scatter(x,sevendaysdfY, marker='o', color='orange', zorder=4)
    elif type(clf__estimator)==type(xgb.XGBRegressor()):
        print("innnn")
        # "XGB P" prediction
    else:
    
        for m in estimator.estimators_:
            #print(m.coef_)
            #print(m.intercept_)
            #print(m.predict(sevendaysdfNorm))
            #print(m)
            #print(m.get_params())
            pinterval.append(m.predict(sevendaysdfNorm).tolist())

    # "Bagging model" prediction

    return {"dateRange":dateRange.tolist(),"sevendaysPredict":sevendaysPredict.tolist(),"sevendaysdfY":sevendaysdfY,"higherData":higherData,"lowerData":lowerData,"pinterval":pinterval,"r2":r2,"mse":mse,"residual":residual}