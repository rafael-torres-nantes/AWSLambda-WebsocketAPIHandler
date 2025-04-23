# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ #
# RUN LOCALY
from utils.check_aws import AWS_SERVICES

aws_services = AWS_SERVICES()

session = aws_services.login_session_AWS()
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ #

import json
import boto3
from botocore.exceptions import ClientError

class APIGatewayClass: 
    def __init__(self, apigateway_name=None):
        """
        Construtor da classe APIGatewayClass que inicializa o cliente API Gateway da sessão.

        Args:
            apigateway_name (str): Nome da API Gateway a ser criada ou acessada.
        """
        
        # Criação de nome da API Gateway
        self.api_name = apigateway_name
        
        # Inicializa o cliente API Gateway da sessão
        self.apigateway = session.client('apigateway', region_name='us-east-1')

    def init_apigateway_management(self, apigateway_domain=None, apigateway_stage=None):
        """
        Inicializa o cliente API Gateway Management API da sessão.

        Args:
            apigateway_domain (str): Domínio da API Gateway.
            apigateway_stage (str): Estágio da API Gateway.
        """

        # Define o domínio e o estágio da API Gateway Management API
        self.websocket_domain = apigateway_domain
        self.websocket_stage = apigateway_stage
        print(f'[DEBUG] O domímio da API Gateway {self.websocket_domain} e o estágio {self.websocket_stage} foram definidos.')

        # Inicializa o cliente API Gateway Management API da sessão
        self.apigateway_api_management = session.client('apigatewaymanagementapi', 
                                                        endpoint_url=f'https://{self.websocket_domain}/{self.websocket_stage}')

    def send_websocket_message(self, connection_id, message):
        """
        Envia uma mensagem para um cliente conectado a um WebSocket.

        Args:
            connection_id (str): ID da conexão do cliente.
            message (str): Mensagem a ser enviada.
        """
        try: 
            # Envia a mensagem para o cliente conectado
            self.apigateway_api_management.post_to_connection(
                ConnectionId=connection_id,
                Data=json.dumps({
                    'action': 'sendFeedback',
                    'status': 'success',
                    'message': f'{message}',
                }).encode('utf-8'),  # Converte a mensagem para bytes
            )
            
            print(f"[DEBUG] Enviando mensagem para o cliente {connection_id}: {message}")
            return True

        except ClientError as e:
            print(f"[DEBUG] Erro ao enviar mensagem para o cliente {connection_id}: {e}")
            raise e