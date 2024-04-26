#!/usr/bin/env python3.9

import sys
import shutil
import os
import pandas as pd
import seaborn as sns
import pdfkit
import datetime
import pytz

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

scatter_location = f'{dest}/scatter.png'
scatter = relplot(df_melt, "cell_type", "cell_distribution", "subject", "scatter", subject_hue_order)
rotateXaxis(scatter, 90).savefig(scatter_location)

t_cell_scatter_location = f'{dest}/tcell_scatter.png'
tcell_scatter = relplot(data, "T cell", "T cell CD4", "subject", "scatter", subject_hue_order)
rotateXaxis(tcell_scatter, 90).savefig(t_cell_scatter_location)

raw_tcell_scatter = relplot(data, "T cell", "T cell CD4", "file", "scatter", hue_order)
rotateXaxis(raw_tcell_scatter, 90).savefig(f'{dest}/raw_tcell_scatter.png')

# create report - pdfkit
banner = "/service/I3H_Logo_HiRes.jpg"
eastern = pytz.timezone('US/Eastern')
dt = datetime.datetime.now(eastern)
generated = dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')
body = """
    <html>
      <head>
        <meta name="pdfkit-page-size" content="A4"/>
        <meta name="pdfkit-orientation" content="Portrait"/>
      </head>
      <header>
      <img src="{banner}" width="500px">
      </header>
      <body>
      <hr style="width:100%;text-align:left;margin-left:0">
      <div><i>Report Generated : {generated}<i></div>
      <br>
      <table style="border-collapse: collapse;">
        <tr>
        <th></th>
        <th></th>
        </tr>
        <tr>
            <td><b>Cell populations plotted against their frequencies<b></td><td><img src="{scatter_location}"></td>
        </tr>
        <tr>
            <td><b>T cell CD4 plotted against total T cells<b></td><td><img src="{t_cell_scatter_location}"></td>
        </tr>
      </table>
      </body>
      <br>
      <footer><center>421 Curie Blvd. Philadelphia, PA 19104</center></footer>
      </html>
    """.format(banner=banner, generated=generated, scatter_location=scatter_location, t_cell_scatter_location=t_cell_scatter_location)

options = {"enable-local-file-access": ""}
pdfkit.from_string(body, f'{dest}/ih-report.pdf', options=options)

print("end of processing")
