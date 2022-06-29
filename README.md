Assetto Corsa server exporter for Prometheus

simple python app to export online players values, uses openmetrics format (prometheus compatible)

usage:
    1. upload wherever u want to run it
    2. adjust the script output file using FILE variable
    3. change execute bit (chmod u+x etc) 
    4. setup cron to periodically run the script

if you want to collect the data, you need to make it possible for eg prometheus to collect this data. Sample simple nginx config:

    server {
    
    listen 80;
    server_name hostname; 
    root /var/www/metrics;

    location / {
        add_header Cache-Control 'must-revalidate';
        add_header Content-Type text/plain;
        try_files $uri $uri/ =404;
    }
}

and of course in the python script defined FILE path as: /var/www/metrics/acmetrics.

For prometheus: 

  - job_name: 'assetto_servers'
    scheme: "http"
    metrics_path: 'acmetrics'
    static_configs:
    - targets: ['hostname']

and for grafana to import the dashboard, a json model is made available (a basic version that i created at the time of creating this readme).

More values can be easily made available, however were not needed for me at the time of writing this readme.
