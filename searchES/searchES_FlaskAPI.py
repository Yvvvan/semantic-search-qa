"""Project maintainers, 2021."""

import os
import math
import json
import csv
import time
import sys
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import tensorflow as tf
import tensorflow_hub as hub
from flask import Flask
from flask_cors import CORS  # This is the magic
from langdetect import detect
from langdetect import DetectorFactory
from langdetect import detect_langs

DetectorFactory.seed = 0

ELASTIC_HOST = os.getenv('ELASTIC_HOST','semantic-search-qa-elastic')

def connect2ES():
    print('Connecting to {} ...'.format(ELASTIC_HOST) )
    # connect to ES on localhost on port 9200
    es = Elasticsearch([{'host': ELASTIC_HOST, 'port': 9200}])
    if es.ping():
            print('Connected to ES!')
    else:
            #print('Could not connect!')
            raise ConnectionError('Could not connect!')
            #sys.exit()

    print("*********************************************************************************")
    return es

def keywordSearch(es, q):
    #Search by Keywords
    b={
            'query':{
                'match':{
                    "frage":q
                }
            }
        }

    res= es.search(index='questions-index',body=b)

    return res

# Search by Vec Similarity
def sentenceSimilaritybyNN(es, sent):
    query_vector = tf.make_ndarray(tf.make_tensor_proto(embed([sent]))).tolist()[0]
    b = {"query" : {
                "script_score" : {
                    "query" : {
                        "match_all": {}
                    },
                    "script" : {
                        "source": "cosineSimilarity(params.query_vector, 'frage_vector') + 1.0",
                        "params": {"query_vector": query_vector}
                    }
                }
             }
        }


    #print(json.dumps(b,indent=4))
    res= es.search(index='questions-index',body=b)
    
    return res

def keywordSearchAnswers(es, q):
    #Search by Keywords
    ba={
        'query':{
            'match':{
                "antwort":q
                }
            }
        }
    res= es.search(index='questions-index',body=ba)

    return res

# Search by Vec Similarity
def sentenceSimilaritybyNNAnswers(es, sent):
    query_vector = tf.make_ndarray(tf.make_tensor_proto(embed([sent]))).tolist()[0]
    ba = {"query" : {
                "script_score" : {
                    "query" : {
                        "match_all": {}
                    },
                    "script" : {
                        "source": "cosineSimilarity(params.query_vector, 'antwort_vector') + 1.0",
                        "params": {"query_vector": query_vector}
                    }
                }
             }
        }

    #check antwort
    res= es.search(index='questions-index',body=ba)
    
    return res


app = Flask(__name__)
CORS(app)

es = connect2ES()
import tensorflow_text
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3")
print("model loaded")
print("loading model ....")

@app.route('/healthz')
def healthz():
    return 'ok'

def sortresult(result1, result2):
    dic = {}
    for hit in result1['hits']['hits']:
        dic[str(hit['_id'])+'f'] = hit['_score']
    for hit in result2['hits']['hits']:
        if str(hit['_id'])+'f' not in dic:
            dic[str(hit['_id'])+'a'] = hit['_score']
        else:
            dic[str(hit['_id'])+'d'] = hit['_score']+dic[str(hit['_id'])+'f']
            dic.pop(str(hit['_id'])+'f')

    return sorted(dic.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)

# score scaling
def scaling(result_list):
    x = []
    for (id,score) in result_list:
        x.append(score)
    # add ceiling and floor
    if math.ceil(max(x))-max(x) >=0.5:
        x.append(math.ceil(max(x))-0.5)
    else:
        x.append(math.ceil(max(x)))
    if min(x)-math.floor(min(x)) >=0.5:
        x.append(math.floor(min(x))+0.5)
    else:
        x.append(math.floor(min(x)))
    range_values=(0,10)
    new_score= [round( ((xx - min(x)) / (1.0*(max(x) - min(x)))) * (range_values[1] - range_values[0]) + range_values[0], 2) for xx in x]

    # return scaled result
    new_result=[]
    for index in range(len(result_list)):
        new_result.append((result_list[index][0],new_score[index]))
    return (new_result,[3,7])

