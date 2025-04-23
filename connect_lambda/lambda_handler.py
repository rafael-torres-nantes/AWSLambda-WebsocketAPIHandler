import os
import json
from dotenv import load_dotenv

# Importar as classes de serviços necessárias para a Lambda Function
from services.dynamodb_services import DynamoDBClass

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém o nome da tabela do DynamoDB do arquivo .env
DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME')

def lambda_handler(event, context):
    
    try:
        # 1 - Imprime o evento recebido
        print('*********** Start Lambda ***************')
        print(f'[DEBUG] Event: {event}')

        # 2 - Instancia a classe DynamoDBClass
        dynamodb_service = DynamoDBClass(DYNAMODB_TABLE_NAME)

        # 3 - Obtém o valor de connection_id do evento
        connection_id = event['requestContext']['connectionId']
        print(f"[DEBUG][API_CONNECT] Cliente conectado: {connection_id}")

        # 4 - Registra o log no DynamoDB
        dynamodb_service.log_register_dynamodb(connection_id)
        
        return {
            'statusCode': 200,
            'body': 'Conexão estabelecida com sucesso'
        }
    
    except Exception as e:
        print(f"[ERROR][API_CONNECT] Erro ao conectar: {str(e)}")
        return {
            'statusCode': 503,
            'body': 'Falha na conexão'
        }
