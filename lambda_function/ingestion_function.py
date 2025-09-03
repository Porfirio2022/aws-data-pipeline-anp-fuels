import boto3
import requests
import os
from datetime import datetime
import zipfile
import io

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        bucket_name = os.environ['S3_BUCKET_NAME']
        data_url = os.environ['DATA_URL']
    except KeyError as e:
        print(f"Erro: Variável de ambiente {e} não foi definida!")
        raise e

    print(f"Iniciando ingestão do arquivo ZIP da URL: {data_url}")
    print(f"Bucket de destino: {bucket_name}")

    try:
        response = requests.get(data_url, verify=False)
        response.raise_for_status()
        print("Download do arquivo ZIP realizado com sucesso.")

        zip_in_memory = io.BytesIO(response.content)

        with zipfile.ZipFile(zip_in_memory, 'r') as zip_ref:
            csv_file_names = [name for name in zip_ref.namelist() if name.lower().endswith('.csv')]
            if not csv_file_names:
                raise ValueError("Nenhum arquivo CSV encontrado dentro do ZIP.")
            
            csv_file_name = csv_file_names[0]
            print(f"Arquivo CSV encontrado dentro do ZIP: {csv_file_name}")
            
            csv_content = zip_ref.read(csv_file_name)
        
        current_date = datetime.now().strftime('%Y-%m-%d')
        s3_key = f"bronze/anp-price-data/{current_date}-{csv_file_name}"

        print(f"Fazendo upload do conteúdo do CSV para s3://{bucket_name}/{s3_key}")
        s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=csv_content)

        print("Upload para o S3 concluído com sucesso!")
        
        return {
            'statusCode': 200,
            'body': f'Arquivo {csv_file_name} salvo com sucesso em {s3_key}'
        }

    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer o download do arquivo ZIP: {e}")
        raise e
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        raise e