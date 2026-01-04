from matplotlib.pylab import choice
from data_manager import DataManager
from data_explorator import DataExplorator
from data_preprocessor import DataPreprocessor
from data_visualizer import DataVisualizer 
from feature_engineer import FeatureEngineer
from risk_scorer_customer import RiskScorer
from transaction_flagger import TransactionFlagger  
from report_generator import ReportGenerator

def main():
    raw_data = None
    clean_data = None
    customer_profiles = None  
    scored_profiles = None   
    flagged_df = None        

    dm = DataManager()

    while True:
        print("\n   MAIN MENU   ")
        print("="*40)
        print("1. Load CSV files")
        print("2. Run Data exploration")
        print("3. Preprocess and Clean Data")
        print("4. Visualizations")
        print("5. Feature engineering")
        print("6. Customer risk scoring")
        print("7. Transaction fraud flagging")
        print("8. Final Report & Export")
        print("0. Exit")
        
        user_input = input("\nChoose an option: ")

        if user_input == '1':
            path1 = "Data/fraudTrain.csv"
            path2 = "Data/fraudTest.csv"
            res = dm.load_dataset(path1, path2)
            if res:
                raw_data = dm.get_dataframe()
            
        elif user_input == '2':
            if raw_data is not None:
                exp = DataExplorator(raw_data)
                exp.explore_all()
            else:
                print("Please load data first!")

        elif user_input == '3':
            if raw_data is not None:
                cln = DataPreprocessor(raw_data)
                clean_data = cln.clean_all()
            else:
                print("No data to clean!")

        elif user_input == '4':
            if clean_data is not None:
                viz = DataVisualizer(clean_data)
                viz.visualize_all()
            else:
                print("Clean data first please")

        elif user_input == '5':
            if clean_data is not None:
                fe = FeatureEngineer(clean_data)
                customer_profiles = fe.build_all_features(rolling_window=7)
            else:
                print("Clean data first")

        elif user_input == '6':
            if customer_profiles is not None:
                scorer = RiskScorer(customer_profiles)
                scorer.calculate_risk_scores()
                scored_profiles = scorer.assign_risk_bands() 
            else:
                print("Please run Feature Engineering (Option 5) first.")

        elif user_input == '7':
            if clean_data is not None and scored_profiles is not None:
                flagger = TransactionFlagger(clean_data, scored_profiles)
                flagger.flag_suspicious_activity()
                flagger.calculate_performance()
                flagged_df = flagger.get_flagged_data()
            else:
                print("Please run Risk Scoring (Option 6) first.")

        elif user_input == '8':
            if flagged_df is not None and scored_profiles is not None:
                reporter = ReportGenerator(flagged_df, scored_profiles)
                reporter.export_report_to_txt()
            else:
                print("\nPlease run steps Risk Scoring (Option 6), Transaction flagging (Option 7) first to export the data.")

        elif user_input == '0':
            print("Exit program.")
            break
        
        else:
            print("Wrong option, try again.")

        input("\nPress Enter to return to menu ")

if __name__ == "__main__":
    main()