from API_get import df, data_json
#from main import user_ratings
#from main import hero_ID
import pandas as pd
import numpy as np

def heuristic_prediction(userId, vector_user, recommendation):
    predict = []
    for i in range(0, recommendation.shape[0]):
        num = np.array(vector_user.loc[userId]).dot(np.array(recommendation.loc[i][1:-1]))
        denom = np.linalg.norm(np.array(vector_user.loc[userId]))*np.linalg.norm(np.array(recommendation.loc[i][1:-1]))
        predict.append([recommendation.iloc[i]['id'], num/denom])
    return predict
    
def getTop3ById(prediction):
    df = data_json[data_json['id'] == prediction[0]].append(data_json[data_json['id'] == prediction[1]]).append(data_json[data_json['id'] == prediction[2]])
    return (df)

def Prediction(user_ratings, hero_ID):
    user_id = [1 for i in range(5)]
    ratings = pd.DataFrame({"id" :hero_ID, "rating" :user_ratings, "userID" : user_id})
    df_merge = pd.merge(df, ratings, on='id')
    df_merge.iloc[:,1:-2] = df_merge.apply(lambda x : x['rating']*x.iloc[1:-2], axis=1)
    df_merge = df_merge.drop(["rating", "id"], axis =1 )
    vector_user = df_merge.groupby("userID").sum()
    reco = df.copy()
    reco["pred"] = 0
    prediction = pd.DataFrame(heuristic_prediction(1, vector_user, reco)).sort_values(by=1,ascending=False).iloc[:3][0].values
    return getTop3ById(prediction)
