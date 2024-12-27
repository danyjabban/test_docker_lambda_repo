import json
import numpy as np
import boto3

def lambda_handler(event, context):
    arr = np.random.randn(3,3)
    d = {'message': 'Hello from Lambda! update made test CICD', 'matrix':arr.tolist()}

    sqs = boto3.client("sqs")

    sqs.send_message(
        Queue_url = "https://sqs.us-east-1.amazonaws.com/116497644226/MyQueue1",
        message_body = json.dumps(d)
    )

    
    return {
        'statusCode': 200,
        'body': json.dumps(d)
    }