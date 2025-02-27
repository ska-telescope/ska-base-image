# /etc/nginx/nginx.conf
user  nginx;
worker_processes  ${NGINX_WORKER_PROCESSES};

error_log  /var/log/nginx/error.log  ${NGINX_LOG_LEVEL};
pid        /var/run/nginx.pid;

events {
    worker_connections  ${NGINX_WORKER_CONNECTIONS};
}

http {
    # Load standard MIME types
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    
    # Logs
    log_format main '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent"';

    access_log  /var/log/nginx/access.log  main;

    # Security
    server_tokens off;

    # Keepalive settings
    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 4096;

    # Gzip Compression
    gzip on;
    gzip_proxied     any;
    gzip_min_length  1024;
    gzip_comp_level  5;
    gzip_types
        text/plain
        text/css
        text/javascript
        application/javascript
        application/x-javascript
        application/json
        application/xml
        image/svg+xml;
    
    # Cache
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=cache:10m
                     max_size=1g inactive=60m use_temp_path=off;

    # Include any custom/global configs
    include /etc/nginx/conf.d/*.conf;

    server {
        # Listen on HTTP
        listen ${NGINX_PORT};
        server_name ${NGINX_SERVER_NAME};

        # Path static content root
        root ${NGINX_ROOT};
        index index.html index.htm;

        # Security headers
        add_header X-Content-Type-Options "nosniff";
        add_header X-XSS-Protection "1; mode=block";
        add_header X-Frame-Options "SAMEORIGIN";

        # Serve static files with caching
        location ~* \.(?:css|js|gif|jpe?g|png|ico|svg|woff2?|ttf|eot)$ {
            expires ${NGINX_STATIC_FILE_CACHE_EXPIRATION};
            add_header Pragma public;
            add_header Cache-Control "public";
            try_files $uri =404;
        }

        # Default location for static files
        location / {
            try_files $uri $uri/ =404;
        }
    }
}
