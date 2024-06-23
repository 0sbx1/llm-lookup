import os
import pandas as pd

# Simple function to save a new csv file without overwriting (by iterating and appending a number at end)

def save_new_csv(file_path, merged_df):
    base_path = os.path.splitext(file_path)[0]
    counter = 1
    new_file_path = f'{base_path}_new.csv'

    while os.path.exists(new_file_path):
        new_file_path = f'{base_path}_new_{counter}.csv'
        counter += 1

    merged_df.to_csv(new_file_path, index=False)

    print(f"Saved CSV at: {new_file_path}")