@app.route('/search/<query>')
def search(query):
    q = query.replace("+", " ")

    # language detection
    supported_lang=['ar','zh-cn','zh-tw','en','fr','de','it','ja','ko','nl','pl','pt','es','th','tr','ru']
    detected_lang = []
    not_support = True

    for possible_lang in detect_langs(q):
        lan = str(possible_lang).split(':')[0]
        if lan in supported_lang:
            detected_lang.append(lan)
            not_support = False
            continue
    

    if not_support:
        ret = '{"lang":"not_support","smscore":"%s","kwscore":"%s","semantic":[],"kw":[]}'%([0,0],[0,0])
        return json.dumps(ret, ensure_ascii=False).encode('utf8')

    # semantic search
    # searching from questions
    res_f = sentenceSimilaritybyNN( es, q)
    # searching from answers
    res_a = sentenceSimilaritybyNNAnswers( es, q)
    # combine and sort
    result = sortresult(res_f, res_a)
    # scale score and get a split line of score quality
    if len(result)>0:
        (result,kmeans)  = scaling(result)
    else:
        kmeans=[0,0]
    # make the header
    lang = detected_lang[0]
    if 'de' in detected_lang:
        lang = 'de'
    ret = '{"lang":"%s","smscore":"%s","semantic":['%(lang,kmeans)

    for (id,score) in result:
        find=0
        typ = id[-1]
        id = id[:-1]
        for hit in res_f['hits']['hits']:
            if hit['_id'] == id:
                ret += ('{"type":"'+typ+'","id":'+hit['_id'] +',"score":'+str(score) + ',"body":"' + str(hit['_source']['frage']).replace("\"","'") + '","body2":"' + str(hit['_source']['antwort']).replace("\"","'")+ '","link":"' +str(hit['_source']['link'])+'"},')
                find=1
                break
        if find == 1:
            find=0
            continue
        for hit in res_a['hits']['hits']:
            if hit['_id'] == id:
                ret += ('{"type":"'+typ+'","id":'+hit['_id'] +',"score":'+str(score) + ',"body":"' + str(hit['_source']['frage']).replace("\"","'")+ '","body2":"' + str(hit['_source']['antwort']).replace("\"","'")+ '","link":"' +str(hit['_source']['link'])+'"},')
                break

    if ret[-1]==",":
        ret = ret[:-1]

    # keyword
    # if not german, stop keyword search (not supported)
    if 'de' not in detected_lang:
        ret+='],"kwscore":"[0,0]","kw":[]}'
        return json.dumps(ret, ensure_ascii=False).encode('utf8')

    res_f = keywordSearch(es, q)
    res_a = keywordSearchAnswers(es, q)
    result = sortresult(res_f, res_a)
    if len(result)>0:
        (result,kmeans)  = scaling(result)
    else:
        kmeans=[0,0]
    ret+='],"kwscore":"%s","kw":['%kmeans

    for (id,score) in result:
        find=0
        typ = id[-1]
        id = id[:-1]
        for hit in res_f['hits']['hits']:
            if hit['_id'] == id:
                ret += ('{"type":"'+typ+'","id":'+hit['_id'] +',"score":'+str(score) + ',"body":"' + str(hit['_source']['frage']).replace("\"","'") + '","body2":"' + str(hit['_source']['antwort']).replace("\"","'")+ '","link":"' +str(hit['_source']['link'])+'"},')
                find=1
                break
        if find == 1:
            find=0
            continue
        for hit in res_a['hits']['hits']:
            if hit['_id'] == id:
                ret += ('{"type":"'+typ+'","id":'+hit['_id'] +',"score":'+str(score) + ',"body":"' + str(hit['_source']['frage']).replace("\"","'")+ '","body2":"' + str(hit['_source']['antwort']).replace("\"","'")+ '","link":"' +str(hit['_source']['link'])+'"},')
                break
    
    if ret[-1]==",":
        ret = ret[:-1]
    ret+=']}'

    return json.dumps(ret, ensure_ascii=False).encode('utf8')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
