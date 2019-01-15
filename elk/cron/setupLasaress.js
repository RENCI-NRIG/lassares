var fs = require('fs');
var http = require('http');
var elasticsearch = require('elasticsearch');

var createVisPath = '/api/saved_objects/visualization';
var deleteAllVisPath = '/.kibana/doc/_delete_by_query';
var deleteAllVisBody = '{"query": {"match": {"type": "visualization"}}}';

function replaceAll(str, find, replace) {
    return str.replace(new RegExp(find, 'g'), replace);
}

function sendRestRequest(operation, reqPath, port, body) {
    const options = {
        hostname: '172.31.22.51',
        port: port,
        auth: 'elastic:elastic',
        path: reqPath,
        method: operation,
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(body),
            'kbn-xsrf': 'true'
        }
    };

    const req = http.request(options, (res) => {
        console.log(`STATUS: ${res.statusCode}`);
        console.log(`HEADERS: ${JSON.stringify(res.headers)}`);
        res.setEncoding('utf8');
        res.on('data', (chunk) => {
            console.log(`BODY: ${chunk}`);
        });
        res.on('end', () => {
            console.log('No more data in response.');
        });
    });

    req.on('error', (e) => {
        console.error(`problem with request: ${e.message}`);
    });

    // write data to request body
    req.write(body);
    req.end();
}

// Read the JSON
var visualize = fs.readFileSync('/root/cron/vis.json', 'utf8');


var client = new elasticsearch.Client({
  host: 'http://elastic:elastic@172.31.22.51:9200'
});

void async function() {
    try {
        // Delete all existing visualizations
        await sendRestRequest('POST', deleteAllVisPath, 9200, deleteAllVisBody);
        // Search for all the unique jobIds
        const resp = await client.search({
            index: 'logstash-*',
            body: {
                "size" : "0",
                "aggs" : {
                    "distinct_jobs": {
                        "composite" : {
                            "sources" : [
                                { "JobId": { "terms" : { "field": "Measurement.JobId" } } }
                            ]
                        }
                    }
                }
            }
        });
        var jobArr = resp.aggregations.distinct_jobs.buckets;
        // Create visualization for each JobId
        for( var job in jobArr) {
            if(jobArr.hasOwnProperty(job)) {
                console.log("Creating visualization for JobId: " + jobArr[job].key.JobId);
                var body = visualize;
                body = replaceAll(body, "JOBID", jobArr[job].key.JobId);
                console.log("Visualization body for JobId: " + body);
                await sendRestRequest('POST', createVisPath, 5601, body);
            }
        }
    }
    catch (error) {
        console.trace(error.message)
    }
}();
