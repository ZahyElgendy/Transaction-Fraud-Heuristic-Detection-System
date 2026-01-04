import pandas as pd
import numpy as np

class TransactionFlagger:
    def __init__(self, original_df, scored_profiles):
        self.df = original_df.copy()
        self.profiles = scored_profiles
        self.results_df = None

    def flag_suspicious_activity(self):
        
        # add risk and avg transaction to main df
        risk_map = self.profiles.set_index('cc_num')['risk_band']
        self.df['risk_level'] = self.df['cc_num'].map(risk_map)
        
        avg_map = self.profiles.set_index('cc_num')['avg_transaction']
        self.df['cust_avg'] = self.df['cc_num'].map(avg_map)

        # Transaction flagging conditions
        danger_cats = ['shopping_net', 'grocery_pos', 'misc_net']
        
        cond1 = self.df['category'].isin(danger_cats)
        cond2 = (self.df['amt'] >= 200) 
        cond3 = (self.df['trans_hour'] >= 23) | (self.df['trans_hour'] <= 4)
        cond4 = self.df['amt'] > (self.df['cust_avg'] * 3)
        cond5 = (self.df['risk_level'] == 'Critical')

        # default not flagged
        self.df['is_flagged'] = 0
        
        # flag if:
        fraud = (cond1 & cond2) | (cond3 & cond2) | (cond4 & cond2) | cond5

        self.df['is_flagged'] = np.where(fraud, 1, 0)

        self.results_df = self.df

        self.df.to_csv("flagged_transactions.csv", index=False)

        return self.results_df

    def calculate_performance(self):
        # Calculate metrics

        n_total = len(self.df)
        total_fraud = self.df['is_fraud'].sum()
        true_pos = ((self.df['is_flagged'] == 1) & (self.df['is_fraud'] == 1)).sum()
        false_pos = ((self.df['is_flagged'] == 1) & (self.df['is_fraud'] == 0)).sum()
        false_neg = ((self.df['is_flagged'] == 0) & (self.df['is_fraud'] == 1)).sum()
        
        # calculate recall
        rec_val = (true_pos / total_fraud) * 100

        print("\n--- FLAGGING TRANSACTIONS STARTED ---")
        
        print("\nTop fraud categories ")
        # fraud rows for each categories
        f_rows = self.df[self.df['is_flagged'] == 1]
        print(f_rows['category'].value_counts().head(5))
        
        print("\nPerformance:")
        print(f"Total rows:{n_total}")        
        print(f"Actual fraud (total fraud):{total_fraud}")
        print(f"Caught fraud (true positives):{true_pos}")
        print(f"Missed cases (false negatives):{false_neg}")
        print(f"False alarms (true positives):{false_pos}")
        print(f"Detection Rate(recall): {rec_val:.2f}%")

        # amount saved from blocked transactions.
        savings_data = self.df[(self.df['is_flagged'] == 1) & (self.df['is_fraud'] == 1)]
        total_money = savings_data['amt'].sum()
        print(f"Money saved from blocked frauds: ${total_money:.2f}")

        print("\n--- FLAGGING TRANSACTIONS FINISHED ---")
        

    def get_flagged_data(self):
        return self.results_df