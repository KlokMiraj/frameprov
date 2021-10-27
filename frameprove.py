
import os
from io import StringIO
import requests
import json
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


class ApiClient:
    Bearer_AUTH=''

    def __init__(self, api_key: str):
        self.api_key = api_key  # <-- dependency is injected
        self.Bearer_AUTH=api_key
         

        

    def bearer_oauth(r):
        """
        Method required by bearer token authentication.
        """
        
        r.headers["Authorization"] = f"Bearer {'AAAAAAAAAAAAAAAAAAAAAKcMVAEAAAAA%2FFQ2qeKEwPbvKfYoua1uZOK7uHE%3DRbsN3dbegtXsr4m5goHCUOKs8QcR9SjG2S9dTlp8bnaAPsnaCR'}"
        r.headers["User-Agent"] = "v2FullArchiveSearchPython"
        return r

    def connect_to_endpoint(self,url:str, params:str):
            
            response = requests.request("GET", search_url, auth=self.bearer_oauth, params=params)
    
            if response.status_code != 200:
                raise Exception(response.status_code, response.text)

            response=response.json()
            df = pd.DataFrame(response['data'])
            df=df.dropna()
            return df


class Service:
 
    def __init__(self, api_client: ApiClient,data_from_api:ApiClient):
        self.api_client = api_client  # <-- dependency is injected
        self.logic(data_from_api)
        
    def logic(self,data_from_api):

        df=data_from_api
        filtered_df=df.drop(['id'],axis=1)
        df_tweet=df['text']
        
        df_clean_tweets=self.wrangle_data(df_tweet)
        
        print('Number of Tweet removed:')
        print(len(df_tweet)-len(df_clean_tweets))

        analyzer=SentimentIntensityAnalyzer()
        

        map_object=map(lambda df_tweet:analyzer.polarity_scores(df_tweet)["compound"] > 0,df_clean_tweets)


        print('out of :')
        print(str(len(df_clean_tweets))) 
        print('positive_people:')
        print(sum(list(map_object)))

    def wrangle_data(self,DataToClean):
        
        DataToClean=DataToClean.dropna()
        DataToClean.drop_duplicates(inplace=True)
        DataToClean=DataToClean.str.replace('  ','')
        return DataToClean

def main(service: Service):  # <-- dependency is injected  
  ...  

if __name__ == '__main__':

        API_KEY="AAAAAAAAAAAAAAAAAAAAAKcMVAEAAAAA%2FFQ2qeKEwPbvKfYoua1uZOK7uHE%3DRbsN3dbegtXsr4m5goHCUOKs8QcR9SjG2S9dTlp8bnaAPsnaCR"
        search_url='https://api.twitter.com/2/tweets/search/recent'
        params={'query':'lang:en' '(from:Squid Game -is:retweet ) OR #squidgames','tweet.fields': 'author_id,text,created_at','max_results':'100'}
        main(service=Service(api_client=ApiClient(API_KEY),data_from_api=(ApiClient.connect_to_endpoint(ApiClient,search_url,params))))