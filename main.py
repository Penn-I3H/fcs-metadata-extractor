import sys
import shutil
import os
import pdfkit
import datetime
import pytz
import subprocess

# try:
#     output = subprocess.run(["Rscript", "/service/R/main.R"]) 
# except subprocess.CalledProcessError as e:
#     print(f"command failed with return code {e.returncode}")

print("Generating report ...")

dest = os.environ['OUTPUT_DIR']    

# create report - pdfkit
banner = "/service/I3H_Logo_HiRes.jpg"
eastern = pytz.timezone('US/Eastern')
dt = datetime.datetime.now(eastern)
generated = dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')

boxplot_location = f'{dest}/boxplots.png'
cleanup_location = f'{dest}/cleanup.png'
lasso_location = f'{dest}/lasso.png'
umap_location = f'{dest}/umap.png'

# QC All
qc_summary_all = f'{dest}/QC_all/qc_summary.png'
qc_univariate_B_all = f'{dest}/QC_all/qc_univariate_B cell.png'
qc_univariate_Neutrophil_all = f'{dest}/QC_all/qc_univariate_Neutrophil.png'
qc_univariate_T_CD4_all = f'{dest}/QC_all/qc_univariate_T cell CD4.png'
qc_univariate_T_CD8_all = f'{dest}/QC_all/qc_univariate_T cell CD8.png'
# QC Controls
qc_summary_controls = f'{dest}/QC_controls/qc_summary.png'
qc_univariate_B_controls = f'{dest}/QC_controls/qc_univariate_B cell.png'
qc_univariate_Neutrophil_controls = f'{dest}/QC_controls/qc_univariate_Neutrophil.png'
qc_univariate_T_CD4_controls = f'{dest}/QC_controls/qc_univariate_T cell CD4.png'
qc_univariate_T_CD8_controls = f'{dest}/QC_controls/qc_univariate_T cell CD8.png'

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
      This report was generated using the "Automated CyTOF Data workflow" on the Pennsieve Platform. For more information about the results, please contact the Immune Health Data Core (Matei Ionita).
      </p>
      
      <table style="border-collapse: collapse;">
        <tr>
        <th></th>
        <th></th>
        </tr>

        <tr>
            <td><b>1. Cleanup<b></td>
        </tr>
        <tr>
        <td>Graphing CD4 T-cell populations against total T-Cell populations across all included subjects.</td>
        </tr>
        <tr style='padding-bottom:50px'>
            <td style='text-align:center; vertical-align:middle'><img width="900px" src="{cleanup_location}"></td>
        </tr>

        <tr>
            <td><b>2. QC All<b></td>
        </tr>
        <tr>
        <td>Graphing CD4 T-cell populations against total T-Cell populations across all included subjects.</td>
        </tr>
        <tr style='padding-bottom:50px'>
            <td style='text-align:center; vertical-align:middle'><img width="900px" src="{qc_summary_all}"></td>
        </tr>
            <tr style='padding-bottom:50px'>
            <td style='text-align:center; vertical-align:middle'><img width="900px" src="{qc_univariate_B_all}"></td>
        </tr>
        <tr style='padding-bottom:50px'>
            <td style='text-align:center; vertical-align:middle'><img width="900px" src="{qc_univariate_Neutrophil_all}"></td>
        </tr>
        <tr style='padding-bottom:50px'>
            <td style='text-align:center; vertical-align:middle'><img width="900px" src="{qc_univariate_T_CD4_all}"></td>
        </tr>
        <tr style='padding-bottom:50px'>
            <td style='text-align:center; vertical-align:middle'><img width="900px" src="{qc_univariate_T_CD8_all}"></td>
        </tr>

        <tr>
            <td><b>3. QC Controls<b></td>
        </tr>
        <tr>
        <td>Graphing CD4 T-cell populations against total T-Cell populations across all included subjects.</td>
        </tr>
        <tr style='padding-bottom:50px'>
            <td style='text-align:center; vertical-align:middle'><img width="900px" src="{qc_summary_controls}"></td>
        </tr>
            <tr style='padding-bottom:50px'>
            <td style='text-align:center; vertical-align:middle'><img width="900px" src="{qc_univariate_B_controls}"></td>
        </tr>
        <tr style='padding-bottom:50px'>
            <td style='text-align:center; vertical-align:middle'><img width="900px" src="{qc_univariate_Neutrophil_controls}"></td>
        </tr>
        <tr style='padding-bottom:50px'>
            <td style='text-align:center; vertical-align:middle'><img width="900px" src="{qc_univariate_T_CD4_controls}"></td>
        </tr>
        <tr style='padding-bottom:50px'>
            <td style='text-align:center; vertical-align:middle'><img width="900px" src="{qc_univariate_T_CD8_controls}"></td>
        </tr>

        <tr>
            <td><b>4. Boxplots<b></td>
        </tr>
        <tr>
        <td>Cell classification across across all included subjects. Only selected classifications are included in this graph.</td>
        </tr>
        <tr style='padding-bottom:50px'>
        <td style='text-align:center; vertical-align:middle'><img width="900px" src="{boxplot_location}"></td>
        </tr>

        <tr>
            <td><b>5. Lasso<b></td>
        </tr>
        <tr>
        <td>Cell classification across across all included subjects. Only selected classifications are included in this graph.</td>
        </tr>
        <tr style='padding-bottom:50px'>
        <td style='text-align:center; vertical-align:middle'><img width="900px" src="{lasso_location}"></td>
        </tr>


        <tr>
            <td><b>6. Umap<b></td>
        </tr>
        <tr>
        <td>Cell classification across across all included subjects. Only selected classifications are included in this graph.</td>
        </tr>
        <tr style='padding-bottom:50px'>
        <td style='text-align:center; vertical-align:middle'><img width="900px" src="{umap_location}"></td>
        </tr>

      </table>
      </body>
      <br>
      <footer><center>421 Curie Blvd. Philadelphia, PA 19104</center></footer>
      </html>
    """.format(banner=banner, generated=generated, boxplot_location=boxplot_location, cleanup_location=cleanup_location, lasso_location=lasso_location, umap_location=umap_location,
               qc_summary_all=qc_summary_all, qc_univariate_B_all=qc_univariate_B_all, qc_univariate_Neutrophil_all=qc_univariate_Neutrophil_all, qc_univariate_T_CD4_all=qc_univariate_T_CD4_all, qc_univariate_T_CD8_all=qc_univariate_T_CD8_all,
               qc_summary_controls=qc_summary_controls, qc_univariate_B_controls=qc_univariate_B_controls, qc_univariate_Neutrophil_controls=qc_univariate_Neutrophil_controls, qc_univariate_T_CD4_controls=qc_univariate_T_CD4_controls, qc_univariate_T_CD8_controls=qc_univariate_T_CD8_controls)

options = {"enable-local-file-access": ""}
pdfkit.from_string(body, f'{dest}/ih-report.pdf', options=options)

print("Report generation complete.")
