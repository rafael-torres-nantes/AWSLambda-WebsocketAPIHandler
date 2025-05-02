import json
import os

# Nome da tabela DynamoDB onde os logs serão registrados
ARN_LAMBDA_SEND_FEEDBACK = os.getenv('ARN_LAMBDA_SEND_FEEDBACK')
ARN_LAMBDA_GET_BRIEFING = os.getenv('ARN_LAMBDA_GET_BRIEFING')
ARN_API_LAMBDA_CONNECT = os.getenv("ARN_API_LAMBDA_CONNECT")
ARN_API_LAMBDA_DISCONNECT = os.getenv("ARN_API_LAMBDA_DISCONNECT")
HASH_KEY = os.getenv('HASH_KEY')

# --------------------------------------------------------------------
# Função Lambda que processa a requisição de autorização
# ----------------------------------------------------------------
def lambda_handler(event, context):
    # 1 - Log the event
    print('*********** The event is: ***************')
    print(event)
    
    # 2 - See if the person's token is valid
    auth = 'Deny'
    if 'queryStringParameters' in event and event['queryStringParameters']:
        if 'authorization' in event['queryStringParameters'] and event['queryStringParameters']['authorization'] == HASH_KEY:
            auth = 'Allow'
            
    # 3 - Construct and return the response
    authResponse = {
        "principalId": "abc123",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Resource": [
                        ARN_LAMBDA_SEND_FEEDBACK,
                        ARN_LAMBDA_GET_BRIEFING,
                        ARN_API_LAMBDA_CONNECT,
                        ARN_API_LAMBDA_DISCONNECT
                    ],
                    "Effect": auth
                }
            ]
        }
    }
    return authResponse