----------------------------------------------- TABELAS -------------------------------------

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

----------------------------------- IMPORTAÇAO DE DADOS CSV ------------------------------------

COPY operadoras FROM '/var/lib/postgresql/16/main/intui/Relatorio_cadop.csv' DELIMITER ';' CSV HEADER;
COPY dados_contabeis FROM '/var/lib/postgresql/16/main/intui/2022/1T2022.csv' DELIMITER ';' CSV HEADER;
COPY dados_contabeis FROM '/var/lib/postgresql/16/main/intui/2022/2T2022.csv' DELIMITER ';' CSV HEADER ENCODING 'LATIN1';
COPY dados_contabeis FROM '/var/lib/postgresql/16/main/intui/2022/3T2022.csv' DELIMITER ';' CSV HEADER;
COPY dados_contabeis FROM '/var/lib/postgresql/16/main/intui/2022/4T2022.csv' DELIMITER ';' CSV HEADER;

COPY dados_contabeis FROM '/var/lib/postgresql/16/main/intui/2023/1T2023.csv' DELIMITER ';' CSV HEADER;
COPY dados_contabeis FROM '/var/lib/postgresql/16/main/intui/2023/2t2023.csv' DELIMITER ';' CSV HEADER;
COPY dados_contabeis FROM '/var/lib/postgresql/16/main/intui/2023/3T2023.csv' DELIMITER ';' CSV HEADER;

---------------------------- TRANSFORMAÇAO DE DADOS CSV PARA RECONHECIMENTO SQL -------------------------------------

UPDATE dados_contabeis 
SET 
    saldo_inicial = REPLACE(saldo_inicial, ',', '.')::NUMERIC,
    saldo_final = REPLACE(saldo_final, ',', '.')::NUMERIC,
    data = REPLACE(data, '/', '-');

ALTER TABLE dados_contabeis
ALTER COLUMN saldo_inicial TYPE DECIMAL USING saldo_inicial::DECIMAL,
ALTER COLUMN saldo_final TYPE DECIMAL USING saldo_final::DECIMAL,
ALTER COLUMN data TYPE DATE USING data::DATE;

---------------------------------------- CONSULTAS --------------------------------------------------------

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

