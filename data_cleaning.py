import pandas as pd

class DataClean:
    def clean_user_data(self, df):
        # remove invalid data
        self.df = df
        country_codes = ['DE', 'GB', 'US']
        correct_rows = self.df['country_code'].isin(country_codes)
        data_validated = self.df[correct_rows]
        
        # standardise datetimes
        data_validated.loc[:, 'date_of_birth'] = pd.to_datetime(data_validated.loc[:, 'date_of_birth'], infer_datetime_format=True)
        data_validated.loc[:, 'join_date'] = pd.to_datetime(data_validated.loc[:, 'join_date'], infer_datetime_format=True)

        return data_validated
    
    def clean_card_data(self, df):
       self.df = df
        # reset index
       df1 = self.df.reset_index(drop=True)
        # remove null and invalid data
       card_categories = ['JCB 15 digit', 'JCB 16 digit', 'VISA 13 digit', 'Diners Club / Carte Blanche', 'VISA 19 digit', 'American Express', 'Maestro', 'VISA 16 digit', 'Discover']
       correct_rows = df1['card_provider'].isin(card_categories)
       data_validated = df1[correct_rows]

       return data_validated

    def clean_store_data(self, data):
        self.data = data
        # remove 'lat' column
        df = self.data.drop(['lat'], axis=1)
        
        # line to print which staff_numbers aren't integers. 
        # have then used sql to correct those lines
        # print(df.loc[~df['staff_numbers'].str.isdigit(), 'staff_numbers'].tolist())

        # remove invalid rows
        country_codes = ['DE', 'GB', 'US']
        correct_rows = df['country_code'].isin(country_codes)
        df = df[correct_rows]

        # standardise opening_date
        df.loc[:, 'opening_date'] = pd.to_datetime(df.loc[:, 'opening_date'], infer_datetime_format=True)
        
        # remap continent errors
        mapping = {'eeEurope': 'Europe', 'eeAmerica': 'America'}
        df['continent'] = df['continent'].replace(mapping)

        return df
    
    def convert_product_weights(self, df):
        self.df = df
        self.df['unit'] = pd.NA

        # separate unit into separate column
        def unit_strip(unit, weight_str):
            self.df.loc[i, 'unit'] = unit
            weight_str = weight_str.replace(unit, '')
            self.df.loc[i, 'weight'] = weight_str

        for i, row in self.df.iterrows():
            weight_str = str(row['weight'])
            if 'kg' in weight_str:
               unit_strip('kg', weight_str=weight_str)
            elif 'g' in weight_str:
               unit_strip('g', weight_str=weight_str)
            elif 'ml' in weight_str:
               unit_strip('ml', weight_str=weight_str)
            elif 'oz' in weight_str:
               unit_strip('oz', weight_str=weight_str)

            # deal with multipacks
            if 'x' in weight_str:
                weight_str = weight_str.replace('x', '*').replace(' ', '').replace('g', '')
                self.df.loc[i, 'weight'] = eval(weight_str)
            
            # remove line 1781 error and all invalid data
            self.df.loc[1779, 'weight'] = 77

            removed = ['Still_avaliable', 'Removed']
            valid_rows = self.df['removed'].isin(removed)
            self.df = self.df[valid_rows]

        # standardise units to kg and remove unit column
        for i, row in self.df.iterrows():
            self.df.loc[i, 'weight'] = float(self.df.loc[i, 'weight'])
            if row['unit'] == 'g' or row['unit'] == 'ml':
                self.df.loc[i, 'weight'] = self.df.loc[i, 'weight'] / 1000
            if row['unit'] == 'oz':
                self.df.loc[i, 'weight'] = self.df.loc[i, 'weight'] / 35.274

        self.df = self.df.drop(columns=['unit'])

        return self.df

    def clean_orders_data(self, df):
        self.df = df
        self.df = self.df.drop(columns=['first_name', 'last_name', '1', 'level_0', 'index'])
        return self.df
    
    def clean_date_data(self, df):
        self.df = df
        time_periods = ['Midday', 'Late_Hours', 'Evening', 'Morning']
        valid_rows = self.df['time_period'].isin(time_periods)
        self.df = self.df[valid_rows]
        return self.df




