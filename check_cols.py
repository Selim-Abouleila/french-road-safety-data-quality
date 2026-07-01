import pandas as pd
import os

files = ['caract-2024.csv', 'lieux-2024.csv', 'usagers-2024.csv', 'vehicules-2024.csv']
for f in files:
    print(f"--- {f} ---")
    try:
        df = pd.read_csv(f, sep=';', nrows=10)
        print("Data Types (first 10 rows to infer):")
        print(df.dtypes)
    except Exception as e:
        print(f"Failed to read with sep=';', trying ',': {e}")
        try:
            df = pd.read_csv(f, sep=',', nrows=10)
            print("Data Types (first 10 rows to infer):")
            print(df.dtypes)
        except Exception as e2:
            print(f"Failed to read with sep=',': {e2}")
    print("\n")
