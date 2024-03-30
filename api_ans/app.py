from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse
import uvicorn
import psycopg2
import boto3

s3_client = boto3.client( # conexao com a interface vue.js por um bucket s3
    service_name='s3',
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name='us-east-1' 
)

conn = psycopg2.connect(
    dbname='',
    user='',
    password='',
    host='' #O Endpoint do Banco RDS da AWS
)

app = FastAPI()

@app.get('/') # Rota Interface Vue.js para Bucket S3
async def index():
    s3_bucket_name = "api-fastapi"
    response = s3_client.get_object(Bucket=s3_bucket_name, Key='index.html')
    html_content = response['Body'].read().decode('utf-8')

    return HTMLResponse(content=html_content, status_code=200)


@app.get('/buscar-operadoras') # Rota para busca textual por interface vue.js
async def buscar_operadoras(query: str = Query(None)):
    if query is None:
        return []
    
    cursor = conn.cursor()
    cursor.execute("SELECT cnpj, razao_social FROM operadoras WHERE razao_social iLIKE %s", ('%' + query + '%',))
    resultados = [{'CNPJ': row[0], 'nome': row[1]} for row in cursor.fetchall()]
    cursor.close()
    return resultados

@app.get('/buscar-nome/{nome_operadora}') # Rota API para busca textual - retorna json
async def buscar_operadora_por_nome(nome_operadora: str):
    cursor = conn.cursor()
    cursor.execute("SELECT cnpj, razao_social FROM operadoras WHERE razao_social iLIKE %s", ('%' + nome_operadora + '%',))
    resultados = [{'CNPJ': row[0], 'nome': row[1]} for row in cursor.fetchall()]
    cursor.close()
    return resultados

@app.get('/buscar-registro/{registro_ans}') # Rota API para busca por registro_ans - retorna json
async def buscar_operadora_por_registro_ans(registro_ans: int):
    cursor = conn.cursor()
    cursor.execute("SELECT cnpj, razao_social FROM operadoras WHERE registro_ans = %s", (registro_ans,))
    resultados = [{'CNPJ': row[0], 'nome': row[1]} for row in cursor.fetchall()]
    cursor.close()
    return resultados


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=5000)
