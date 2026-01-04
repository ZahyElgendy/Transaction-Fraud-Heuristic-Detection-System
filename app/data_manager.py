import pandas as pd

class DataManager:
    
    def __init__(self):
        self.df = None #Attribute to hold the dataframe
        
    def load_dataset(self, file_path1, file_path2=None): #Load given CSV
        print("\n--- LOADING STARTED ---\n")
        try:
            print(f"Loading {file_path1}")
            df1 = pd.read_csv(file_path1)
            print(f"Loaded {len(df1)} rows")
            
            if file_path2: # if two files, combine them
                print(f"Loading {file_path2}")
                df2 = pd.read_csv(file_path2)
                print(f"Loaded {len(df2)} rows")
                
                self.df = pd.concat([df1, df2])
                self.df = self.df.reset_index(drop=True) #to restart indexing and drop old index
                print(f"Concatenated total: {len(self.df)} rows")
                print("\n--- LOADING FINISHED ---\n")
            else:
                self.df = df1
                

            return True
        except Exception as e:
            print(f"Loading file failed: {e}")
            return False
    
    def get_dataframe(self):
        return self.df

