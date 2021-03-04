import boto3

ssm_client = boto3.client('ssm')
PUBLIC_KEY_PARAM = ssm_client.get_parameter(
    Name='/Vhserver/Discord/PublicKey',
    WithDecryption=False
)
PUBLIC_KEY = PUBLIC_KEY_PARAM['Parameter'].get('Value')

SERVER_START_PARAM = ssm_client.get_parameter(
    Name='/Vhserver/Discord/Command/Start',
    WithDecryption=False
)
SERVER_START_ID = SERVER_START_PARAM['Parameter'].get('Value')

RESPONSE_TYPES =  { 
                    'PONG': 1, 
                    'ACK_NO_SOURCE': 2, 
                    'MESSAGE_NO_SOURCE': 3, 
                    'MESSAGE_WITH_SOURCE': 4, 
                    'ACK_WITH_SOURCE': 5
                  }

DISCORD_BODY = {
            'type': RESPONSE_TYPES['MESSAGE_NO_SOURCE'],
            'data': {
                'tts': False,
                'content': 'BEEP BOOP',
                'embeds': [],
                'allowed_mentions': []
            }
        }