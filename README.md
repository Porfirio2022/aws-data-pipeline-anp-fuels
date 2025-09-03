# Pipeline de Dados de Preços de Combustíveis na AWS

## Visão Geral do Projeto

Este repositório contém os artefatos e a documentação de um projeto de engenharia de dados de ponta a ponta, construído na nuvem da AWS. O objetivo deste pipeline é ingerir, processar, armazenar e analisar dados públicos sobre os preços de combustíveis no Brasil, fornecidos pela Agência Nacional do Petróleo, Gás Natural e Biocombustíveis (ANP).

O projeto demonstra a construção de uma arquitetura serverless, escalável e resiliente, capaz de lidar com desafios de dados do mundo real.

## Arquitetura da Solução

A solução foi implementada utilizando uma arquitetura de Data Lakehouse na AWS, com as seguintes camadas e serviços:

![Diagrama da Arquitetura](architecture/architecture_diagram.png)

* **Ingestão (Extract):** Uma função **AWS Lambda** escrita em Python é responsável por buscar os dados mais recentes do portal da ANP, descompactar os arquivos `.zip` em memória e depositar os dados brutos (CSV) na camada `bronze` do nosso Data Lake.

* **Armazenamento (Storage):** O **Amazon S3** serve como nosso Data Lake, dividido em duas camadas principais:
    * **Camada Bronze:** Armazena os dados brutos, inalterados, como chegaram da fonte.
    * **Camada Silver:** Armazena os dados limpos, transformados, particionados e em formato colunar (Parquet), prontos para análise.

* **Transformação (Transform & Load):** O **AWS Glue Studio** foi utilizado para construir um job de ETL visual. Este job é responsável por:
    1.  Ler os dados da camada `bronze`.
    2.  Renomear colunas para um formato padronizado.
    3.  Converter os tipos de dados para formatos adequados (String para Date, Decimal, etc.).
    4.  Criar novas colunas de partição (`ano` e `mes`) usando uma transformação SQL.
    5.  Salvar o resultado final na camada `silver` em formato **Parquet**.

* **Catálogo de Dados e Análise (Analytics):**
    * O **AWS Glue Data Catalog** é populado automaticamente pelo job do Glue, criando uma tabela com o schema dos dados processados.
    * O **Amazon Athena** é utilizado como ferramenta de consulta interativa, permitindo a execução de consultas SQL diretamente nos arquivos da camada `silver` para análises de negócio.

## Stack de Tecnologia

* **Linguagens:** Python, SQL
* **Serviços AWS:**
    * AWS S3 (Data Lake)
    * AWS Lambda (Ingestão Serverless)
    * AWS Glue Studio (ETL Visual)
    * AWS Glue Data Catalog (Metadados)
    * Amazon Athena (Análise SQL)
    * AWS IAM (Gerenciamento de Permissões)
* **Formatos de Dados:** CSV, Parquet

## Desafios e Aprendizados

A execução deste projeto foi uma simulação fiel dos desafios encontrados no dia a dia de um engenheiro de dados. O principal obstáculo foi a qualidade e o formato inconsistente do arquivo de origem, o que exigiu um processo de depuração metódico e aprofundado, incluindo:
* Diagnóstico e correção de erros de schema, delimitadores e codificação de caracteres (`encoding`).
* Implementação de um pré-processamento manual dos dados (data laundering) para limpar o arquivo de origem.
* Superação de anomalias de ambiente da própria plataforma AWS, exigindo a migração completa do projeto entre regiões (`sa-east-1` para `us-east-1`) para garantir a estabilidade.
* Uso de múltiplas ferramentas de depuração (Logs do CloudWatch, Crawlers de diagnóstico, scripts customizados e a interface visual do Glue Studio) para isolar e resolver a causa raiz dos problemas.

## Conteúdo do Repositório

* `/lambda_function/ingestion_function.py`: Código Python da função Lambda de ingestão.
* `/glue/transformation_sql.sql`: Lógica SQL principal utilizada no nó de transformação do Glue Studio.
* `/architecture/architecture_diagram.png`: Diagrama visual da arquitetura do pipeline.
* `README.md`: Este arquivo.

---