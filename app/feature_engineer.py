import pandas as pd
import numpy as np

class FeatureEngineer:
    def __init__(self, df):
        self.df = df.copy()
        self.customer_profiles = pd.DataFrame() # Dataframe to store each customer features

    def aggregate_spending(self):
        print("Aggregating spending statistics per card")
        self.customer_profiles = self.df.groupby('cc_num').agg(
            total_spending=('amt', 'sum'),
            avg_transaction=('amt', 'mean'),
            max_transaction=('amt', 'max'),
            total_trans_count=('amt', 'count')
        ).reset_index()
        return self.customer_profiles


    def calculate_velocity(self):
        print("Calculating velocity")
        
        self.df['t_date'] = self.df['trans_date_trans_time'].dt.date
        active_days = self.df.groupby('cc_num')['t_date'].nunique() # count days of transaction
        
        self.customer_profiles['days_active'] = self.customer_profiles['cc_num'].map(active_days)
        # divide count by days
        self.customer_profiles['daily_velocity'] = (self.customer_profiles['total_trans_count'] / self.customer_profiles['days_active'])
        return self.customer_profiles

    def calculate_rolling_stats(self, window=5): # window is size of transactions
            print(f"Calculating rolling statistics")
            
            # Sort by date
            temp_df = self.df.sort_values(['cc_num', 'trans_date_trans_time'])
            
            temp_df[f'rolling_avg_{window}'] = temp_df.groupby('cc_num')['amt'].rolling(window=window, min_periods=1).mean().reset_index(level=0, drop=True)
            
            latest_rolling = temp_df.groupby('cc_num')[f'rolling_avg_{window}'].last()
            self.customer_profiles['recent_spending_trend'] = self.customer_profiles['cc_num'].map(latest_rolling)
            
            return self.customer_profiles

    def calculate_behavioral_patterns(self):
            print("Extracting behavioral patterns")
            
            # Find the  mode category for each person
            most_freq_cat = self.df.groupby('cc_num')['category'].agg(lambda x: pd.Series.mode(x)[0])
            self.customer_profiles['most_freq_category'] = self.customer_profiles['cc_num'].map(most_freq_cat)
            
            # Finding the most frequent hour for each person
            most_freq_hour = self.df.groupby('cc_num')['trans_hour'].agg(lambda x: pd.Series.mode(x)[0])
            self.customer_profiles['customer_peak_hour'] = self.customer_profiles['cc_num'].map(most_freq_hour)
            
            return self.customer_profiles


    def build_all_features(self, rolling_window=5):
        print("\n--- FEATURE ENGINEERING STARTED ---\n")        
        self.aggregate_spending()
        self.calculate_velocity()
        self.calculate_rolling_stats(window=rolling_window) 
        self.calculate_behavioral_patterns() 
        
        print("\nFeatures built for", len(self.customer_profiles), "cards: ")
        print(self.customer_profiles.head())
        print("\n--- FEATURE ENGINEERING FINISHED ---\n")
        return self.customer_profiles    