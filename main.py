#!/usr/bin/env python3.9

import sys
import shutil
import os
import pandas as pd
import seaborn as sns
import pdfkit
import datetime
import tempfile

def extractSubject(file):
    val = file.find('.')
    if val == -1:
        return file
    return file.split('.')[0]

def rotateXaxis(v, rotation):
    for axes in v.axes.flat:
        _ = axes.tick_params(axis='x', labelrotation = rotation)

    return v

def relplot(data, x_axis, y_axis, hue, kind, hue_order):
    return sns.relplot(data=data, x=x_axis, y=y_axis, hue=hue, kind=kind, hue_order=hue_order)

print("start of processing")

src = os.environ['INPUT_DIR']
dest = os.environ['OUTPUT_DIR']

source_files = os.listdir(src)
print("source files: ", source_files)
dataframes = []
for filename in source_files:
    df = pd.read_csv(f'{src}/{filename}')
    df['subject'] = extractSubject(df["file"].squeeze())
    dataframes.append(df)
data = pd.concat(dataframes, axis=0)

sorted_data = data.sort_values("file")
sorted_data.to_csv(f'{dest}/merged_results.csv')

sns.set_theme(style="white")

hue_order = sorted_data['file'].to_list()
subject_hue_order = sorted_data['subject'].to_list()

df_melt = pd.melt(sorted_data, id_vars=['file', 'subject'], var_name='cell_type', value_name='cell_distribution')
print(df_melt)
tcell_sorted_data = sorted_data[["file","T cell","T cell CD4", "subject"]]
df_melt_tcell = pd.melt(tcell_sorted_data, id_vars=['file', 'subject'], var_name='cell_type', value_name='cell_distribution')
print(df_melt_tcell)

# plots
raw_scatter = relplot(df_melt, "cell_type", "cell_distribution", "file", "scatter", hue_order)
rotateXaxis(raw_scatter, 90).savefig(f'{dest}/raw_scatter.png')

scatter = relplot(df_melt, "cell_type", "cell_distribution", "subject", "scatter", subject_hue_order)
rotateXaxis(scatter, 90).savefig(f'{dest}/scatter.png')

tcell_scatter = relplot(data, "T cell", "T cell CD4", "subject", "scatter", subject_hue_order)
rotateXaxis(tcell_scatter, 90).savefig(f'{dest}/tcell_scatter.png')

raw_tcell_scatter = relplot(data, "T cell", "T cell CD4", "file", "scatter", hue_order)
rotateXaxis(raw_tcell_scatter, 90).savefig(f'{dest}/raw_tcell_scatter.png')

# create report - pdfkit
# pdfkit.from_url('http://google.com', f'{dest}/ih-report2.pdf')
header = f'/service/I3H_Logo_HiRes.jpg'
generated = datetime.datetime.now()
body = """
    <html>
      <head>
        <meta name="pdfkit-page-size" content="A4"/>
        <meta name="pdfkit-orientation" content="Portrait"/>
      </head>
      <header>
      <img src="{header}" width="500px">
      </header>
      <hr style="width:100%;text-align:left;margin-left:0">
      <div><i>Report Generation Date : {generated}<i></div>
      </html>
    """.format(header=header, generated=generated)

with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as temp:
    temp.write(b'<!DOCTYPE html><html><body>421 Curie Blvd. Philadelphia, PA 19104</body></html>')
    temp.seek(0)

options = {"enable-local-file-access": "", 'footer-html': temp.name}
pdfkit.from_string(body, f'{dest}/ih-report2.pdf', options=options)

print("end of processing")
