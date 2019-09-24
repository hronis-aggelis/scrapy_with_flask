from __future__ import unicode_literals

import json
import requests

from flask import Flask
from flask import jsonify
import os
import argparse
import logging
from variables import spanish_stop_words 
import pandas as pd
from pandas.core.series import Series
from whoosh import writing
from whoosh.analysis import StemmingAnalyzer
from whoosh.filedb.filestore import RamStorage
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.query import Variations

app = Flask(__name__)

@app.route('/')
def show_product_info():
    params = {
        'spider_name': 'corte_ingles_spider',
        'start_requests': False,
        'url' : 'https://www.elcorteingles.es/moda/A30716945-abrigo-de-mujer-lana-cocida-bolsillos-laterales/'
        #'url' : 'https://www.elcorteingles.es/moda/A29458856-pijama-de-mujer-rayas-de-somos-osos/'
        #'url' : 'https://www.elcorteingles.es/moda/MP_0143040_OI19275070540-cardigan-de-hombre-de-color-gris-con-cierre-de-botones/'
        #'url' : 'https://httpbin.org/status/404'
    }
    response = requests.get('http://localhost:9080/crawl.json', params)
    #check if there was an error in the flask request
    response.raise_for_status() 
    data = json.loads(response.text)
    #check if there was an error in the initial request
    try:
        data['stats']['httperror/response_ignored_count']
        data['status'] = 'failed'
        return jsonify(**data)
    except:
        #check if all fields were scraped
        counter = 0
        failed_list = []
        for i in data['items'][0]:
            if data['items'][0][i]:
                counter +=1
            else:
                failed_list.append(i)
        if counter == 10:
            #loading the taxonomy file and initialize product dictionary.
            df = pd.read_csv('google_taxonomy_spain.csv')
            product_dict = {'title': data['items'][0]['title'].split(' ')[0], 
            'description': ' '.join(data['items'][0]['description']), 
            'category_levels' : 
            data['items'][0]['category_levels'][-1:][0]} 
            
            #calling the scoring function
            exact_or_partial = 'exact'
            x,df2 = score_calc(df, product_dict, exact_or_partial)

            #retrieve best category match and id
            if x == 1:
                google_product_category = df2[df2.total_score == df2.total_score.max()].reset_index(drop = True).combined_levels[0]
                google_category_id = df2[df2.combined_levels == google_product_category].id.reset_index(drop = True)[0]
            else:
                google_product_category = 0
                google_category_id = 0
            data['items'][0]['google_product_category'] = google_product_category
            data['items'][0]['google_category_id'] = str(google_category_id)
            data['status'] = 'success'
            return jsonify(**data)
        else:
            data['status'] = 'failed/did not scrape ' + ','.join(failed_list)
            return jsonify(**data)
def index_product_info(product_dict): 
     schema = Schema(path=ID(stored=True, analyzer=StemmingAnalyzer()),  
     content=TEXT(stored=True, analyzer=StemmingAnalyzer())) 
     st = RamStorage() 
     st.create()  
     ix = st.create_index(schema)  
     writer = ix.writer() 
     for key in product_dict.keys(): 
        writer.add_document(path=key, content=product_dict[key]) 
     writer.commit(mergetype=writing.CLEAR)  
     return ix

def get_category(string): 
    points = 0 
    name = None 
    if string: 
        board = {} 
        for s in string.split(">"): 
            name = s.strip() 
            points += 1 
            board.update({'{}'.format(name):points}) 
        return board

def match(ix, category, exact_or_partial):  
    categories = category.combined_levels.replace(',', ' OR ').replace('&', ' OR ')  
    #remove stop words for partial match
    if exact_or_partial == 'partial':
        for i in spanish_stop_words: 
            categories = categories.replace(' '+i+' ',' ')
    else:
        pass
    board  = get_category(categories)       
    weights = {'description': 1, 'category_levels': 2, 'title': 3} 
    with ix.searcher() as searcher:  
        total_score = 0  
        #we will score each sub-category and then get the sum
        for query in board:               
            if exact_or_partial == 'exact':
                parsed_query = QueryParser("content", schema=ix.schema, 
                termclass=Variations).parse(query)  
            else:
                parsed_query = QueryParser("content", schema=ix.schema, 
                termclass=Variations).parse(query.replace(' ',' OR '))
            results = searcher.search(parsed_query, terms=False)  
            score = 0  
            for r in results:  
                score += r.score * weights[r['path']] 
            total_score += score                   
        return total_score

def score_calc(df, product_dict, exact_or_partial):
    ix = index_product_info(product_dict)
    df['total_score'] = df.apply(lambda x:match(ix, x, exact_or_partial), axis=1)
    if df.total_score.max() < 2:
        exact_or_partial = 'partial'
        df['total_score'] = df.apply(lambda x:match(ix, x, exact_or_partial), axis=1)
        if df.total_score.max() < 3:
            return 2,df
        else:
            return 1,df
    else:
        return 1,df