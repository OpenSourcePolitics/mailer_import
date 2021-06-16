import sib_api_v3_sdk as sib
import psycopg2
import sqlalchemy
import os
import pandas as pd


def set_database_connection():
    global connection 
    engine = sqlalchemy.create_engine(
        "postgresql+psycopg2://postgres@localhost/sendinblue"
    )
    connection = engine.connect()


def config_api(API_KEY=os.getenv("SIB_API_KEY")):
    configuration = sib.Configuration()
    configuration.api_key['api-key'] = API_KEY

    api_client = sib.ApiClient(configuration)
    return api_client


def convert_data_object_to_sql(table_name, data_object):
    df = pd.DataFrame(data_object)
    df.to_sql(
        table_name,
        connection,
        if_exists='replace',
        dtype={
            'recipients': sqlalchemy.types.JSON,
            'sender': sqlalchemy.types.JSON,
            'statistics': sqlalchemy.types.JSON
        }
    )
