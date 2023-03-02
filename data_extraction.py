import pandas as pd
import tabula
import requests
import boto3
from botocore import UNSIGNED
from botocore.client import Config

class DataExtractor:
    # This class contains methods that extract data from various sources
    def __init__(self, database_connector) -> None:
        self.database_connector = database_connector
        self.number_of_stores_endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'

    def extract_rds_table(self, table_name):
        engine = self.database_connector.init_db_engine()
        table = pd.read_sql_table(table_name, engine)   
        rds_dataframe = pd.DataFrame(table)
        return rds_dataframe
    
    def retrieve_pdf_data(self, link):
        tables = tabula.read_pdf(link, lattice=True, pages='all')
        df = pd.concat(tables)
        return df

    def retrieve_stores_data(self, header):
        df_list = []
        for i in range(451):
            response = requests.get(f'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{i}', headers=header)
            dict_response = response.json()
            df = pd.DataFrame(dict_response, index=[i])
            df_list.append(df)
            stores_df = pd.concat(df_list, ignore_index=True)
        return stores_df

    def list_number_of_stores(self, header):
        response = requests.get(self.number_of_stores_endpoint, headers=header)
        return response
    
    def extract_from_s3(self):
        s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
        products_data = s3.get_object(Bucket='data-handling-public', Key='products.csv')
        products_df = pd.read_csv(products_data['Body'])
        return products_df

    def extract_json_data(self, link):
        df = pd.read_json(link)
        return df