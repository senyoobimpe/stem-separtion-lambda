import base64
import os
import tempfile
from pathlib import Path
import boto3
from basic_pitch import ICASSP_2022_MODEL_PATH

from basic_pitch.inference import predict
from basic_pitch.inference import predict_and_save
client = boto3.client('s3')


def lambda_handler(event, context):
    id = context.identity.cognito_identity_id
    # song = open(
    #     '/Users/senyo/Desktop/NOISELAB/lapi/src/midi/test-quartet.mp3', 'rb').read()
    # data = base64.b64encode(song)
    # print(f'DATA::::{data}')

    os.chdir('/tmp')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
        decoded = base64.b64decode(event)
        tmp.write(decoded)
        tmp.flush()
        print(tmp.name, 'TEMP FILExs')
        # output_path = '/'
        res = predict_and_save(
            audio_path_list=[tmp.name], output_directory='/tmp', save_midi=True, sonify_midi=False, save_notes=False, save_model_outputs=False)
        print(f'model output : {res}')
        # print(f'midi data : {midi_data}')
        # print(f'note events : {note_events}')
        # track_folder = res['path']['folder']
        file = tmp.name.split('/')[-1].split(".")[0]
        out_path = f'/tmp/{file}_basic_pitch.mid'
        print(file, "FILE")
        print('CURRENT', os.getcwd())
        print(os.path.exists(tmp.name))
        print(os.path.exists(out_path))

        print(out_path)

        if os.path.exists(out_path):
            client.upload_file(out_path,
                               'tracks-destination-nl', f'{id}/midi/{file}.mid')
