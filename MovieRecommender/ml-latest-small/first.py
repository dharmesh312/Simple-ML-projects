import pandas as pd 
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import csv

def saveTofile(arr2,userData,ratingsData,userid):
    indexArr=userData2.index
    ans=np.argsort(arr2,axis=1)
    ans=ans[:,-1:]
    writer=csv.writer(resultFile)
    count=0
    for lst in ans:
        for elem in lst:
            if elem not in indexArr:
                # print (ratingsData.loc[[elem]])
                # lst=[int()]
                writer.writerows([[ userid,ratingsData.loc[elem]['title'] ]])    
                count=count+1
                if(count>=5):
                    return



# importing the data
movies=pd.read_csv("movies.csv",sep=",")
ratings=pd.read_csv("ratings.csv",sep=",")
resultFile=open('suggestions.csv','w')

# data preparation
part_dummies = pd.get_dummies(movies.genres.str.split('|',expand=True).stack()).sum(level=0)
movies=(pd.concat([movies, part_dummies], axis=1, join_axes=[movies.index]))
ratingsData=ratings.join(movies.set_index('movieId'), on='movieId')
ratingsData.dropna(axis=0,how='any')
# print (ratingsData.describe())
# ratingsData.groupby(['userId'])
arr=ratingsData.userId.unique()
# print (arr)



for userid in arr:
    print (userid)
    userData=ratingsData.groupby(['userId']).get_group(userid)
    userData2=userData[userData.rating>=5.0]
    if len(userData2)<5:
        userData2=userData[userData.rating>=4.5]
    if len(userData2)<5:
        userData2=userData[userData.rating>=4.0]
    if len(userData2)<5:
        userData2=userData[userData.rating>=3.5]    
    arr2=cosine_similarity(userData2.iloc[:,6:].head(len(userData2)),ratingsData.iloc[:,6:].head(len(ratingsData)) )  
    saveTofile(arr2,userData,ratingsData,userid)

# print (ratingsData.head(20))

# trainData=ratingsData.iloc[:,6:]
# training and testing of the model
# i=0
# count=0
# arr=[]


# for chunk in np.array_split(ratingsData, 100004):
#     # print (chunk)    
#     count=count+1
#     print ('chunk NO:' ,count)
#     print (chunk)
#     if(chunk['rating']>=4):
#         print ('yes')
#     else:
#         print ('No')    
#     break
    # arr.append(  cosine_similarity(chunk, trainData.head(len(trainData)))  )
# arr=pickle.dump(arr,open('arr','rb'))
