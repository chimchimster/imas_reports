## Настройка Nginx для конкурентной работы с сервисами highcharts.

1. docker pull onsdigital/highcharts-export-node
2. docker network create my_network
3. docker run -d --name=service1 --network=my_network onsdigital/highcharts-export-node (Столько инстансов сколько понадобится).
4. docker run -d --name=nginx-proxy --network=my_network -p 80:80 nginx

## Конфиг NGINX

```
worker_processes 5;

events {

    worker_connections 1024;
}

http {

    upstream backend {
	ip_hash;
        server IP:PORT;
        server IP:PORT;
        server IP:PORT;
    }

    server {
        listen 80;

        location / {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }
    }
}
```