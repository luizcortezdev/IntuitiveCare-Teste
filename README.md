# Teste de Alinhamento IntuitiveCare

Repositorio criado para disponibilizar minha resolução do teste de nivelamento para estagio na area de engenharia de software na IntuitiveCare


### Teste de API com Vue.js e Python

O Objetivo sera desenvolver uma interface web interativa utilizando Vue.js que se comunique com um servidor em Python para realizar operações de busca textual na lista de cadastros de operadoras, conforme preparado anteriormente. Além disso, sera feito o deploy desta aplicação em um ambiente de nuvem da AWS, usando um servidor EC2 e um banco de dados Postgres dentro da AWS pelo RDS!

Link para API: https://bit.ly/operadoras_ans 

Documentação da API em /docs do site!!

##### REQUISITOS: 

- Conta AWS
- Maquina EC2 Ubuntu
- Acesso SSH a maquina
- Banco de dados RDS da postgres

Certifique-se de ter as seguintes bibliotecas python instaladas:

`fastapi`
`uvicorn`
`psycopg2`



##### VPC:

Crie uma vpc com 2 subnets publicas e 2 subnets privadas



##### Firewall:

Configure o security group da maquina ec2, liberando o trafego de entrada para as portas 80(http) e 22(ssh)
Configure o security group do banco RDS, liberando o trafego de entrada para as porta 5432(postgresql) apenas para o security group da maquina ec2!!
Atenção: nao libere o acesso publico ao banco!!!



##### Configuração EC2:

Crie uma maquina ubuntu ec2 com o seguinte user data:

```
#!/bin/bash
sudo apt update
sudo apt upgrade -y
sudo apt install python3 python3-pip -y
sudo pip3 install fastapi uvicorn psycopg2
sudo apt install git
sudo git clone https://github.com/luizcortezdev/IntuitiveCare-Teste

```
Acesse a pasta API no repositorio clonado

suba o servidor com o comando:

```
python3 app.py
```
Teste usando o dns da maquina ec2


### WEB SCRAPING COM PYTHON:

O objetivo deste teste é demonstrar a capacidade de realizar web scraping utilizando as linguagens Python ou Java e + o Upload na nuvem da AWS. O código desenvolvido deve automatizar as seguintes tarefas:

- Acesso ao site: https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos

- Download dos Anexos I e II em formato PDF.

- Compactação de todos os anexos em um único arquivo (formatos ZIP, RAR, etc.)

- Upload do arquivo ZIP para um bucket no Amazon S3.


##### REQUISITOS:

- Conta AWS
- Ter um usuario IAM autenticado a fazer upload de arquivos dentro de um bucket S3 na AWS
- Credenciais de Acesso do usuario IAM
  

Certifique-se de ter as seguintes bibliotecas instaladas:

- `requests`
- `beautifulsoup4`
- `wget`
- `boto3`

  
Você pode instalá-las via pip:
```
pip install requests beautifulsoup4 wget boto3
```



##### UTILIZAÇÃO:


1. Baixe o arquivo scraping.py em https://github.com/luizcortezdev/IntuitiveCare-Teste/tree/main/web_scraping

1. Antes de executar o script, preencha as credenciais de acesso da AWS nos campos `aws_access_key_id`, `aws_secret_access_key` e o nome de seu bucket s3 no comando `client.upload_file`.

2. Execute o script Python.



### TRANSFORMAÇÃO DE DADOS EM TABELA PDF PARA TABELA CSV:

O Objetivo principal dessa atividade é um código em Python que extraia uma Tabela de um arquivo PDF, transforme os dados, estruture em um formato legível e compacte-a em CSV para facilitar o armazenamento e compartilhamento, apos isso, upe o arquivo csv para um Bucket S3 na nuvem AWS.



##### REQUISITOS:

- Conta AWS
- Ter um usuario IAM autenticado a fazer upload de arquivos dentro de um bucket S3 na AWS
- Credenciais de Acesso do usuario IAM

Certifique-se de ter as seguintes bibliotecas python instaladas:

`tabula`
`pandas`
`boto3`



##### UTILIZAÇÃO:

1. Preencha as credenciais de acesso da AWS nos campos `aws_access_key_id`, `aws_secret_access_key` e o nome de seu bucket s3 no comando `client.upload_file`.
2. Execute o Script





### CONVERSÃO DE TABELA CSV PARA BANCO DE DADOS:

O objetivo deste teste é transformar algumas tabelas CSV das operadoras registradas na ans em uma tabela de banco de dados utilizando PostgreSQL


As etapas incluem:

Preparação:
- Baixar os dados cadastrais das operadoras ativas no formato CSV.

