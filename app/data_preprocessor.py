import pandas as pd

class DataPreprocessor:
    def __init__(self, df):
        self.df = df.copy()
    
    def drop_unnamed_column(self):
        self.df.drop(columns=['Unnamed: 0'], inplace=True) #modify directly
        return self.df

    def remove_duplicates(self):
        before = len(self.df)
        self.df.drop_duplicates(inplace=True)
        after = len(self.df)
        print("Removed duplicates:", (before - after)) #No. of duplicates removed
        return self.df
    
    def convert_datetime(self):
        print("Fixing date formats")
        self.df['trans_date_trans_time'] = pd.to_datetime(self.df['trans_date_trans_time']) #convert trans time to datetime type
        self.df['dob'] = pd.to_datetime(self.df['dob'])  #convert dob to datetime type
        return self.df
    
    def extract_time_features(self):
        print("Extracting hour and day") # extract hour, day, month from the date column
        self.df['trans_hour'] = self.df['trans_date_trans_time'].dt.hour
        self.df['trans_day'] = self.df['trans_date_trans_time'].dt.day
        self.df['trans_month_year'] = self.df['trans_date_trans_time'].dt.to_period('M')
        return self.df
    
    def calculate_age(self):
        print("Calculating age")
        diff = self.df['trans_date_trans_time'] - self.df['dob']
        self.df['age'] = diff.dt.days // 365
        return self.df
    
    def drop_unnecessary_columns(self):
        print("Cleaning unneeded columns")
        bad_cols = ['dob', 'first', 'last', 'street', 'trans_num', 'unix_time']
        
        for c in bad_cols:
            self.df = self.df.drop(columns=[c])
        
        return self.df
    
    def clean_all(self):
        print("\n--- PREPROCESSING STARTED ---\n")
        self.drop_unnamed_column()
        self.remove_duplicates()
        self.convert_datetime()
        self.extract_time_features()
        self.calculate_age()
        self.drop_unnecessary_columns()
        print(f"Final size:{self.df.shape}")
        print("\n--- PREPROCESSING FINISHED ---\n")
        return self.df

