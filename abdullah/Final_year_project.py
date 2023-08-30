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
stock_name = 'NVDA'
if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client['Final_Year_Project']
#     bulk = db.test.initialize_ordered_bulk_op() # yeh line hata dena
    collection = db[f'tracking_data']
    collection_real_data = db[f'stock_twits_dataset']
#     collection_real_data = bulk[f'stock_twits_data_{stock_name}']
    # first getting all records that contain only pending entry
    records = collection.find({'stock_name':stock_name,'status':'pending'})  

    # looping in the records collection and 
    api_next_list = []
    update_list_last = []
    for record in records:
        # For collecting the whole day dat this list is created 
        stock_twits_data_list = []
        data_inserted_list = []
        # extracking end_date,start_date, next_api
        end_date                   = record['end_date']
        start_date                 = record['start_date']
        next_api_tracking          = record['next_api']
        stock_name                 = record['stock_name']
        id_name                    = record['_id']
        
        # generating api link and requests is send and converted into json format to use it
        url = f'https://api.stocktwits.com/api/2/streams/symbol/{stock_name}.json?filter=top&limit=22'
        request_success = requests.get(url)   
        json_data_dict = request_success.json()
        
        # Now getting the json data
        usefull_data = (json_data_dict['messages']) # # # # important
    
#         # Taking last record to break te for loop tracking data
#         usefull__last_data = usefull_data[-1]
        
        # next_api is the next api link limit
        next_api_first = json_data_dict['cursor']['max']
        next_api_first = str(next_api_first)
        next_api_first = '&max='+next_api_first
        print(next_api_first,'It is the next api link entry')   
        
        
        last_date_complete_api_list = list(collection.find({'stock_name':stock_name,'status':'complete'}).sort('end_date'))
        
        last_twit_date_1 = (json_data_dict['messages'][-1])
        last_twit_date_1 = last_twit_date_1['created_at']
        last_twit_date_1 = re.sub(pattern = "[T-Z]+",repl = ' ',string=last_twit_date_1)
        last_twit_date_1 = last_twit_date_1.replace(last_twit_date_1[10:],'')
        last_twit_date_1 = datetime.strptime(last_twit_date_1,'%Y-%m-%d')
        print(last_twit_date_1,'IT IS THE LAST DATE OF twit in api link limit')
        
        
        # looping in json_data it is a list of dictionary
        for data in usefull_data:
            print(end_date,'it is in the database tracking')
            # Getting the twit date from  usefull_data and cleaning is done
            twit_date = data['created_at']
            twit_date = re.sub(pattern = "[T-Z]+",repl = ' ',string=twit_date)
            twit_date = twit_date.replace(twit_date[10:],'')
            twit_date = datetime.strptime(twit_date,'%Y-%m-%d')
            print(f'{twit_date} twit_date')
            
            
            # Applying if condition to scrape data twit date is equal to end_date than scrape the data
            if twit_date == end_date:
                print('it is in first if condition')
                print(end_date,'end_date')
                print(twit_date,'twit_date')
                twit = data['body']
                signal = data['entities']['sentiment']
                if signal == None:
                    signal = 'Null'
                else :
                    signal = signal['basic']
                stock_twits_data = {'stock_name':stock_name ,'Date':twit_date,'Twits': twit,'Signal': signal}
                
                
                # appending data in a list to avoid overwrite
                stock_twits_data_list.append(stock_twits_data)
            
            #printing stock_twits_data_list
            print(stock_twits_data_list)
            # Again if condition is there if twits date is less than end_date tha break the loop
            # take th
            if twit_date < end_date:
                print('it is in second if condition')
                # if stock_twits_data_list is empty than no insertion in database else insert in database
                if len(stock_twits_data_list) == 0:
                    print('list is empty')
                else:
                    collection_real_data.insert_many(stock_twits_data_list)
            
                # Updating the pending into complete 
                status_initial = { 'status': 'pending'} 
                status_update = { "$set": { 'status': 'complete','next_api':next_api_first}}
                collection.update_one(status_initial,status_update)
                break
            try:
                if end_date < last_twit_date_1:
                    break
            except:
                print('no last_twit_date in nested loop')

        try:
            if end_date > last_twit_date_1:
                print('it is in the continue condition-------------------------------------------------------------------')
                continue
        except:
            print('no last_twit_date in main for loop')

    
            
        #While loop is used to change the api links 
        
