import boto3
import datetime
from collections import Counter
boto3.setup_default_session(profile_name='dev')
regions = ['us-east-1','us-west-2']

for region in regions:
	print("*****************************     {}    *****************************".format(region))
	ec2 = boto3.resource('ec2',region_name=region)

	instances = ec2.instances.filter(
		    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
	
	d=list()
	total_running=0
	inst=None
	for instance in instances:
		d.append(instance.instance_type)
		total_running+=1
		inst=instance
	running_count=Counter(d)
	print(running_count)
	print(inst)
