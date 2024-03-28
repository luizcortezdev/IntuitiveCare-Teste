import shutil
import requests
from bs4 import BeautifulSoup
import os
import wget
import boto3

url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

response = requests.get(url)

client = boto3.client(
    service_name='s3',
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name='us-east-1' 
)


if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    
    links = soup.find_all("a", href=True)
    
    os.makedirs("pdfs", exist_ok=True)
    pasta = 'pdfs'
    
    for link in links:
        if ("Anexo I" in link.text or "Anexo II" in link.text) and link.attrs.get("href").endswith(".pdf"):
            file_url = link.attrs.get("href")
            filename = file_url.split('/')[-1]
            wget.download(file_url, f'{pasta}/{filename}')
            print(filename, 'Download Concluido!')

    caminho_pasta = 'pdfs'
    caminho_zip = 'anexos'

    shutil.make_archive(caminho_zip, 'zip', caminho_pasta)
    shutil.rmtree(caminho_pasta)

    client.upload_file("anexos.zip", "webscraping2", "anexos")

else:
    print("Página Fora do Ar!!")