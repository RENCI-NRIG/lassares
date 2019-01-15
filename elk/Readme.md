# Elastic Search Kibana Logstash (ELK)

## What is ELK ?
"ELK" is the acronym for three open source projects: Elasticsearch, Logstash, and Kibana. Elasticsearch is a search and analytics engine. Logstash is a server‑side data processing pipeline that ingests data from multiple sources simultaneously, transforms it, and then sends it to a "stash" like Elasticsearch. Kibana lets users visualize data with charts and graphs in Elasticsearch.

The Elastic Stack is the next evolution of the ELK Stack. For more details: [ELK](https://www.elastic.co/elk-stack)

## How to use ?

Clone the code from the lassaress repository on any of linux CentOs-6 based server and execute the configElkServer.sh script
```
# git clone https://github.com/RENCI-NRIG/lassares.git /root/lassaress
# /root/lassaress/configElkServer.sh <BUCKETNAME> <ELASTIC_VERSION>
```

## What does this installation do?
- Sets up elastic user for elasticsearch, kibana and logstash
- Creates Mapping for the Lassaress Measurements
- Creates a Default Index for the Lassaress Measurements
- Sets up a cron job to periodically create visualizations

## Manual configuration

Increase tileMap MaxPrecision:
a) Log on to Kibana via http://<public-ip-of-your-instance>:5601
b) Go to Management->Advanced Settings(under kibana), Change visualization:tileMap:maxPrecision to 10. Default value is 7.
![Advanced](../../master/images/Advanced.png)
