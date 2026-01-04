class ReportGenerator:
    def __init__(self, flagged_df, final_profiles):
        self.df = flagged_df
        self.profiles = final_profiles

    def export_report_to_txt(self):
        

        total_rows = len(self.df)
        total_fraud = self.df['is_fraud'].sum()
        true_pos = ((self.df['is_flagged'] == 1) & (self.df['is_fraud'] == 1)).sum()
        false_pos = ((self.df['is_flagged'] == 1) & (self.df['is_fraud'] == 0)).sum()
        false_neg = ((self.df['is_flagged'] == 0) & (self.df['is_fraud'] == 1)).sum()
        rec_val = (true_pos / total_fraud) * 100 if total_fraud > 0 else 0
        money_saved = self.df[(self.df['is_flagged'] == 1) & (self.df['is_fraud'] == 1)]['amt'].sum()

        with open("final_summary.txt", "w") as f:
            f.write("--- CUSTOMER RISK SCORING ---\n\n")
            f.write("Risk band distribution:\n")
            f.write(self.profiles['risk_band'].value_counts().to_string() + "\n")
            
            f.write("\n--- TRANSACTION FLAGGING PERFORMANCE ---\n")
            f.write(f"Total rows:      {total_rows}\n")
            f.write(f"Actual fraud (total fraud):    {total_fraud}\n")
            f.write(f"Caught fraud (true positives):    {true_pos}\n")
            f.write(f"Missed cases (false negatives):    {false_neg}\n")
            f.write(f"False alarms (true positives):    {false_pos}\n")
            f.write(f"Detection Rate(recall):  {rec_val:.2f}%\n")
            f.write(f"Money saved:     ${money_saved:,.2f}\n")
            
            f.write("\n--- TOP FLAGGED CATEGORIES ---\n")
            f_rows = self.df[self.df['is_flagged'] == 1]
            f.write(f_rows['category'].value_counts().head(5).to_string() + "\n")
            print("\n--- FINAL REPORT EXPORTED ---")
