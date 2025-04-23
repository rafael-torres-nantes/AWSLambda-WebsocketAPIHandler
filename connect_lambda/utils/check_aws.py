import boto3
import boto3.session
from botocore.exceptions import ClientError
from utils.import_credentials import aws_credentials

class AWS_SERVICES:
    def __init__(self, region_name='us-east-1'):
        # Inicializa as credenciais AWS usando a função aws_credentials() que retorna ACCESS_KEY, SECRET_KEY e SESSION_TOKEN.
        self.ACESS_KEY, self.SECRET_KEY, self.SESSION_TOKEN = aws_credentials()
        
        # Armazena a região
        self.region_name = region_name

        # Cria uma sessão AWS automaticamente ao inicializar a classe.
        self.session = self.login_session_AWS()

    
    def login_session_AWS(self):
        # Função que cria uma sessão AWS usando as credenciais fornecidas (ACCESS_KEY, SECRET_KEY, SESSION_TOKEN).
        session = boto3.Session(aws_access_key_id=self.ACESS_KEY, 
                                aws_secret_access_key=self.SECRET_KEY, 
                                aws_session_token=self.SESSION_TOKEN,
                                region_name=self.region_name)
        
        # Retorna a sessão criada.
        return session
    
    def check_aws_credentials(self):
        # Verifica se as credenciais AWS são válidas usando o serviço STS (Security Token Service).
        try:
            # Cria um cliente STS com a sessão atual.
            sts_client = self.session.client('sts')
            
            # Obtém a identidade do chamador (conta, ARN, UserID) para verificar as credenciais.
            identity = sts_client.get_caller_identity()
            
            # Se bem-sucedido, imprime os detalhes da conta, UserID e ARN.
            print("AWS credentials are valid.")
            print(f"Account: {identity['Account']}, UserID: {identity['UserId']}, ARN: {identity['Arn']}")
            
            # Retorna True indicando que as credenciais são válidas.
            return True
        
        # Em caso de erro ao verificar as credenciais, captura a exceção e imprime uma mensagem de erro.
        except ClientError as e:
            print("Erro ao verificar a sessão: ", e)
            return False
    
# Bloco principal que será executado ao rodar o script.
if __name__ == "__main__":
    # Inicializa a classe AWS_SERVICES, o que automaticamente cria uma sessão.
    aws_utils = AWS_SERVICES()
        
    # Verifica se as credenciais são válidas.
    aws_utils.check_aws_credentials()