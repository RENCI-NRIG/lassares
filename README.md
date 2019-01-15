# Lassaress
This project involves development and configuration of cloud-based data collection, analysis and visualization pipeline as well as mobile web application. See more details about the project [here!](http://nrig.renci.org/project/lassaress/)

## Analysis & Visualization Pipeline
Analysis and visualization pipeline is implemented via Elastic Search, Logstash and Kibana stack.

## Web Application
Using Django, a high-level Python Web framework that encourages rapid development and clean, pragmatic design, Gmail based authenticated web application which allows users to add, update and delete measurements. Once the user is satisfied with the date, the same can be pushed to Analysis & Visualization Pipeline.

![Block-Diagram](../master/images/block-diagram.png)

## Open Items
- Domain name for webserver
- License for Elastic Stack. Open Source Apache license does not have security and advanced zoom level needed for the Coordinate Map visualization.
