from flask import Flask , render_template , request , redirect , url_for
from flask_cors import CORS
import pymongo
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import re
import time
from datetime import date
from datetime import timedelta
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime 
import json
import requests
from pymongo.errors import BulkWriteError
from pprint import pprint
import nltk
import string
nltk.download('stopwords')
from nltk.corpus import stopwords
import emoji
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from itertools import chain
from collections import Counter
import joblib 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, roc_auc_score, accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score, f1_score, precision_recall_curve
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from joblib import dump, load
pd.set_option('display.max_colwidth', None)
app = Flask(__name__)
CORS(app)
main_result_dict = {} # All information that need to display on frontend is stored here
@app.route('/stock_prediction/<string:stock_name>',methods = ['GET','POST'] )
def stock_prediction_api(stock_name):
        main_result_dict['Stock_name'] = stock_name
        header = {'Accept' : 'application/json',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language' :  'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6',
            'Connection': 'keep-alive',
            'Sec-Fetch-Site':'same-site',
            'Sec-Fetch-Mode':'cors',
            'Sec-Fetch-Dest':'empty'}
        stock_description_list = []
        list_of_pages = ['about','fundamentals']   # making a list of pages
        for link_address in list_of_pages:
            url_frontend = f"https://stocktwits.com/symbol/{stock_name}/{link_address}"   # two words will be change in the domain name
            responce = requests.get(url_frontend,headers = header)
            htmlContent = responce.content
            soup = BeautifulSoup(htmlContent,"html.parser")
            
            if link_address == 'about':  # if it is in about page than this will execute
                stocks_full_package = soup.find_all(('div') ,{"class":"SymbolAbout_container__0u8Yw px-4 py-5 text-base flex flex-col justify-between"})
                for element in stocks_full_package:
                    stock_description = element.find(('div') , {"data-cy" : "symbol-about-description"}).text
                    # stock_description_result = {'about': stock_description}
                    main_result_dict['About_Stock'] = stock_description
            elif link_address == 'fundamentals': # if it is in fundamentals page than this will execute
                stocks_full_package = soup.find_all(('div') ,{"class":"SymbolFundamentalsTable_container__2fbMe grid pt-4 tabletSm|pt-10 w-full bg-primary-background"})
                elements = soup.find_all(class_='SymbolFundamentalsTable_value__7PL60 font-semibold text-sm')  # Taking all the same class name


                ######################## having double print statement##################################
                # current_price = f"Current Price: {elements[0].text}"
                # previous_close = f"Previous Price: {elements[1].text}"
                # open_price = f"Open: {elements[2].text}"
                # dividend_yield = f"Dividend Yield: {elements[3].text}"
                # fifty_day_moving_average = f"50-Day Moving Average: {elements[4].text}"
                # beta = f"Beta: {elements[5].text}"
                # avg_volume = f"Avg. Volume: {elements[6].text}"
                # pe_ratio = f"PE Ratio : {elements[7].text}"
                # fifty_two_week_high = f"52-Week High: {elements[8].text}"
                # fifty_two_week_low = f"52-Week Low: {elements[9].text}"
                # market_capitalization = f"Market Capitalization: {elements[10].text}"
                # eps = f"EPS: {elements[11].text}"
                # price_to_book = f"Price to Book: {elements[12].text}"
                # revenue_per_emp = f"Revenue Per Employee: {elements[13].text}"
                # enterprise_value_slash_ebitda = f"Enterprise Value/EBITDA: {elements[14].text}"
                ######################## having double print statement##################################
                
                # Here giving the elements as its indivitual values through indexing
                current_price = f"{elements[0].text}"
                previous_close = f"{elements[1].text}"
                open_price = f"{elements[2].text}"
                dividend_yield = f"{elements[3].text}"
                fifty_day_moving_average = f"{elements[4].text}"
                beta = f"{elements[5].text}"
                avg_volume = f"{elements[6].text}"
                pe_ratio = f"{elements[7].text}"
                fifty_two_week_high = f"{elements[8].text}"
                fifty_two_week_low = f"{elements[9].text}"
                market_capitalization = f"{elements[10].text}"
                eps = f"{elements[11].text}"
                price_to_book = f"{elements[12].text}"
                revenue_per_emp = f"{elements[13].text}"
                enterprise_value_slash_ebitda = f"{elements[14].text}"
        # print(stock_description)
        final_dict = {'Current Price':current_price,'Previous Close': previous_close,
                     'Open Price':open_price,'Dividend Yeild':dividend_yield,
                     '50 Day Moving Average':fifty_day_moving_average,'Beta':beta,
                     'Avg Volume':avg_volume,'PE Ratio':pe_ratio,'52 Week High':fifty_two_week_high,
                     '52 Week Low': fifty_two_week_low,'Market Capitalization':market_capitalization,
                     'EPS':eps,'Price to Book':price_to_book,'Revenue Per Employee':revenue_per_emp,
                     'Enterprise Value/EBITDA':enterprise_value_slash_ebitda}
        
        keys_of_final_dict = final_dict.keys()
        keys_of_final_dict = list(keys_of_final_dict)
        value_of_final_dict = final_dict.values()
        value_of_final_dict = list(value_of_final_dict)
        for key, value in zip(keys_of_final_dict, value_of_final_dict):
            main_result_dict[key] = value

        # main_result_dict['stocks_information'] = final_dict     # poor quality
                      # this name will come from flask frontend
        main_data = []                    #  All data will store here
        api_next_list = []


        time = 24                                     # Change according to number of days
        current_time = datetime.now()                 # It show current time
        time = current_time - timedelta(hours=time)   # it will go 24 hours back and give you a specific time and time


        #Initializing the request and converts it into json
        url = f'https://api.stocktwits.com/api/2/streams/symbol/{stock_name}.json?filter=top&limit=22'  
        request_success = requests.get(url,headers=header)   
        json_data_dict = request_success.json()


        #Taking all the usefull data from the json data
        usefull_data = (json_data_dict['messages']) 

        #picking the next api address for further scrapping
        next_api_first = json_data_dict['cursor']['max']
        next_api_first = str(next_api_first)
        next_api_first = '&max='+next_api_first



        # Retrieving the last date from twit to break the first loop
        last_twit_date_1 = (json_data_dict['messages'][-1])
        last_twit_date_1 = last_twit_date_1['created_at']
        last_twit_date_1 = re.sub(pattern = "[T-Z]+",repl = ' ',string=last_twit_date_1) # eliminating alphabets
        last_twit_date_1 = datetime.strptime(last_twit_date_1, "%Y-%m-%d  %H:%M:%S ")  # changing datatype



        #Looping in the usefull_data
        for data in usefull_data:
            # Getting the twit date from  usefull_data and cleaning is done
            twit_date = data['created_at']
            twit_date = re.sub(pattern = "[T-Z]+",repl = ' ',string=twit_date)
            twit_date = datetime.strptime(twit_date, "%Y-%m-%d  %H:%M:%S ")   
            
            if twit_date > time:
                twit = data['body']
                signal = data['entities']['sentiment']
                if signal == None:
                    signal = 'Null'
                else :
                    signal = signal['basic']
                stock_twits_data = {'stock_name':stock_name ,'Date':twit_date,'Twits': twit,'Signal': signal,'Cleaning_status':'pending','Cleaning_status_lemmatization':'pending'}
                main_data.append(stock_twits_data)
            if twit_date < time:
                if len(main_data) == 0:
                    print('No twits found')
                else:
                    print('twits are there')
                break
            try:
                if time < last_twit_date_1.strptime('%H:%M:%S'):
                    break
            except:
                pass

        #########################################################################################################################################    
        while (True):
            loop_break = []
            url =  f'https://api.stocktwits.com/api/2/streams/symbol/{stock_name}.json?filter=top&limit=22{next_api_first}'
            request_success = requests.get(url,headers=header)   
            json_data_dict = request_success.json() 
            next_api_first = json_data_dict['cursor']['max']
            next_api_first = str(next_api_first)
            next_api_first = '&max='+next_api_first
            usefull_data = (json_data_dict['messages'])
            for data in usefull_data:
                twit_date = data['created_at']
                twit_date = re.sub(pattern = "[T-Z]+",repl = ' ',string=twit_date)
                twit_date = datetime.strptime(twit_date, "%Y-%m-%d  %H:%M:%S ")   
                if twit_date > time:
                    twit = data['body']
                    signal = data['entities']['sentiment']
                    if signal == None:
                        signal = 'Null'
                    else :
                        signal = signal['basic']
                    stock_twits_data = {'stock_name':stock_name ,'Date':twit_date,'Twits': twit,'Signal':signal,'Cleaning_status':'pending','Cleaning_status_lemmatization':'pending'}
                    main_data.append(stock_twits_data)

                    
                    
            if twit_date < time:
                print('while loop break')
                break
        if not main_data:    
            print('No data is found')
        else :
            df = pd.DataFrame(main_data)
            pd.set_option('display.max_colwidth', None)


            ##Removing Links from dataframe
            print('---------------------------------Links------------------------------------')
            df['Twits'] = df['Twits'].replace(r'http\S+', '', regex=True).replace(r'www\S+', '', regex=True)


            ## Lowercase the whole twits column
            print('---------------------------------lowercase------------------------------------')
            df['Twits'] = df['Twits'].apply(lambda x: x.lower())


            ## Eliminating the pumctuation 
            print('----------------------------eliminate punctuation-------------------------------')
            df['Twits'] = df['Twits'].str.replace('[^\w\s]',' ',regex=True)


            ##Eliminating stopwords 
            def remove_stopwords(x):
                return " ".join([word for word in str(x).split() if word not in stop_words])
            stop_words = set(stopwords.words('english'))
            print('----------------------------removing stopwords-------------------------------')
            df['Twits'] = df['Twits'].apply(lambda x : remove_stopwords(x))


            ##Eliminating Emoji from dataframe
            print('----------------------------removing emojis-------------------------------')
            df['Twits'] = df['Twits'].apply(lambda s: emoji.replace_emoji(s, ''))

            # Stemming on dataframe
            print('----------------------------stemming is done-------------------------------')
            stemmer = PorterStemmer()
            df['Twits'] = df['Twits'].str.split()
            df['Twits'] = df['Twits'].apply(lambda x: [stemmer.stem(y) for y in x]) # Stem every word.
            df['Twits'] = df['Twits'].apply(lambda x: " ".join(x))

            # Removing number str from column twits
            print('----------------------------removing number is done-------------------------------')
            df['Twits'] = df['Twits'].replace('\d+', '', regex=True)

            # Removing the words which contain only 1 letter
            print('----------------------------removing 1 letter word is done-------------------------------')
            df['Twits'] = df['Twits'].str.split()
            for text in df['Twits']:
                for word in text:
                    if len(word) == 1:
                        text.remove(word)
            df['Twits'] = df['Twits'].apply(lambda x: " ".join(x))
            df_yesterday = df.drop(['stock_name','Date','Cleaning_status','Cleaning_status_lemmatization','Signal'], axis=1)
            df_yesterday = df_yesterday.drop_duplicates()
            print(df_yesterday)
            total_twits = len(df_yesterday.index)
            main_result_dict['Total_twits'] = total_twits
            df_yesterday_combine         = df_yesterday                                            # duplicating the df_yesterday
            twits_prediction_lists       = df_yesterday_combine['Twits'].tolist()                                   # Converting it into list
            twits_prediction_lists_merge = " ".join(twits_prediction_lists)                        # joining each element of a list into a single element
            dict_yesterday_twits_merge   = {'Twits':twits_prediction_lists_merge}                  # Initializing of creating dataframe  
            df_yesterday_twits_merge     = pd.DataFrame(dict_yesterday_twits_merge,index=['Index'])# making dataframe
            df_yesterday_twits_merge_unicode  = df_yesterday_twits_merge['Twits'].astype('unicode')# Converting it into unicode
            
            loaded_tfidf_vectorizer = load('tfidf_vectorizer.pkl')
            x_test_prediction_yesterday_merge = loaded_tfidf_vectorizer.transform(df_yesterday_twits_merge_unicode) 
            print("Shape of yesterday_dataset:", x_test_prediction_yesterday_merge.shape)
            loaded_model = load('linear_regression_final.joblib')
            predictions = loaded_model.predict(x_test_prediction_yesterday_merge)
            ##############################
            # print(f'The {stock_name }predicted value is {predictions}')
            if predictions > 0.5 :
                main_result_dict['Signal'] = f'''The model predicts that the stock is Bullish. Our analysis suggests a positive trend in the stock's performance. During a bullish trend, traders are inclined to buy securities with the expectation that their value will continue to appreciate. This trend often occurs during periods of economic growth, favorable corporate earnings, or positive market news.'''
                main_result_dict['bull_bear_signal'] = 'Bullish'
            else:
                main_result_dict['Signal'] = f'''The model predicts that the stock is Bearish. Our analysis suggests a neagtive trend in the stock's performance. During a bearish trend, market sentiment is negative, leading to a decline in stock prices or asset values. Bearish trends often coincide with economic downturns, poor corporate performance, or negative market developments.'''
                main_result_dict['bull_bear_signal'] = 'Bearish' 
        main_result_dict['Model_Accuracy'] = '79%'
        print(main_result_dict)
        return main_result_dict
if __name__ == '__main__':
    app.run(debug=True,port=2000) 