#################################################################################################################################
        if len(last_date_complete_api_list) != 0:
            print('it is in else condition last_date_complete_api_list')
            next_api_first = last_date_complete_api_list[0]['next_api']
            print(next_api_first,'Im getting this parameter from database')   
        else:
            try:
                next_api_first = api_next_list[-1]
                print(next_api_first)
                print('there is no element of complete status in database thats why we are taking api parameter from code itself ')
            except:
                print('error next_api_first1 is not define')

        while (True):
            
            update_list = [] # helps in breaking the while loop
            print('entering in while loop ----------------------------------------------------------------')
            # generating api link and requests is send and converted into json format to use it
            url =  f'https://api.stocktwits.com/api/2/streams/symbol/{stock_name}.json?filter=top&limit=22{next_api_first}'
            request_success = requests.get(url)   
            json_data_dict = request_success.json()  
            
            # Now getting the json data
            usefull_data = (json_data_dict['messages']) # # # # important
            

            for data in usefull_data:  
                print(end_date,'for checking purpose only')
                # Getting the twit date from  usefull_data and cleaning is done
                twit_date = data['created_at']
                twit_date = re.sub(pattern = "[T-Z]+",repl = ' ',string=twit_date)
                twit_date = twit_date.replace(twit_date[10:],'')
                twit_date = datetime.strptime(twit_date,'%Y-%m-%d')
                print(f'{twit_date} twit_date')
                
                # Applying if condition to scrape data twit date is equal to end_date than scrape the data
                if twit_date == end_date:
                    print('it is in if condition while loop')
                    print(end_date,'end_date')
                    twit = data['body']
                    signal = data['entities']['sentiment']
                    if signal == None:
                        signal = 'Null'
                    else :
                        signal = signal['basic']
                    stock_twits_data = {'stock_name':stock_name ,'Date':twit_date,'Twits': twit,'Signal': signal}

                    # appending data in a list to avoid overwrite
                    stock_twits_data_list.append(stock_twits_data)
                    
                    # Removing id which is coming in stock_twits_data_list for avoiding duplication
                    for id_ in stock_twits_data_list:
                        # If id is there than remove it
                        if '_id' in id_:
                            removed_value = id_.pop('_id')
                        # If not then print 'no id found'
                        else:
                            print('no id found')
                        
                    # printing the stock_twits_data_list to see the twits
                    print(stock_twits_data_list)
                
                # Again if condition is there if twits date is less than end_date tha break the loop
                if twit_date < end_date:
                    print('it is in second condition while loop')  
                    # if stock_twits_data_list is empty than no insertion in database else insert in database
                    if len(stock_twits_data_list) == 0:
                        insert_data = 'list is empty'
                    else:
                        insert_data = collection_real_data.insert_many(stock_twits_data_list)
#                         data_inserted_list.append(data_inserted)
                    # Updating the pending into complete with respect to id
                    status_initial = { 'stock_name':stock_name,'status': 'pending','_id' : id_name } 
                    status_update = { "$set": { 'status': 'complete','next_api':next_api_first}}#'next_scroll':next_scroll
                    update_status = collection.update_one(status_initial,status_update)
                    update_list.append(insert_data)
                    break

            next_api_first = json_data_dict['cursor']['max']
            next_api_first = str(next_api_first)
            next_api_first = '&max='+next_api_first
            update_list_last.append(next_api_first)
            print(f'{next_api_first} it is changing in while loop')
            if len(update_list) != 0:
                print('while loop break')
                break
        next_api_first1 = json_data_dict['cursor']['max']
        next_api_first1 = str(next_api_first1)
        next_api_first1 = '&max='+next_api_first1
        api_next_list.append(next_api_first1)
        print(api_next_list)
        print('-------------------------------------------------------------------------------------------------for loop')
        