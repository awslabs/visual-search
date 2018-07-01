'''

VISUAL SEARCH MATCHES LAMBDA FUNCTION

'''

import boto3
import redis
import logging
import json
import math
import copy
from queue import PriorityQueue


logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('VisualSearchFeatures')
r = redis.StrictRedis(  host='visual-search-2.de4w70.0001.use1.cache.amazonaws.com',
                        port=6379,
                        db=0,
                        decode_responses=True)



# scan table outside handler so feature vectors are always available to lambda function
ddb_response = table.scan()
items = ddb_response['Items'] # returns a list of objects, but features are string
logger.info('NUMBER OF ITEMS:  ' + str(len(items)))
for e in items:
    vec = e['features'].replace('[', '').replace(']', '').split(',')
    e['features'] = [float(x) for x in vec]


def lambda_handler(event, context):

    #---------------------------------------------
    #  UNPACK QUERY
    #---------------------------------------------

    if 'features' not in event:
        logger.info(event)
        return

    query = event
    query_features = query['features']
    vec = query_features.split(',')
    query_features = [float(x) for x in vec]
    query_normalized = normalize(query_features)


    #---------------------------------------------
    #  COMPUTE COSINE SIMILARITY
    #---------------------------------------------

    q = PriorityQueue(maxsize=3) # maintains top closest matches

    for item in items:
        cosine = cosine_similarity(query_normalized, item['features'])
        checkHeap(q, (cosine, item))

    top3 = []
    while not q.empty():
        top3.append(q.get())
    top3.reverse() # in place
    match_objects = [top[1] for top in top3]  # pull out dicts from top3 tuples of (cosine, match)

    query_matches = match_objects
    query_result = {}
    match_copy = copy.deepcopy(query_matches) # avoid popping features from in-memory features store
    for match in match_copy:
        match.pop('features', None)
    query_result['matches'] = match_copy

    #---------------------------------------------
    #  Validate / return response
    #---------------------------------------------

    logger.info('QUERY RESULTS:  ' + json.dumps(query_result))
    # check query results for issues
    response = {}
    matches = query_result['matches']
    if matches is None or len(matches) < 1:
        response['statusCode'] = 404
        response['body'] = "NO MATCHES"
    else:
        response['statusCode'] = 200
        response['body'] = "matches found"
        r.lpush('stack:matches', query_result)

    return response


def cosine_similarity(query, to_compare):
    # cosine is just dot product of two unit vectors since feature vectors in
    # the data store for comparison are already normalized
    return dot_product(query, to_compare)


def normalize(vec):
    magnitude = math.sqrt(sum([e**2 for e in vec]))
    return [e/magnitude for e in vec]


def dot_product(v1, v2):
    return sum([i*j for i, j in zip(v1, v2)])


def checkHeap(queue, num):
    if not queue.full():
        queue.put(num)
        return
    top = queue.get()
    if num > top:
        queue.put(num)
    else:
        queue.put(top)
    return

