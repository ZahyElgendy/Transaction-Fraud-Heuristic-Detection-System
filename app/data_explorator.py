class DataExplorator:
    
    def __init__(self, df):
        self.df = df
    
    def show_info(self):
        print(f"\nDataset Size:{self.df.shape}")
        print(f"\nColumn names: \n{self.df.columns.tolist()}")
    
    def show_head(self, n=5):
        print(f"\nFirst {n} rows:")
        print(self.df.head(n))

    def check_missing(self):
        missing = self.df.isnull().sum()
        print(f"\nTotal missing values: {missing.sum()}")

    def show_types(self):
        print(f"\nData Types:\n{self.df.dtypes}")

    def show_stats(self):
        print(f"\nNumerical Stats:\n{self.df.describe()}")
        print("\nTotal customers:", self.df["cc_num"].nunique(), "unique values")

    def show_categories(self):
        print("\nCategorical Columns:")
        for col in self.df.columns:
            if self.df[col].dtype == "object":
                print(col + ":", self.df[col].nunique(), "unique values")
        
    def explore_all(self):
        print("\n--- EXPLORATION STARTED ---")
        self.show_info()
        self.show_head()
        self.check_missing()
        self.show_types()
        self.show_stats()
        self.show_categories()
        print("\n--- EXPLORATION FINISHED ---")
