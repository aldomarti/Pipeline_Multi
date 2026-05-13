import sys
import datetime
import time
import json
import io
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.transforms import *
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from awsglue.utils import getResolvedOptions
import pytz
import boto3
import pandas as pd

"""
- RESUMEN
- Squad              : PLAN DE DATOS RETAIL
- Descripción        : Job de carga archivos json verint transcription
- Fecha de Creación  : 11/10/2024
- Responsable IBK	 : David Silva C
- Autor              : David Silva C
- MODIFICACIONES
- Nro. (SRT/SRI)   Fecha         Desarrollador  Líder Técnico	  Descripción
- SRT_2024-12649   11/10/2024    David Silva C  David Silva C   Version Inicial

"""

# Obtener argumentos
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_BUCKET_INPUT', 'S3_BUCKET_OUTPUT',
                                     'S3_BUCKET_RESULT','P_ENV_DB','P_FECHA_INI','P_FECHA_FIN'])


key_mapping = {
    "Percent_of_mutual_silence": "tiempo_silencio",
    "Local_audio_start_time": "fechahora_inicio",
    "Duration_seconds": "duracion",
    "Direction": "direccion",
    "Percent_of_other_call": "tiempo_habla_cliente",
    "Pbx_login_id": "codigo_asesor",
    "Percent_of_agent_call": "tiempo_habla_asesor",
    "ContactID": "id_transcripcion",
    "CD2": "cuc_cliente",
    "CD4": "nombre_cliente",
    "Local_audio_end_time": "fechahora_fin",
    "Switch_call_id": "id_llamada",
    "Dnis": "numero_ibk",
    "CD6": "nivel_servicio",
    "Agent_name": "nombre_asesor",
    "Ani": "numero_cliente"
}

# Acceder a los parámetros
S3_BUCKET_INPUT = args['S3_BUCKET_INPUT']
S3_BUCKET_OUTPUT = args['S3_BUCKET_OUTPUT']
S3_BUCKET_RESULT = args['S3_BUCKET_RESULT']
P_ENV_DB = args['P_ENV_DB']
P_FECHA_INI = args['P_FECHA_INI']
P_FECHA_FIN = args['P_FECHA_FIN']

# Inicializar el entorno de Glue
glueContext = GlueContext(SparkContext.getOrCreate())

# Definir la zona horaria para Perú
zona_horaria_peru = pytz.timezone('America/Lima')
today_date = datetime.datetime.now(zona_horaria_peru)
#today_date = datetime.datetime(2024, 2, 29, 8, 30, 0, 0, zona_horaria_peru)
hora_limite_7am = today_date.replace(hour=7, minute=0, second=0, microsecond=0)
hora_limite_9am = today_date.replace(hour=9, minute=0, second=0, microsecond=0)

if P_FECHA_INI == '2020-01-01':
    # Comprobar si la hora actual está dentro del rango de 7:00 AM a 9:00 AM
    if hora_limite_7am <= today_date <= hora_limite_9am:
        start_date = today_date.date() - datetime.timedelta(days=1)
        end_date = today_date.date()
    else:
        start_date = today_date.date()
        end_date = today_date.date()
