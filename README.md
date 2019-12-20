# Lassaress
This project involves development and configuration of cloud-based data collection, analysis and visualization pipeline as well as mobile web application. See more details about the project [here!](http://nrig.renci.org/project/lassaress/)

## Analysis & Visualization Pipeline
Analysis and visualization pipeline is implemented via PostgreSQL/PostGIS and Openlayers/D3.js.

## Web Application
The web application backend uses the Django Rest Framework, accessible through a NGINX server, to serve data extracted from a PostgreSQL/PostGIS database. The web application frontend accesses and displays the data using Openlayers and D3.js, which are wrapped in a Vue/Quasar user interface. Openlayers also accesses OpenStreetMap and MapBox tile map services. The entire web application is packaged into containers using Docker, for easy transport to cloud services such as AWS. 

![Block-Diagram](../master/images/RENCIPropDiagram.png)

## Installtion
### Development mode on AWS
Lassaress web server can be hosted on AWS for development purposes by using the Cloud Formation file: pfiCloudFormation.json
User is prompted to provide following information:
- MBTOKEN - Map Box Token
- CLIENTID - Auth0 Client ID
- AUTH0DOMAIN - Auth0 Domain
- APIIDENTIFIER - Auth0 API Identifier
### Production mode on Vmware cluster
1. Clone the git repo as root user:
```
git clone https://github.com/RENCI-NRIG/lassares.git
cd /root/lassares
```
2. Run the start script
```
./start_django_project.sh [MBTOKEN] [CLIENTID] [AUTH0DOMAIN] [APIIDENTIFIER]
```
- MBTOKEN - Map Box Token
- CLIENTID - Auth0 Client ID
- AUTH0DOMAIN - Auth0 Domain
- APIIDENTIFIER - Auth0 API Identifier
