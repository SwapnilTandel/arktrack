# Container for Jupyter
ARG BASE_CONTAINER=jupyter/minimal-notebook
FROM $BASE_CONTAINER
LABEL author="SwapnilT"
USER root
RUN pip install pandas numpy matplotlib plotly scipy aiohttp requests
# Switch back to jovyan to avoid accidental container runs as root
USER $NB_UID
