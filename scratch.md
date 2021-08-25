
### Certificate

Let's encrypt:

```console
sudo apt install certbot python3-certbot-nginx
certbot --version
sudo certbot certonly --nginx
sudo certbot install --nginx
```

Edit ```nginx/default.conf``` with the help following output:

```console
tail -n 22 /etc/nginx/sites-available/default
```



docker-compose


  proxy:
    build:
      context: ./nginx
    volumes:
      - static_data:/vol/static
      - /etc/letsencrypt:/etc/letsencrypt
  
  
  
nginx


server {
	listen 8080;

	location /static {
		alias /vol/static;
	}

	location / {
		uwsgi_pass app:8000;
		include /etc/nginx/uwsgi_params;
	}

    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/box.ivanne.de/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/box.ivanne.de/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

}
server {
    if ($host = box.ivanne.de) {
        return 301 https://$host$request_uri;
    }
}



Dockerfile

RUN mkdir -p /etc/letsencrypt
