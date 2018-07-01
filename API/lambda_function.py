'''

VISUAL SEARCH API LAMBDA FUNCTION

'''

import redis
import logging
import json

r = redis.StrictRedis(host='visual-search-2.de4w70.0001.use1.cache.amazonaws.com', port=6379, db=0, decode_responses=True)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    matches = r.lrange('stack:matches', 0, 0)[0]

    if matches is None:
        logger.error('NO MATCHES')
        response = {
            "statusCode": "400",
            "headers": { "Content-type": "application/json" },
            "body": "NO MATCHES"
        }
    else:
        logger.info('FOUND MATCHES:  ' + json.dumps(matches))
        response = {
            "statusCode": "200",
            "headers": { "Content-type": "application/json" },
            "body": matches
        }

    return response
