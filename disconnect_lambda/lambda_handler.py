import os
import json
from dotenv import load_dotenv

# Importar as classes de serviços necessárias para a Lambda Function
from services.dynamodb_services import DynamoDBClass

#  Carregar variáveis de ambiente do arquivo .env
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
        print(f"[DEBUG][API_DISCONNECT] Cliente desconectado: {connection_id}")

        # 4 - Deleta o item do DynamoDB
        dynamodb_service.delete_item(connection_id)
        
        return {
            'statusCode': 200,
            'body': 'Desconexão processada com sucesso'
        }
    
    except Exception as e:
        print(f"[ERROR][API_DISCONNECT] Erro ao desconectar: {str(e)}")
        return {
            'statusCode': 503,
            'body': 'Falha ao processar desconexão'
        }
