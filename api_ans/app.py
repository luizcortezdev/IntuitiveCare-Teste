from fastapi import FastAPI, Query, File
from fastapi.responses import FileResponse
import uvicorn
import psycopg2

app = FastAPI()

conn = psycopg2.connect(
    dbname='intuitive',
    user='postgres',
    password='2422',
    host='localhost'
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

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=5000)
