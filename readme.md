# AWS Lambda - WebSocket no API Gateway

## 👨‍💻 Projeto desenvolvido por: 
[Rafael Torres Nantes](https://github.com/rafael-torres-nantes)

## Índice

* 📚 Contextualização do projeto
* 🛠️ Tecnologias/Ferramentas utilizadas
* 🖥️ Funcionamento do sistema
   * 🧩 Parte 1 - Backend
* 🔀 Arquitetura da aplicação
* 📁 Estrutura do projeto
* 📌 Como executar o projeto
* 🕵️ Dificuldades Encontradas
* 🔑 Política de Permissões AWS
* 🖥️ Detalhes sobre a Função Lambda

## 📚 Contextualização do projeto

Este projeto utiliza **AWS Lambda** e **API Gateway** para implementar comunicação bidirecional em tempo real via WebSocket. Ele permite que mensagens sejam enviadas e recebidas entre clientes conectados, com suporte para armazenamento de logs no **Amazon DynamoDB**.

## 🛠️ Tecnologias/Ferramentas utilizadas

[<img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white">](https://www.python.org/)
[<img src="https://img.shields.io/badge/Visual_Studio_Code-007ACC?logo=visual-studio-code&logoColor=white">](https://code.visualstudio.com/)
[<img src="https://img.shields.io/badge/Boto3-0073BB?logo=amazonaws&logoColor=white">](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
[<img src="https://img.shields.io/badge/AWS-API_Gateway-FF9900?logo=amazonaws&logoColor=white">](https://aws.amazon.com/api-gateway/)
[<img src="https://img.shields.io/badge/AWS-DynamoDB-FF9900?logo=amazonaws&logoColor=white">](https://aws.amazon.com/dynamodb/)

## 🖥️ Funcionamento do sistema

### 🧩 Parte 1 - Backend

O backend foi desenvolvido em **Python** e utiliza o **AWS Lambda** para gerenciar conexões WebSocket e interagir com o **Amazon DynamoDB**. As principais funcionalidades incluem:

1. **Gerenciamento de Conexões**:
   - Durante o evento de conexão (`$connect`), o **API Gateway** invoca uma função Lambda que registra a conexão no **Amazon DynamoDB**, armazenando o `connectionId` fornecido pelo API Gateway. Esse `connectionId` é usado para identificar e enviar mensagens para clientes específicos.
   - No evento de desconexão (`$disconnect`), outra função Lambda é acionada para remover o `connectionId` correspondente do DynamoDB, garantindo que conexões inativas sejam limpas.

2. **Processamento de Mensagens**:
   - O **API Gateway** encaminha mensagens recebidas para a função Lambda principal, que processa o conteúdo do `$request.body.action`. Este campo é usado para determinar a ação a ser executada, como enviar mensagens para outros clientes ou realizar operações específicas no backend.

3. **Armazenamento de Logs**:
   - Mensagens e eventos são registrados no **Amazon DynamoDB** para fins de auditoria e análise. A classe `DynamoDBClass` é responsável por interagir com o banco de dados.

4. **Envio de Mensagens**:
   - A classe `APIGatewayClass` utiliza o **API Gateway Management API** para enviar mensagens em tempo real para clientes conectados, identificados pelo `connectionId`.

## 🔀 Arquitetura da aplicação

A aplicação segue uma arquitetura modular, com classes específicas para cada serviço AWS. O fluxo principal é gerenciado pela função Lambda definida em lambda_handler.py, que orquestra as interações entre os serviços.

## 📁 Estrutura do projeto

A estrutura do projeto é organizada da seguinte maneira:

```
.
├── connect_lambda/
│   ├── services/
│   │   ├── apigateway_service.py
│   │   └── dynamodb_service.py
│   ├── lambda_handler.py
│   └── .env
├── disconnect_lambda/
│   ├── services/
│   │   ├── apigateway_service.py
│   │   └── dynamodb_service.py
│   ├── lambda_handler.py
│   └── .env
└── readme.md
```

## 📌 Como executar o projeto

Para executar o projeto localmente, siga as instruções abaixo:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/rafael-torres-nantes/aws-lambda-websocket.git
   ```

2. **Configure as credenciais AWS:**
   Preencha o arquivo .env com suas credenciais AWS, conforme o exemplo em .env.example.

3. **Instale as dependências:**
   Certifique-se de ter o Python instalado e execute:
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a função Lambda localmente:**
   Utilize o AWS SAM CLI ou frameworks equivalentes para simular a execução da função Lambda.

## 🕵️ Dificuldades Encontradas

Durante o desenvolvimento, algumas dificuldades foram enfrentadas, como:

- **Gerenciamento de Conexões**: Garantir que as conexões fossem gerenciadas corretamente durante eventos de conexão e desconexão.
- **Configuração do API Gateway**: Configurar corretamente o WebSocket no API Gateway para suportar mensagens bidirecionais.
- **Armazenamento de Logs**: Implementar um sistema eficiente para registrar eventos no DynamoDB.

## 🔑 Política de Permissões AWS

Abaixo está um exemplo de política de permissões AWS utilizada para este projeto. Essa política garante que a função Lambda tenha acesso aos serviços necessários, como o **API Gateway** e o **DynamoDB**:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "execute-api:ManageConnections",
                "dynamodb:PutItem",
                "dynamodb:DeleteItem",
                "dynamodb:Scan"
            ],
            "Resource": "*",
            "Effect": "Allow"
        }
    ]
}
```

### Explicação da Política

- **`execute-api:ManageConnections`**: Permite que a função Lambda gerencie conexões WebSocket no API Gateway.
- **`dynamodb:PutItem`**: Permite inserir itens no DynamoDB.
- **`dynamodb:DeleteItem`**: Permite excluir itens do DynamoDB.
- **`dynamodb:Scan`**: Permite escanear tabelas no DynamoDB.
- **`Resource: "*"`**: Aplica as permissões a todos os recursos. Para maior segurança, substitua o `*` pelo ARN específico dos recursos utilizados.

Certifique-se de ajustar a política conforme necessário para atender aos requisitos de segurança e funcionalidade do seu projeto.

## 🖥️ Detalhes sobre a Função Lambda

Na função Lambda, é essencial obter informações específicas do evento recebido para gerenciar as conexões WebSocket e interagir com o API Gateway. O exemplo abaixo demonstra como capturar o `connection_id`, o `domain` e o `stage` do evento:

```python
# ----------------------------------------------------------------------------
# Função Lambda para inferência de modelos de NLP e armazenamento no DynamoDB
# ----------------------------------------------------------------------------
def lambda_handler(event, context):

   # 1 - Imprime o evento recebido
   print('*********** Start Lambda ***************')
   print(f'[DEBUG] Event: {event}')

   # 2 - Obtém o ID da conexão do evento, e o domain e stage do API Gateway
   connection_id = event['requestContext']['connectionId']
   domain_name = event['requestContext']['domainName']
   stage = event['requestContext']['stage']
```

### Explicação do Código

1. **`connection_id`**: Identifica exclusivamente a conexão WebSocket. É usado para enviar mensagens para clientes específicos.
2. **`domain_name`**: Representa o domínio do endpoint do API Gateway.
3. **`stage`**: Indica o estágio do API Gateway (por exemplo, `dev`, `prod`).

Essas informações são cruciais para gerenciar conexões e enviar mensagens em tempo real para os clientes conectados.
