import json
import boto3

REGION = 'us-west-2'

class ec2Codes:
    pending = 0
    running = 16
    shutting_down = 32
    terminated = 48
    stopping = 64
    stopped = 80


ssm_client = boto3.client('ssm')
ec2_client = boto3.client('ec2', region_name=REGION)
ec2_resource = boto3.resource('ec2')

INSTANCE_PARAM = ssm_client.get_parameter(
    Name='/Vhserver/Server/InstanceID',
    WithDecryption=False
)
INSTANCE_ID = INSTANCE_PARAM['Parameter'].get('Value')

def start():
    instance = ec2_resource.Instance(INSTANCE_ID)
    if instance.state['Code'] == (ec2Codes.running or ec2Codes.pending):
        raise CanNotStartException('Server already running or starting, Be patient young padawan.')
    elif instance.state['Code'] == (ec2Codes.shutting_down or ec2Codes.stopping):
        raise CanNotStartException('Server is going down for a rest, you can try again in a couple of minutes.')
    elif instance.state['Code'] == ec2Codes.terminated:
        raise CanNotStartException('server has been deleted, find a new game to play.')
    elif instance.state['Code'] == ec2Codes.stopped:
        ec2_client.start_instances(InstanceIds=[INSTANCE_ID])
    return instance.state

    
class CanNotStartException(Exception):
    pass
