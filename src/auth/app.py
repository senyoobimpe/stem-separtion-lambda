import os 
import boto3
import json
import base64

import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


client = boto3.client('lambda')
# Use a service account.

def router(term):
    params ={
        'name': '',
        'payload':''
    }
        
def lambda_handler(event, context):
    print(f"EVENT ::::{event}")
    print(context,"CONTEXT")
    event_ip = event['ip']
    print(f'EVENT IP ::{event_ip}')

    ip,user = supabase.from('requests').select('ip', 'user').eq('ip', event_ip).execute()
    
    print(f'TABLE IP AND USER::{ip, user}')



    requests = supabase.table('requests').eq('ip', ip).execute()
    attempts = user.collection('attemps')

    if requests :
        if 0 < attempts < 4:
            attempts = supabase.table('requests').select('attemps').eq('ip', ip).execute()
            supabase.table('requests').update({'attempts', attempts +1 }).eq('ip', ip)

    else :
        params = {'ip': ip,attempts:1 }
        supabase.table('requests').insert(params)


    f = event['funciton_name']
    p = event['payload']
    client.invoke( FunctionName =f,
        Payload= p)

    return 'somtething'