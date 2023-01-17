import pandas as pd
import tabula
import requests
import boto3
from botocore import UNSIGNED
from botocore.client import Config

class DataExtractor:
    def extract_rds_table(self, DB_instance, table_name):
        self.DB_instance = DB_instance
        self.table_name = table_name
        engine = self.DB_instance.init_db_engine()
        table = pd.read_sql_table(table_name, engine)   
        df = pd.DataFrame(table)
        return df
    
    def retrieve_pdf_data(self, link):
        self.link = link
        tables = tabula.read_pdf(self.link, lattice=True, pages='all')
        df = pd.concat(tables)
        return df

    def retrieve_stores_data(self, header):
        self.header = header
        df_list = []
        for i in range(451):
            response = requests.get(f'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{i}', headers=self.header)
            dict_response = response.json()
            df = pd.DataFrame(dict_response, index=[i])
            df_list.append(df)
            df_final = pd.concat(df_list, ignore_index=True)
        
        return df_final

    def list_number_of_stores(self, header, endpoint='https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'):
        self.endpoint = endpoint
        self.header = header
        response = requests.get(self.endpoint, headers=self.header)
        return response
    
    def extract_from_s3(self, link):
        self.link = link

        s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
        products_data = s3.get_object(Bucket='data-handling-public', Key='products.csv')
        products_df = pd.read_csv(products_data['Body'])

        return products_df

    def extract_json_data(self, link):
        self.link = link
        df = pd.read_json(self.link)
        return df