else:
    #Entrada Manual de Fecha
    start_date = datetime.datetime.strptime(P_FECHA_INI, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(P_FECHA_FIN, '%Y-%m-%d')

def process_day(date):
    bucket = S3_BUCKET_INPUT
    ruta = f"modeloscontactbtp/{date.strftime('%Y-%m-%d')}/"
    s3_client = boto3.client('s3')
    json_data = []
    paginator = s3_client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket,Prefix=ruta)
    for page in page_iterator:
        if 'Contents' in page:
            for obj in page['Contents']:
                if obj['Key'] == f"modeloscontactbtp/{date.strftime('%Y-%m-%d')}/":
                    pass
                else:
                    try:
                        obj_json = s3_client.get_object(Bucket=bucket, Key=obj['Key'])
                        file_content = obj_json['Body'].read().decode('utf-8')
                        json_content = json.loads(file_content)

                        json_final = json_content['metadata']
                        arreglo_details = json_content['plainTextTime']['verbatims']
                        arreglo_renombrado = []
                        for elemento in arreglo_details:
                            nuevo_elemento = {
                                "inicio_fragamento": str(elemento["s"]),
                                "fin_fragamento": str(elemento["e"]),
                                "fragamento": str(elemento["w"]),
                                "tipo_participante": str(elemento["sp"])
                            }
                            arreglo_renombrado.append(nuevo_elemento)
                        json_final['details'] = arreglo_renombrado
                        json_data.append(json_final)
                    except NoCredentialsError as e:
                        print(f"No credentials available for accessing S3: {e}")
                    except PartialCredentialsError as e:
                        print(f"Incomplete credentials provided for accessing S3: {e}")
                    except ClientError as e:
                        print(f"ClientError: {e}")
                    except json.JSONDecodeError as e:
                        print(f"Failed to decode JSON from the file content: {e}")
                    except Exception as e:
                        print(f"An unexpected error occurred: {e}")
        print('-----------------')
    print(f"Para la carpeta {date.strftime('%Y-%m-%d')} se tienen {len(json_data)} json")
    print('-------------------------')
    print("Se creara el dataframe")

    df = pd.DataFrame(json_data)
    if df.empty:
        print("El dataframe esta vacio, no se guardara nada")
    else:
        for original_key, new_key in key_mapping.items():
            if original_key in df.columns:
                df.rename(columns={original_key: new_key}, inplace=True)
            else:
                df[new_key] = None
        
        print(df.head())

        columna_a_no_convertir = 'details'
        columnas_a_convertir = [col for col in df.columns if col != columna_a_no_convertir]
        columna_no_convertida = df[columna_a_no_convertir]
        
        df[columnas_a_convertir] = df[columnas_a_convertir].astype(str)
        df[columna_a_no_convertir] = columna_no_convertida        
        parquet_buffer = io.BytesIO()
        df.to_parquet(parquet_buffer, index=False)
        
        parquet_buffer.seek(0)
        s3_bucket = S3_BUCKET_OUTPUT
        s3_key = (
            f"pre-stage/motion/streams/hubclientes/t_transcription/"
            f"p_date={date.strftime('%Y%m%d')}/data.parquet"
        )
        s3_client.upload_fileobj(parquet_buffer, s3_bucket, s3_key)

        print("Se repara la tabla")
        # Ejecutar MSCK REPAIR TABLE en Athena
        athena_database = P_ENV_DB
        athena_result = f"s3://{S3_BUCKET_RESULT}/"
        athena_table = 't_transcription'

        # Inicializar el cliente de Athena
        client = boto3.client('athena')

        # Definir la consulta
        query = f"MSCK REPAIR TABLE {athena_database}.{athena_table}"

        # Ejecutar la consulta
        response = client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={
                'Database': athena_database
            },
            ResultConfiguration={
                'OutputLocation': athena_result
            }
        )

        # Imprimir el ID de ejecución de la consulta
        print(f"Query execution ID: {response['QueryExecutionId']}")

        # Verificación del estado de la consulta
        query_execution_id = response['QueryExecutionId']

        # Número máximo de ciclos
        max_cycles = 5
        current_cycle = 0

        while current_cycle < max_cycles:
            query_status = client.get_query_execution(QueryExecutionId=query_execution_id)
            status = query_status['QueryExecution']['Status']['State']

            #if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            if status == 'SUCCEEDED':
                print(f"Query status: {status}")
                break
            elif status == 'FAILED':
                # Obtener la razón del fallo
                error_message = query_status['QueryExecution']['Status']['StateChangeReason']
                print(f"Query failed: {error_message}")
                break
            elif status == 'CANCELLED':
                print(f"Query status: {status}")
                break

            print("Waiting for query to finish...")

            current_cycle += 1  # Incrementar el contador
            time.sleep(5)  # Esperar 5 segundos antes de volver a comprobar

        if current_cycle == max_cycles:
            print("Se alcanzo el numero maximo de ciclos para comprobación. Exiting the loop.")

current_date = start_date
while current_date <= end_date:
    process_day(current_date)
    current_date += datetime.timedelta(days=1)
