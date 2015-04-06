# Deployment

## Preparation

- Install Docker on your machine (see <https://get.docker.com/> or <https://docs.docker.com/installation/>).
- `git clone https://github.com/Stegoo/lol-senpai.git`
- `docker build -t lol-senpai lol-senpai/`
- `docker run --name lol-senpai-redis -d redis`
- `docker run --name lol-senpai -p 5000:5000 --link lol-senpai-redis:redis -e "API_KEY=YOUR_API_KEY" -d lol-senpai` (replace `YOUR_API_KEY` with your key)


## Access

You can access this website through `http://your-domain.tld:5000`.

If you want to use port 80, run your image with this command: `docker run --name lol-senpai -p 80:5000 --link lol-senpai-redis:redis -e "API_KEY=YOUR_API_KEY" -d lol-senpai`.

Otherwise, if you want use Apache or Nginx, here is their configurations:

### Apache

Beforehand, you must enable modules `proxy` and `proxy_http`.

```
<VirtualHost your-domain.tld:80>
        ServerName your-domain.tld
        ProxyPass / http://localhost:5000/
        ProxyPassReverse / http://localhost:5000/
        ProxyPreserveHost On
</VirtualHost>
```

### Nginx

```
upstream senpai {
	server 127.0.0.1:5000;
}
server {
	listen 80;
	server_name your-domain.tld;
	location / {
		proxy_pass http://senpai;
	}
}
```
