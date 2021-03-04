import json
import logging

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from ec2_control import (
    ec2Codes,
    start as server_start,
    CanNotStartException
)
import app_config as app


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def generate_response(status=400, body=app.DISCORD_BODY, body_content='BEEP BOOP', ping=False):    
    body['data']['content'] = body_content
    response = {
        'isBase64Encoded': False,
        'statusCode': status,
        'headers': { 'Content-Type': 'Application/json' },
        'body': json.dumps(body)
    }
    if ping:
        ping_pong = {'type': 1}
        response['body'] = json.dumps(ping_pong)
        return response

    return response

def verify_signature(event):
    body = event.get('body')
    signature = event['headers'].get('x-signature-ed25519')
    timestamp  = event['headers'].get('x-signature-timestamp')
    verify_key = VerifyKey(bytes.fromhex(app.PUBLIC_KEY))

    try:
        verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
    except BadSignatureError:
        raise Exception(401, 'invalid request signature')

def ping_pong(body):
    if body.get('type') == 1:
        return True
    return False

def start_server(body):
    # Example Payload
    #  {"id":"816801171791937587","name":"server","options":[{"name":"start","type":5,"value":true}]}
    options = body['data'].get('options')
    if (body['data'].get('id') == app.SERVER_START_ID
      and options[0]['name'] == 'start'
      and options[0]['value'] == True):
        return True
    return False
    
def handler(event, context):
    logger.info('## EVENT')
    logger.info(event)
    json_body = json.loads(event['body']) if event['body'] is not None else None
    if event['httpMethod'] != 'POST':
        response = generate_response(body_content='bad request')
        logger.warn(response)
        return response

    # verify the signature
    try:
        verify_signature(event)
    except:
        response = generate_response(status=401, body_content='Invalid request signature')
        logger.warn(response)
        return response


    # check if message is a ping
    if ping_pong(json_body):
        response = generate_response(status=200, ping=True)
        logger.info(response)
        return response
    elif start_server(json_body):
        try:
            ec2_status = server_start()
            message = 'Congrats you did it, Give it a few minutes and play your heart out.'
            if ec2_status['Code'] != (ec2Codes.pending or ec2Codes.running):  # Instance State code 0 == Pending 16 == Running
                message = 'You really messed this one up, better ask Mitch'
            response = generate_response(status=200, body_content=message)
            logger.info(response)
            return response
        except CanNotStartException as ex:
            message = str(ex)
            response = generate_response(status=200, body_content=message)
            logger.info(response)
            return response

    
    # dummy return
    response = generate_response(status=200)
    logger.info(response)
    return response
   