import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class DataVisualizer:
    sns.set_theme(style="whitegrid") #class level

    def __init__(self, df):
        self.df = df.copy()
        self.df['is_fraud'] = self.df['is_fraud'].astype(int)

        self.save_dir = "outputs/images"

    def plot_fraud_distribution(self):
        print("Visualizing fraud distribution")
        f_counts = self.df['is_fraud'].value_counts()

        plt.figure(figsize=(7, 7))

        plt.pie(f_counts, labels=['Legit', 'Fraud'], autopct='%.1f%%', colors=['blue','red'])
        plt.title('Fraudulent vs Non-Fraudulent Transactions %')
        plt.savefig(f"{self.save_dir}/fraud_dist.png")
        plt.show()

    def plot_amount_dist(self):
        print("Visualizing amount distribution")
        plt.figure(figsize=(16, 6))
        
        # Non-fraud amount distribution
        plt.subplot(1, 2, 1)
        sns.histplot(self.df[self.df['is_fraud'] == 0]['amt'], bins=50, color='blue', kde=True)
        plt.title('Non-Fraud Transaction Amount Distribution')
        plt.xlabel('Amount (USD)')
        plt.xlim(0, 1000)

        # Fraud amount distribution
        plt.subplot(1, 2, 2)
        sns.histplot(self.df[self.df['is_fraud'] == 1]['amt'], bins=50, color='red', kde=True)
        plt.title('Fraud Transaction Amount Distribution')
        plt.xlabel('Amount (USD)')
        plt.xlim(0, 1500)
        
        plt.tight_layout()
        plt.savefig(f"{self.save_dir}/amount_histogram.png")
        plt.show()

    def plot_amount_box(self):
        print("Visualizing Amount Inferences")
        plt.figure(figsize=(10, 6))
        
        color_map = {0: 'blue', 1: 'red', '0': 'blue', '1': 'red'}
        
        sns.boxplot(data=self.df, x='is_fraud', y='amt', hue='is_fraud', palette=color_map, legend=False)
        
        plt.ylim(0, 1000) 
        plt.ylabel('Amount (USD)')
        plt.xlabel('Transaction status (0=Legit, 1=Fraud)')
        plt.title('Transaction amounts: Legit vs Fraud')
        plt.savefig(f"{self.save_dir}/amount_boxplot.png")
        plt.show()

    def plot_monthly_count(self):
        print("Visualizing Monthly Transaction Volume")
        monthly_data = self.df['trans_month_year'].astype(str)
        
        plt.figure(figsize=(12, 6))
        sns.countplot(x=monthly_data.sort_values(), palette='viridis')
        plt.title('Total Transactions per Month')
        plt.xticks(rotation=45) 
        plt.ylabel('Count')
        plt.savefig(f"{self.save_dir}/monthly_volume.png")
        plt.show()

    def plot_time_ratio(self):
        print("Visualizing Time Patterns")
        plt.figure(figsize=(12, 6))
        sns.countplot(data=self.df, x='trans_hour', hue='is_fraud', palette={0: 'blue', 1: 'red'})
        plt.yscale("log") # log scale for visibility
        plt.title('Hourly Transaction Patterns (Log Scale)')
        plt.savefig(f"{self.save_dir}/time_patterns.png")
        plt.show()
        

    def plot_age_fraud_ratio(self):
        print("Visualizing age risk ratios")
        bins = [0, 30, 45, 60, 75, 120]
        labels = ['<30', '30-45', '46-60', '61-75', '>75']
        
        temp = self.df.copy()
        temp['age_group'] = pd.cut(temp['age'], bins=bins, labels=labels)
        
        res = temp.groupby('age_group')['is_fraud'].mean() * 100
        
        plt.figure(figsize=(10, 6))
        res.plot(kind='bar', color='red')
        plt.title('Fraud Probability (%) by Age Group')
        plt.ylabel('Fraud Rate (%)')
        plt.savefig(f"{self.save_dir}/age_risk.png")
        plt.show()

    def plot_category_ratio(self):
        print("Visualizing category risk ratios")

        c_risk = self.df.groupby('category')['is_fraud'].mean() * 100
        c_risk = c_risk.sort_values(ascending=False)
        
        plt.figure(figsize=(12, 8))
        c_risk.plot(kind='barh', color='red')
        plt.xlim(0, 2.5)
        
        plt.title('Fraud Rate (%) by Category')
        plt.xlabel('Fraud Probability (%)')
        plt.savefig(f"{self.save_dir}/category_risk.png")
        plt.show()



    def visualize_all(self):
            while True:
                print("\n--- DATA VISUALIZATION MENU ---")
                print("1. Fraud vs legit distribution")
                print("2. Transaction amount risk visualization")
                print("3. Time risk visualizations (hours & months)")
                print("4. Age risk visualization")
                print("5. Category risk visualization")
                print("0. Back to main menu")
                
                choice = input("\nSelect visualization type: ")
                
                if choice == '1':
                    self.plot_fraud_distribution()
                elif choice == '2':
                    self.plot_amount_dist()
                    self.plot_amount_box()
                elif choice == '3':
                    self.plot_time_ratio()
                    self.plot_monthly_count()
                elif choice == '4':
                    self.plot_age_fraud_ratio()
                elif choice == '5':
                    self.plot_category_ratio()
                elif choice == '0':
                    break
                else:
                    print("Invalid choice")        