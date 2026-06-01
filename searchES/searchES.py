import json
import time
import sys
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import csv
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text
import os

ELASTIC_HOST = os.getenv('ELASTIC_HOST','semantic-search-qa-elastic')

def connect2ES():
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
    """
    b={
            'query':{
                'bool':{
                    'should':[
                        {'match':{"frage":q}},
                        {'match':{"antwort":q}}
                    ]
                }
            }
        }
    """
    #bf = body frage
    bf={
        'query':{
            'match':{
                "frage":q
                }
            }
        }
    #res= es.search(index='questions-index',body=bf)
    #print("Keyword Search:\n")
    #for hit in res['hits']['hits']:
    #    print("Frage_id "+hit['_id'] +" (score:"+str(hit['_score'])+")" + "\t" + hit['_source']['frage'])#+ "\t" +hit['_source']['link'])
    
    #ba = body antwort
    ba={
        'query':{
            'match':{
                "antwort":q
                }
            }
        }
    res= es.search(index='questions-index',body=ba)
    for hit in res['hits']['hits']:
        print("Antwort_id "+hit['_id'] +" (score:"+str(hit['_score'])+")" + "\t" + hit['_source']['antwort'])#+ "\t" +hit['_source']['link'])

    print("*********************************************************************************")

    return


# Search by Vec Similarity
def sentenceSimilaritybyNN(embed, es, sent):
    query_vector = tf.make_ndarray(tf.make_tensor_proto(embed([sent]))).tolist()[0]
    bf = {"query" : {
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

    #check frage
    #res= es.search(index='questions-index',body=bf)

    print("Semantic Similarity Search:\n")
    #for hit in res['hits']['hits']:
    #    print("Frage_id "+hit['_id'] +" (score:"+str(hit['_score'])+")" + "\t" + hit['_source']['frage'])#+ "\t" +hit['_source']['link'])

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
    for hit in res['hits']['hits']:
        print("Antwort_id "+hit['_id'] +" (score:"+str(hit['_score'])+")" + "\t" + hit['_source']['antwort'])#+ "\t" +hit['_source']['link'])

    print("*********************************************************************************")



if __name__=="__main__":

    es = connect2ES()
    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3")

    while(1):
        query=input("Enter a Query:")

        start = time.time()
        if query=="END":
            break

        print("Query: " +query)
        keywordSearch(es, query)
        sentenceSimilaritybyNN(embed, es, query)

        end = time.time()
        print(end - start, "sec")
