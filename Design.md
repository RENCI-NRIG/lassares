# Lassaress Software Architecture
The LASSARESS software architecture consists of two separate components
- Data collection 
- Data processing. 

Data collection is based on available standards and frameworks and provide mechanisms for low-latency collection of data from multiple geographically distributed devices. Data collection architecture provides the flexibility of early data aggregation and processing in at the edge for low-latency response with further forwarding of the data to the public cloud for processing and long-term storage. 

Data processing architecture supports processing at the edge as well as more complex processing and long-term storage of the collected data in the public cloud. 
 
Amazon Web Services (AWS) provides several services that could be used, also mature open source alternatives exist. Both are described in this document.

## Data collection and processing architecture alternatives
- AWS Greengrass
  - Established
  - Siloed
  - Vendor lock-in
- Apache ELK stack
  - Open-source
  - Extensible and highly configurable
  - Requires some work to connect to devices producing measurements
- ELK can be deployed in on-premises infrastructure or institutional or public cloud
  - Provides substantial deployment and scaling flexibility

[collection]

### Kafka and Elastic Search
- Apache Kafka [1] is a “distributed streaming platform.” It provides many of the data collection architecture requirements out of the box; others may require custom programming. Kafka enables secure and scalable message transfer, fault-tolerant storage, and stream processing.  By coupling stream processing with storage, it allows for re-processing (see Kappa Architecture).

- Security, both authentication and encryption, is accomplished using SSL and/or SASL, and must be managed manually.

- Kafka is not an IoT platform, so it does not provide any mechanism for configuration control of devices. Any device security settings would need to be managed manually.  However, the number of deployed devices is expected to be small.

- Kafka does not directly provide a mechanism for edge processing of data, although it does have a framework, Kafka Connect, to simplify data transfer from the device.  Other open source solutions, such as Logstash or Beats (both part of the Elastic Stack) can be used for any pre-processing necessary along with data transfer.

- Elastic Stack [2] provides a suite of tools to search, analyze, and visualize data. This can be deployed as an entirely self-managed open source stack, or Elastic (the company) provides several licensing tiers that can include support and hosting. Amazon and other companies also provide managed Elasticsearch Services. Kafka can be integrated with the Elastic Stack via Logstash. 

### Measurement collection
- Measurements collected by devices are streamed via Kafka+Logstash into ELK engine (Elastic Search + Kibana visualization)
- Each measurement carries standardized metadata 
- Measurements are 
  - Stored for long-term analysis
  - Used for GIS visualization of measurement gradients   
- Visualization resolution currently limited to (at 30 deg lat for continental US)

[measurement]

Each measurement associated with metadata that is stored together with measured values

[metadata]

### Measured variables (non-exhaustive 
[variables]


