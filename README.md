# Lassaress
This project involves development and configuration of cloud-based data collection, analysis and visualization pipeline as well as mobile web application. See more details about the project [here!](http://nrig.renci.org/project/lassaress/)

## Analysis & Visualization Pipeline
Analysis and visualization pipeline is implemented via PostGis and Vue.

## Web Application
Using Django, a high-level Python Web framework that encourages rapid development and clean, pragmatic design, Gmail based authenticated web application which allows users to add, update and delete measurements. Once the user is satisfied with the date, the same can be pushed to Analysis & Visualization Pipeline.

![Block-Diagram](../master/images/block-diagram.png)

## Installtion
### Development mode on AWS
Lassaress web server can be hosted on AWS for development purposes by using the Cloud Formation file: pfiCloudFormation.json
User is prompted to provide following information:
- MBTOKEN - Map Box Token
- CLIENTID - Auth0 Client ID
- AUTH0DOMAIN - Auth0 Domain
- APIIDENTIFIER -
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
