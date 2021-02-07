from boto3 import Session
session = Session()
credentials = session.get_credentials()
current_credentials = credentials.get_frozen_credentials()
print(current_credentials.access_key)
print(current_credentials.secret_key)
print(current_credentials.token)
