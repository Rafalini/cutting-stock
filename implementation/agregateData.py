import os
import pandas as pd

filelist = ["effi_extend.csv", "effi_no_ext.csv", "time_extend.csv", "time_no_ext.csv"]
tmp_dir = "tmp_data"
out_dir = "out5"

os.makedirs(out_dir, exist_ok=True)

def merge_csv_files(directory_list, file):
    dfs = []

    for directory in directory_list:
        if os.path.exists(os.path.join(tmp_dir, directory)):
            file_path = os.path.join(tmp_dir, directory, file)
            df = pd.read_csv(file_path)
            dfs.append(df)
        else:
            print(f"Directory '{directory}' does not exist.")
    merged_df = pd.concat(dfs, ignore_index=True)

    merged_df = merged_df.drop(columns=['Unnamed: 0'])
    return merged_df.sort_values(by='true')

directory_list = os.listdir(tmp_dir)

for file in filelist:
    merged_csv = merge_csv_files(directory_list, file)
    merged_csv.to_csv(os.path.join(out_dir,file), index=False)