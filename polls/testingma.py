import pandas as pd

date=["2014-01-02","2014-01-03","2014-01-04","2014-01-05","2014-01-06","2014-01-07"]
arr=[[3,4,4,4,3,5],
[4,3,2,4,3,5],
[1,4,2,4,3,5]]

df = pd.DataFrame(arr, columns = date).max().tolist()
print(df.max().tolist())