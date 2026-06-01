"""Project maintainers, 2021."""

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

# connect to ES on localhost on port 9200
es = Elasticsearch([{'host': ELASTIC_HOST, 'port': 9200}])
if es.ping():
	print('Connected to ES!')
else:
	#print('Could not connect!')
	raise ConnectionError('Could not connect!')
	#sys.exit()

print("*********************************************************************************")

# Mapping: Structure of the index
# Property/Field: frage und antwort  
b = {"mappings": {
		"properties": {
			"frage": {
				"type": "text"
			},
			"frage_vector": {
				"type": "dense_vector",
				"dims": 512
			},
			"antwort": {
				"type": "text"
			},
			"antwort_vector": {
				"type": "dense_vector",
				"dims": 512
			}
		}
	}
	}

ret = es.indices.create(index='questions-index', ignore=400, body=b) #400 caused by IndexAlreadyExistsException, 
print(json.dumps(ret,indent=4))


print("*********************************************************************************")

#load USEG3 model

embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3")



with open('./data/hansche-qa-arbeitsrecht-id.csv', encoding="utf8") as csvfile:
	readCSV = csv.reader(csvfile, delimiter=';' )
	next(readCSV, None)  # skip the headers 
	for row in readCSV:
		print(row[0], row[1], row[2])
		doc_id = row[0]
		link = row[1]
		frage = row[2]
		antwort = row[3]
		vecf = tf.make_ndarray(tf.make_tensor_proto(embed([frage]))).tolist()[0]		
		veca = tf.make_ndarray(tf.make_tensor_proto(embed([antwort]))).tolist()[0]		
		
		b = {"link":link,
			"frage":frage,
			"frage_vector":vecf,
			"antwort":antwort,
			"antwort_vector":veca
			}	
		
		res = es.index(index="questions-index", id=doc_id, body=b)
		#print(res)
		

		# keep count of # rows processed

	print("Completed indexing....")

	print("*********************************************************************************")

if os.getenv('INDEX_INTERACTIVE') == '1':
	import code
	code.interact(banner = 'press "Ctrl+D" to quit', local = locals())


