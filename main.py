#!/usr/bin/env python3.9

import sys
import shutil
import os
import pandas as pd
import seaborn as sns

def extractSubject(file):
    val = file.find('.')
    if val == -1:
        return file
    return file.split('.')[0]

print("start of processing")

src = os.environ['INPUT_DIR']
dest = os.environ['OUTPUT_DIR']

source_files = os.listdir(src)
print(source_files)
dataframes = []
for filename in source_files:
    df = pd.read_csv(f'{src}/{filename}')
    print(df["file"].squeeze())
    df['subject'] = extractSubject(df["file"].squeeze())
    dataframes.append(df)
data = pd.concat(dataframes, axis=0)

sorted_data = data.sort_values("file")
sorted_data.to_csv(f'{dest}/merged_results.csv')

# plot dotplot
print(list(sorted_data))
print(sorted_data.head())
sorted_data = sorted_data[["file","T cell","T cell CD4", "subject"]]
sns.set_theme()

hue_order = sorted_data['file'].to_list()
subject_hue_order = sorted_data['subject'].to_list()
df_melt = pd.melt(sorted_data, id_vars=['file', 'subject'], var_name='cell_type', value_name='cell_distribution')
print(df_melt)
sns.relplot(data=df_melt, x="cell_type", y="cell_distribution", hue="file", kind="scatter", hue_order=hue_order).savefig(f'{dest}/raw_scatter.png')

sns.relplot(data=df_melt, x="cell_type", y="cell_distribution", hue="subject", kind="scatter", hue_order=subject_hue_order).savefig(f'{dest}/scatter.png')

print("end of processing")

