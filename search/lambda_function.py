'''

VISUAL SEARCH MATCHES LOOKUP LAMBDA FUNCTION

'''

import boto3
import json
import logging
import math
import redis

#------------------------------------------
# CONSTANTS
#
# replace <your-kNN-endpoint-name>
# replace <your-redis-endpoint>
#------------------------------------------

table_name = 'VisualSearchMetadata'
endpoint_name = '<your-kNN-endpoint-name>'
redis_hostname = '<your-redis-endpoint>'

#------------------------------------------

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
r = redis.StrictRedis(  host=redis_hostname,
                        port=6379,
                        db=0,
                        decode_responses=True)

runtime = boto3.client('runtime.sagemaker')


def lambda_handler(event, context):

    #---------------------------------------------
    #  UNPACK QUERY
    #---------------------------------------------

    # disregard messages other than those containing features
    if 'features' not in event:
        logger.info(event)
        return

    query = event
    # features are sent by the DeepLens device in CSV form
    query_features = query['features']

    #---------------------------------------------
    #  k-NN INDEX LOOKUP
    #---------------------------------------------

    res = runtime.invoke_endpoint(
                EndpointName=endpoint_name,
                Body=query_features,
                ContentType='text/csv',
                Accept='application/json; verbose=true'
            )

    # extract reference item ids, convert them to a list of strings
    neighbors = json.loads(res['Body'].read())
    f_nb = (((neighbors['predictions'])[0])['labels'])
    ids = [str(int(e)) for e in f_nb]


    #---------------------------------------------
    #  METADATA LOOKUP
    #---------------------------------------------

    # batch request for reference item metadata
    response = dynamodb.batch_get_item(
                        RequestItems={
                                table_name: {
                                    'Keys': [
                                        { 'id': ids[0] },
                                        { 'id': ids[1] },
                                        { 'id': ids[2] },
                                        { 'id': ids[3] }
                                    ],
                                    'ConsistentRead': False,
                                    'AttributesToGet': ['id', 'title', 'url']
                                }
                            },
                          ReturnConsumedCapacity='TOTAL'
                        )


    json_items = json.loads(json.dumps(response['Responses']))
    for _, val in json_items.items():
        matches = val

    # items returned by DynamoDB aren't in nearest match order -> rearrange
    ordered_matches = []
    for index in ids:
        for match in matches:
            if match['id'] == index:
                ordered_matches.append(match)
                continue

    query_result = {}
    query_result['matches'] = ordered_matches

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


