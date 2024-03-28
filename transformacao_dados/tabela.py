import tabula
import pandas as pd
import boto3

client = boto3.client(
    service_name='s3',
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name='us-east-1'
)

tabela = tabula.read_pdf('anexo1.pdf', pages='3-180')

tabela = pd.concat(tabela, ignore_index=True)

tabela = tabela.iloc[:, :13]

tabela = tabela.rename(columns={'OD': 'seg. odontológica', 'AMB': 'seg. ambulatorial'})

tabela = tabela.fillna('')

tabela = tabela[tabela[tabela.columns[0]] != '']

tabela.to_csv('anexo.csv', index=False, sep=';', quoting=1)

client.upload_file("anexo.csv", "tratamento-dados", "tabela-ans.csv")


