FROM rocker/r-ver:4.4.0

WORKDIR /service

RUN apt clean && apt-get update

RUN apt-get -y install wkhtmltopdf

# R program dependencies
RUN apt-get install -y libudunits2-dev && apt-get install -y libgeos-dev && apt-get install -y libproj-dev && apt-get -y install libnlopt-dev && apt-get -y install pkg-config && apt-get -y install gdal-bin && apt-get install -y libgdal-dev
RUN apt-get -y install libcurl4-openssl-dev libfontconfig1-dev libxml2-dev libharfbuzz-dev libfribidi-dev libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev
RUN apt-get -y install glpk-utils libglpk-dev glpk-doc

RUN R --version

## Add additional program specific dependencies below ...
# tidyverse and its prerequisites
RUN Rscript -e "install.packages(c('BH'), Ncpus = 10, repos = 'https://cloud.r-project.org/', dependencies = TRUE)"
RUN Rscript -e "install.packages(c('tidyverse'), Ncpus = 10, dependencies=TRUE)"
RUN Rscript -e "library(tidyverse)" # sanity check

RUN Rscript -e "install.packages('Matrix', type = 'source')"
RUN Rscript -e "install.packages('irlba', type = 'source')"

# various dependencies
RUN Rscript -e "install.packages(c('uwot', 'RColorBrewer', 'glmnet'), Ncpus = 10, dependencies=TRUE)"
RUN Rscript -e "install.packages(c('Rcpp'), Ncpus = 10, dependencies=TRUE)"

RUN Rscript -e "install.packages(c('plyr'), Ncpus = 10, dependencies=TRUE)"

RUN mkdir -p data

COPY . .

# Add additional dependencies below ...
RUN apt-get -y install python3-pip
RUN pip3 --version
RUN pip3 install -r /service/requirements.txt
RUN python3.10 --version

RUN ls /service

CMD [ "python3.10", "/service/main.py" ]