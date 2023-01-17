import yaml
from sqlalchemy import create_engine
from sqlalchemy import inspect
from data_cleaning import DataClean
from data_extraction import DataExtractor
import pandas as pd

class DatabaseConnector:
    def read_db_creds(self):
        with open('db_creds.yaml', 'r') as db_creds_file:
            db_creds = yaml.safe_load(db_creds_file)
        return db_creds

    def init_db_engine(self):
        db_creds = self.read_db_creds()

        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = db_creds['RDS_HOST']
        USER = db_creds['RDS_USER']
        PASSWORD = db_creds['RDS_PASSWORD']
        DATABASE = db_creds['RDS_DATABASE']
        PORT = db_creds['RDS_PORT']
        
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        return engine

    def list_db_tables(self):
        engine = self.init_db_engine()
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        return table_names

    def upload_to_db(self, df):
        self.df = df

        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = 'localhost'
        USER = 'postgres'
        PASSWORD = 'postgres'
        DATABASE = 'Sales_Data'
        PORT = 5432
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

        self.df.to_sql('dim_store_details', engine, if_exists='replace')

conn_instance = DatabaseConnector()
extraction_instance = DataExtractor()
clean_instance = DataClean()

# JSON
# link = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json'
# date_data = extraction_instance.extract_json_data(link)
# date_data_cleaned = clean_instance.clean_date_data(date_data)
# conn_instance.upload_to_db(date_data_cleaned)

# ORDERS 
# orders = extraction_instance.extract_rds_table(conn_instance, 'orders_table')
# orders_cleaned = clean_instance.clean_orders_data(orders)
# conn_instance.upload_to_db(orders_cleaned)

# PRODUCT DETAILS EXTRACT, CLEAN, AND UPLOAD
# product_data_link = 's3://data-handling-public/products.csv'
# products = extraction_instance.extract_from_s3(product_data_link)
# cleaned_products = clean_instance.convert_product_weights(products)
# conn_instance.upload_to_db(cleaned_products)

# STORE DETAILS EXTRACT, CLEAN, AND UPLOAD
header_dict = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
dim_store_details = extraction_instance.retrieve_stores_data(header_dict)
cleaned_dim_store_details = clean_instance.clean_store_data(dim_store_details)
# conn_instance.upload_to_db(cleaned_dim_store_details)

# CARD DETAILS EXTRACT, CLEAN, AND UPLOAD
# card_details_link="https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
# dim_card_details = extraction_instance.retrieve_pdf_data(card_details_link)
# cleaned_dim_card_details = clean_instance.clean_card_data(dim_card_details)
# conn_instance.upload_to_db(cleaned_dim_card_details)