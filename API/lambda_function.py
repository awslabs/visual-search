'''

VISUAL SEARCH API LAMBDA FUNCTION

'''

import redis
import logging
import json

#------------------------------------------
# CONSTANTS
#
# replace <your-redis-endpoint>
#------------------------------------------

redis_hostname = '<your-redis-endpoint>'

#------------------------------------------

r = redis.StrictRedis(host=redis_hostname, port=6379, db=0, decode_responses=True)
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
