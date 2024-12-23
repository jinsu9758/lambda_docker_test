import json
from src.predict import Lamb
import boto3
import os
import requests
import shutil


#역할부여 해야함.
def s3_download_file():
    s3 = boto3.client('s3')
    bucket_name = 'pre-upload-amoin-bucket'

    if not os.path.exists('/tmp/check'):
        os.makedirs('/tmp/check')

    response = s3.list_objects_v2(Bucket=bucket_name)

    for obj in response['Contents']:
        file_key = obj['Key']
        download_path = f"/tmp/check/" + file_key  # 파일명을 임시 경로로 지>정

        # 파일 다운로드
        s3.download_file(bucket_name, file_key, download_path)

        # 다운로드 완료 메시지
        print(f"Downloaded {file_key} to {download_path}")
    return file_key



def handler(event, context):
    file = s3_download_file()
    if os.path.exists('/tmp/extracted'):
        shutil.rmtree('/tmp/extracted/')
        
    pred = Lamb()
    result = pred.predict(file)

    if 'success' in result:
        result['success'] = {k: float(v) for k, v in result['success'].items()}
    
    url = "http://15.165.218.60:8000/developer_page/recieve_result"
    data = result
    res = requests.post(url, json=data)
    
    print(result, res.status_code)

    if os.path.exists('/tmp/check'):
        shutil.rmtree('/tmp/check')



