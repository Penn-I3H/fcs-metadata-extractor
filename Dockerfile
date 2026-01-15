FROM rocker/r-ver:4.4.0

WORKDIR /service

RUN apt clean && apt-get update && apt-get -y install alien

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
RUN Rscript -e "install.packages('plyr', repos='https://cloud.r-project.org')"

# flowCore and its prerequisites
RUN Rscript -e "install.packages(c('BiocManager'), Ncpus=10)"
RUN Rscript -e "BiocManager::install('RProtoBufLib')"
RUN Rscript -e "BiocManager::install(version = '3.19', ask=FALSE)"
RUN Rscript -e "BiocManager::install('cytolib', verbose=TRUE)"
RUN Rscript -e "library(cytolib)" # sanity check
RUN Rscript -e "BiocManager::install('flowCore')"

RUN mkdir -p data

COPY . .

RUN ls /service

ENTRYPOINT [ "Rscript", "/service/main.R" ]
