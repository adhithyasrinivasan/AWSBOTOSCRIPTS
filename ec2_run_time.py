import boto3
from datetime import datetime, timezone
from functools import reduce
import operator

ec2 = boto3.client('ec2')
cloudtrail = boto3.client('cloudtrail')

def get_events(instanceid):
    response = cloudtrail.lookup_events (
        LookupAttributes=[
            {
                'AttributeKey': 'ResourceName',
                'AttributeValue': instanceid
            }
        ],
    )
    return response

def get_timeframes(instanceid):
    details = get_events (instanceid)
    lasttime = ""
    start = []
    stop = []
    if not details.get ("Events"):
        return (None,None)
    for event in details.get ("Events"):
        if lasttime == event.get("EventTime").strftime('%H:%M'):
            continue
        if event.get ("EventName") == "RunInstances":
            owner = event.get ("Username")
            #print(event.get("EventTime"))
            start.append(event.get("EventTime"))
            lasttime = event.get("EventTime").strftime('%H:%M')
        if event.get ("EventName") == "StartInstances":
            start.append(event.get("EventTime"))
            lasttime = event.get("EventTime").strftime('%H:%M')
        if event.get ("EventName") == "StopInstances":
            stop.append(event.get("EventTime"))
            lasttime = event.get("EventTime").strftime('%H:%M')
    
    total_time = []
    for start_time,stop_time in zip(start[1:],stop):
        #print(stop_time-start_time)
        total_time.append(stop_time-start_time)
    
    present = datetime.now(timezone.utc) - start[:1][0]
    total_time.append(present)
    return(reduce(operator.add, total_time),owner)

response = ec2.describe_instances (Filters=[
    {
        'Name': 'instance-state-name',
        'Values': ['running']
    }
])

for r in response['Reservations']:
    for instance in r['Instances']:
        ins_id = instance['InstanceId']
        runtime,user = get_timeframes(ins_id)
        print (ins_id,user,runtime)
