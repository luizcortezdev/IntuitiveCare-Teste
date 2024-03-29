from fastapi import FastAPI, Query, File
from fastapi.responses import FileResponse
import uvicorn
import psycopg2

app = FastAPI()

conn = psycopg2.connect(
    dbname='',
    user='',
    password='',
    host='' #O Endpoint do Banco RDS da AWS
)

@app.get('/')
async def index():
    return FileResponse('static/index.html')


@app.get('/buscar-operadoras')
async def buscar_operadoras(query: str = Query(None)):
    if query is None:
        return []
    
    cursor = conn.cursor()
    cursor.execute("SELECT cnpj, razao_social FROM operadoras WHERE razao_social iLIKE %s", ('%' + query + '%',))
    resultados = [{'CNPJ': row[0], 'nome': row[1]} for row in cursor.fetchall()]
    cursor.close()
    return resultados

@app.get('/buscar-nome/{nome_operadora}')
async def buscar_operadora_por_nome(nome_operadora: str):
    cursor = conn.cursor()
    cursor.execute("SELECT cnpj, razao_social FROM operadoras WHERE razao_social iLIKE %s", ('%' + nome_operadora + '%',))
    resultados = [{'CNPJ': row[0], 'nome': row[1]} for row in cursor.fetchall()]
    cursor.close()
    return resultados

@app.get('/buscar-registro/{registro_ans}')
async def buscar_operadora_por_registro_ans(registro_ans: int):
    cursor = conn.cursor()
    cursor.execute("SELECT cnpj, razao_social FROM operadoras WHERE registro_ans = %s", (registro_ans,))
    resultados = [{'CNPJ': row[0], 'nome': row[1]} for row in cursor.fetchall()]
    cursor.close()
    return resultados


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=5000)
