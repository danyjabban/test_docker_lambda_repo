import json
import numpy as np

def lambda_handler(event, context):
    arr = np.random.randn(3,3)

    d = {'message': 'Hello from Lambda! update made test CICD', 'matrix':arr.tolist()}
    return {
        'statusCode': 200,
        'body': json.dumps(d)
    }