Código:
- Criar a estrutura das tabelas no banco de dados para armazenar os dados do CSV.
- Importar os dados do CSV para a tabela recém-criada.
- Transformação de dados com sintaxe errada para banco de dados
        
Consultas: 
- Quais as 10 operadoras com maiores despesas em "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" no último trimestre?
- Quais as 10 operadoras com maiores despesas nessa categoria no último ano?



##### UTILIZAÇÃO: 

TABELAS:

Alguns atributos numericos e de data foram declarados como varchar, para entendimento SQL, apos isso, passará pela etapa de transformação de dados!!

```
CREATE TABLE operadoras (
    Registro_ANS INT PRIMARY KEY,
    CNPJ VARCHAR(20),
    Razao_Social VARCHAR(255),
    Nome_Fantasia VARCHAR(255),
    Modalidade VARCHAR(50),
    Logradouro VARCHAR(255),
    Numero VARCHAR(50),
    Complemento VARCHAR(255),
    Bairro VARCHAR(100),
    Cidade VARCHAR(100),
    UF CHAR(2),
    CEP VARCHAR(10),
    DDD VARCHAR(5),
    Telefone VARCHAR(20),
    Fax VARCHAR(20),
    Endereco_eletronico VARCHAR(255),
    Representante VARCHAR(255),
    Cargo_Representante VARCHAR(100),
    Regiao_de_Comercializacao INT,
    Data_Registro_ANS DATE
);

CREATE TABLE dados_contabeis(
	data VARCHAR(50), 
	registro_ans INTEGER, 
	cd_conta_contabil INTEGER, 
	descricao VARCHAR(200), 
	saldo_inicial VARCHAR(50), 
	saldo_final VARCHAR(50)
);
```



##### Importação de Dados CSV:

Importação feita usando o comando COPY do postgres
```
COPY operadoras FROM 'caminho para o arquivo csv' DELIMITER ';' CSV HEADER;
```



##### Transformação de Dados:
Nesta etapa, corriji a sintaxe incorreta para SQL, em seguida, alterei o tipo de atributo para date e decima, respectivamente!

```
UPDATE dados_contabeis 
SET 
    saldo_inicial = REPLACE(saldo_inicial, ',', '.')::NUMERIC,
    saldo_final = REPLACE(saldo_final, ',', '.')::NUMERIC,
    data = REPLACE(data, '/', '-');

ALTER TABLE dados_contabeis
ALTER COLUMN saldo_inicial TYPE DECIMAL USING saldo_inicial::DECIMAL,
ALTER COLUMN saldo_final TYPE DECIMAL USING saldo_final::DECIMAL,
ALTER COLUMN data TYPE DATE USING data::DATE;
```



##### Consultas SQL:

Consulta 1: 10 Operadoras com Maiores Despesas no Último Trimestre

```
SELECT op.Razao_social, dc.REGISTRO_ANS, dc.DESCRICAO, SUM(SALDO_INICIAL - SALDO_FINAL) AS DespesaTotal
FROM dados_contabeis AS dc
INNER JOIN operadoras AS op
ON op.Registro_ANS = dc.REGISTRO_ANS
WHERE 
    DATA >= date_trunc('quarter', (SELECT max(DATA) FROM dados_contabeis)) - interval '2 months' 
    AND DATA <= date_trunc('quarter', (SELECT max(DATA) FROM dados_contabeis)) + interval '1 month' - interval '1 day' 
GROUP BY op.Razao_Social, dc.REGISTRO_ANS, dc.DESCRICAO
ORDER BY DespesaTotal DESC
LIMIT 10;

```


Consulta 2: 10 Operadoras com Maiores Despesas no Último Ano com descriçao: EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR

```
SELECT op.Razao_social, dc.REGISTRO_ANS, dc.DESCRICAO, SUM(SALDO_INICIAL - SALDO_FINAL) AS DespesaTotal
FROM dados_contabeis AS dc
INNER JOIN operadoras AS op
ON op.Registro_ANS = dc.REGISTRO_ANS
WHERE 
    DATA >= date_trunc('year', (SELECT max(DATA) FROM dados_contabeis)) 
    AND DATA <= (SELECT max(DATA) FROM dados_contabeis)
    AND dc.Descricao LIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
GROUP BY op.Razao_Social, dc.REGISTRO_ANS, dc.DESCRICAO
ORDER BY DespesaTotal DESC
LIMIT 10;

```
Nota: Certifique-se de ajustar os caminhos dos arquivos CSV e adaptar as consultas conforme necessário para o seu ambiente de banco de dados.




