import numpy as np

class RiskScorer:
    def __init__(self, customer_profiles):
        self.profiles = customer_profiles.copy()

    def calculate_risk_scores(self):
        print("\n--- SCORING STARTED ---\n")

        # Check high velocity using z-score
        v_mean = self.profiles['daily_velocity'].mean()
        v_std = self.profiles['daily_velocity'].std()
        self.profiles['vel_z'] = (self.profiles['daily_velocity'] - v_mean) / v_std
        self.profiles['vel_points'] = np.where(self.profiles['vel_z'] > 2.5, 25, 0) #weightage 25%

        # Check spending spike
        self.profiles['spike_ratio'] = self.profiles['recent_spending_trend'] / self.profiles['avg_transaction']
        self.profiles['spike_points'] = np.where(self.profiles['spike_ratio'] > 2.0, 30, 0) #weightage 30%

        # Check category and amount 
        danger_cats = ['shopping_net', 'grocery_pos', 'misc_net']
        is_danger_cat = self.profiles['most_freq_category'].isin(danger_cats)
        is_high_amt = self.profiles['max_transaction'] > 200
        
        self.profiles['amt_cat_points'] = np.where(is_danger_cat & is_high_amt, 25, 0) #weightage 25%

        # Nighttime check,  11 PM to 4 AM is  danger 
        hour = self.profiles['customer_peak_hour']
        night_condition = (hour >= 23) | (hour <= 4)
        self.profiles['night_points'] = np.where(night_condition, 20, 0) #weightage 20%

        # Sum total risk score
        self.profiles['total_risk_score'] = (
            self.profiles['vel_points'] + 
            self.profiles['spike_points'] + 
            self.profiles['amt_cat_points'] + 
            self.profiles['night_points']
        )
        return self.profiles

    
    def assign_risk_bands(self):
        print("Assigning risk bands")

        self.profiles['risk_band'] = 'Low' 
        self.profiles.loc[self.profiles['total_risk_score'] >= 30, 'risk_band'] = 'Medium'
        self.profiles.loc[self.profiles['total_risk_score'] >= 50, 'risk_band'] = 'High'
        self.profiles.loc[self.profiles['total_risk_score'] >= 70, 'risk_band'] = 'Critical'        

        print("\nRisk band distribution:")
        band_counts = self.profiles['risk_band'].value_counts()
        print(band_counts)

        print("\nSample of customer risk profiles:")
        print(self.profiles.head(5))

        self.profiles.to_csv("customer_risk_summary.csv", index=False)

        print("\n--- SCORING FINISHED ---")
        return self.profiles
