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

# print(list(sorted_data))
# print(sorted_data.head())
sns.set_theme()

hue_order = sorted_data['file'].to_list()
subject_hue_order = sorted_data['subject'].to_list()

df_melt = pd.melt(sorted_data, id_vars=['file', 'subject'], var_name='cell_type', value_name='cell_distribution')
print(df_melt)
tcell_sorted_data = sorted_data[["file","T cell","T cell CD4", "subject"]]
df_melt_tcell = pd.melt(tcell_sorted_data, id_vars=['file', 'subject'], var_name='cell_type', value_name='cell_distribution')
print(df_melt_tcell)

# plots
r = sns.relplot(data=df_melt, x="cell_type", y="cell_distribution", hue="file", kind="scatter", hue_order=hue_order)
for axes in r.axes.flat:
    _ = axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
r.savefig(f'{dest}/raw_scatter.png')

g = sns.relplot(data=df_melt, x="cell_type", y="cell_distribution", hue="subject", kind="scatter", hue_order=subject_hue_order)
for axes in g.axes.flat:
    _ = axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
g.savefig(f'{dest}/scatter.png')

v = sns.relplot(data=tcell_sorted_data, x="T cell", y="T cell CD4", hue="subject", kind="scatter", hue_order=subject_hue_order)
for axes in v.axes.flat:
    _ = axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
v.savefig(f'{dest}/tcell_scatter.png')

print("end of processing")

