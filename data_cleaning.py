import pandas as pd

class DataClean:
    def __init__(self, df):
        self.df = df
        self.country_codes = ['DE', 'GB', 'US']

    def _categorise(self, categories, column):
        correct_rows = self.df[column].isin(categories)
        self.df = self.df[correct_rows]

    def clean_user_data(self):
        # remove invalid data
        self.categorise(self.country_codes, 'country_code')
        
        # standardise datetimes
        self.df.loc[:, 'date_of_birth'] = pd.to_datetime(self.df.loc[:, 'date_of_birth'], infer_datetime_format=True)
        self.df.loc[:, 'join_date'] = pd.to_datetime(self.df.loc[:, 'join_date'], infer_datetime_format=True)
    
    def clean_card_data(self):
        # reset index
       self.df = self.df.reset_index(drop=True)

        # remove null and invalid data
       card_categories = ['JCB 15 digit', 'JCB 16 digit', 'VISA 13 digit', 'Diners Club / Carte Blanche', 'VISA 19 digit', 'American Express', 'Maestro', 'VISA 16 digit', 'Discover']
       self.categorise(card_categories, 'card_provider')

    def clean_store_data(self):
        # remove 'lat' column
        self.df = self.df.drop(['lat'], axis=1)

        # remove invalid rows
        self.categorise(self.country_codes, 'country_code')

        # standardise opening_date
        self.df.loc[:, 'opening_date'] = pd.to_datetime(self.df.loc[:, 'opening_date'], infer_datetime_format=True)
        
        # remap continent errors
        mapping = {'eeEurope': 'Europe', 'eeAmerica': 'America'}
        self.df['continent'] = self.df['continent'].replace(mapping)
    
    def _unit_strip(self, i, unit, weight_str):
        # Method called inside fill_unit_column to strip 'weight' column of any letters
        self.df.loc[i, 'unit'] = unit
        stripped_weight_str = weight_str.replace(unit, '')
        self.df.loc[i, 'weight'] = stripped_weight_str

    def _fill_unit_column(self, i, row):
        # Method called inside convert_product_weights to assign correct unit string to each row 
        weight_str = str(row['weight'])
        if 'kg' in weight_str:
           self._unit_strip(i, 'kg', weight_str)
        elif 'g' in weight_str:
           self._unit_strip(i, 'g', weight_str)
        elif 'ml' in weight_str:
           self._unit_strip(i, 'ml', weight_str)
        elif 'oz' in weight_str:
           self._unit_strip(i, 'oz', weight_str)

        return weight_str # for use in dealing with multipacks (line 77)

    def _standardise_units(self, i):
        # Method called inside convert_product_weights to standardise all weight values to being of the same unit (kg)
        self.df.loc[i, 'weight'] = float(self.df.loc[i, 'weight'])
        if self.df.loc[i, 'unit'] == 'g' or self.df.loc[i, 'unit'] == 'ml':
            self.df.loc[i, 'weight'] = self.df.loc[i, 'weight'] / 1000
        if self.df.loc[i, 'unit'] == 'oz':
            self.df.loc[i, 'weight'] = self.df.loc[i, 'weight'] / 35.274

    def convert_product_weights(self):
        # create empty unit column
        self.df['unit'] = pd.NA
        # remove all invalid data by checking against categorised columns
        removed = ['Still_avaliable', 'Removed']
        self._categorise(removed, 'removed')

        # loop through the table assigning each weight unit to unit column   
        for i, row in self.df.iterrows():
            weight_str = self._fill_unit_column(i, row)
            # deal with multipacks
            if 'x' in weight_str:
                weight_str = weight_str.replace('x', '*').replace(' ', '').replace('g', '')
                self.df.loc[i, 'weight'] = eval(weight_str)
            # remove line 1781 error
            self.df.loc[1779, 'weight'] = 77
            self._standardise_units(i)

        self.df = self.df.drop(columns=['unit'])

        print(self.df.to_string())

    def clean_orders_data(self):
        self.df = self.df.drop(columns=['first_name', 'last_name', '1', 'level_0', 'index'])
    
    def clean_date_data(self):
        time_periods = ['Midday', 'Late_Hours', 'Evening', 'Morning']
        self.categorise(time_periods, 'time_period')




