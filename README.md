# arktrack - ETF Tracker
## ARK Investment Tracker
Populates ETF Holding and loads the Price data from IEX/Polygon.

## Timescale DB on Docker

Docker Timescale DB install + run
```
docker run -d --name timescaledb -p 5432:5432 -e POSTGRES_PASSWORD=password timescale/timescaledb:latest-pg14
```

Show Running Conatiners
```
docker ps
```
Get the bash
```
docker exec -it <CONTAINER_ID> /bin/bash
```

## JupyterNotebook on Docker
```
ARG BASE_CONTAINER=jupyter/minimal-notebook
FROM $BASE_CONTAINER
LABEL author="SwapnilT"
USER root
RUN pip install pandas numpy matplotlib plotly scipy aiohttp requests
# Switch back to jovyan to avoid accidental container runs as root
USER $NB_UID
```


Links:
https://github.com/hackingthemarkets/timescaledb-aiohttp-asyncpg 
