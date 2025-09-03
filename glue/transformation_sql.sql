SELECT
    regiao_sigla,
    estado_sigla,
    municipio,
    revenda,
    cnpj_revenda,
    nome_da_rua,
    numero_rua,
    complemento,
    bairro,
    cep,
    produto,
    unidade_medida,
    bandeira,
    CAST(regexp_replace(valor_venda, ',', '.') AS DOUBLE) AS valor_venda,
    CAST(regexp_replace(valor_compra, ',', '.') AS DOUBLE) AS valor_compra,
    to_date(data_coleta, 'dd/MM/yyyy') AS data_coleta,
    year(to_date(data_coleta, 'dd/MM/yyyy')) AS ano,
    month(to_date(data_coleta, 'dd/MM/yyyy')) AS mes
FROM
    myDataSource