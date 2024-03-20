import os
import boto3
import json
import base64
from model import Demucs
from config import settings


from pathlib import Path
from tempfile import NamedTemporaryFile
import torch
""" 
# Demucs = model.Demucs
# settings= config.settings """


client = boto3.client('s3')
resource = boto3.resource('s3')

outdir = os.path.join(settings.data, 'separated')


destination_bucket = os.environ.get('DESTINATION_BUCKET')
model = Demucs(output_dir=outdir, load=False)
track_folder = None
torch.hub.set_dir(settings.model)


def upload(path, destination_bucket, id):
    print(f"list of paths in tmp folder { os.listdir(path='/tmp') }")

    print('running upload files')
    # bucket_path = f"{ bucket}/{user}"
    try:
        for root, dirs, files in os.walk(path):
            for file in files:

                print(f'path to file uploading ... :{root,file}')
                client.upload_file(os.path.join(root, file),
                                   destination_bucket, f'{id}/split/{file}')

    except Exception as err:
        print(err)
        return {"statusCode": 400,
                'errorMessage': err}

    finally:
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Acces-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "GET",
            },
            "body": id
        }


def lambda_handler(event, context):
    print(f"EVENT ::::{event}")
    print(context, "CONTEXT")
    # print("Lambda function ARN:", context.invoked_function_arn)
    # print("CloudWatch log stream name:", context.log_stream_name)
    # print("CloudWatch log group name:",  context.log_group_name)
    # print("Lambda Request ID:", context.aws_request_id)
    # print("COGNITO:", context.identity)
    # print("COGNITO ID:", context.identity.cognito_identity_id)

    id = context.identity.cognito_identity_id

    model.load()

    os.chdir('/tmp')
    with NamedTemporaryFile(delete=False) as tmp:
        file_content = base64.b64decode(event)
        tmp.write(file_content)
        tmp.flush()

        fpath = Path(tmp.name)
        res = model.separate(fpath)
        track_folder = res['path']['folder']
        return upload(track_folder, destination_bucket, id)
