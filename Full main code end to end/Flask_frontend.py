# Full back end code will be execute here
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
from flask import Flask , render_template , request , redirect , url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/homepage',methods = ['GET','POST'])
def homepage():
    return render_template('stock_market_front_end_main.html')

@app.route('/stock_prediction_my_api',methods = ['GET','POST'])
def process_form():
    name = request.form['stock_name']  # getting values from html page (name of a stock) [frontend]
    print(f'Name: {name}')
    response = requests.get(f'http://127.0.0.1:2000/stock_prediction/{name}')
    data = response.json()      # converting response to json
    print(data)
    table_data = []    # creating empty list

    keys_of_data = data.keys()   # getting all the keys of dictionary
    keys_of_data = list(keys_of_data) # converting it into list
    only_fundamentals_keys = keys_of_data[0:17] # getting only the fundamentals keys name


    value_of_data = data.values()   # getting all the values of dictionary
    value_of_data = list(value_of_data)# converting it into list
    only_fundamentals_value = value_of_data[0:17] # getting only the fundamentals values name

    for key, value in zip(only_fundamentals_keys,only_fundamentals_value):
        dictionary_need_to_add = {'fundamental': key,'value': value}
        if dictionary_need_to_add['fundamental'] == 'About_Stock' or dictionary_need_to_add['fundamental'] == 'Model_Accuracy' or dictionary_need_to_add['fundamental'] =='Signal' or dictionary_need_to_add['fundamental'] =='Stock_name' or dictionary_need_to_add['fundamental'] =='Total_twits' or dictionary_need_to_add['fundamental'] ==  'bull_bear_signal':
            print('No table data')
        else:
            table_data.append(dictionary_need_to_add) 
    return render_template('output_display.html', data = data , table_data = table_data)
    # return data
if __name__ == '__main__':
    app.run(debug=True,port=9000) 




# stock_name = [stock_name_single[0]]
# print(stock_name)
# @app.route(f'/stock_prediction/{stock_name}')
# @app.route('/stock_prediction/<string:stock_name>')
# def stock_prediction_api():
#     print('hello')
#     return 'hogaya'
        






