import sys
import shutil
import os
import pandas as pd
import seaborn as sns
import pdfkit
import datetime
import pytz

print("start of processing")

src = os.environ['INPUT_DIR']
dest = os.environ['OUTPUT_DIR']

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
      <img src="{banner}" width="300px">
      </header>
      <body>
      <hr style="width:100%;text-align:left;margin-left:0">
      <div><i>Report Generated : {generated}<i></div>
      <br>
      <p>
      This report was generated from the "Automatic CyTOF Data workflow on the Pennsieve Platform. For more information about the results, please contact the Immune Health Data Core (Matei Ionita)."
      </p>
      
      <table style="border-collapse: collapse;">
        <tr>
        <th></th>
        <th></th>
        </tr>
        <tr>
            <td><b>1. Cell populations plotted against their frequencies<b></td>
        </tr>
        <tr>
        <td>Cell classification across across all included subjects. Only selected classifications are included in this graph.</td>
        </tr>
        <tr style='padding-bottom:50px'>
        <td style='text-align:center; vertical-align:middle'><img width="450px"></td>
        </tr>
        <tr>
            <td><b>2. T cell CD4 plotted against total T cells<b></td>
        </tr>
        <tr>
        <td>Graphing CD4 T-cell populations against total T-Cell populations across all included subjects.</td>
        </tr>
        <tr style='padding-bottom:50px'>
            <td style='text-align:center; vertical-align:middle'><img width="450px"></td>
        </tr>
      </table>
      </body>
      <br>
      <footer><center>421 Curie Blvd. Philadelphia, PA 19104</center></footer>
      </html>
    """.format(banner=banner, generated=generated)

options = {"enable-local-file-access": ""}
pdfkit.from_string(body, f'{dest}/ih-report.pdf', options=options)

print("end of processing")
