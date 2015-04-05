# Deployment

- Install Docker in your machine (see <https://get.docker.com/> or <https://docs.docker.com/installation/>).
- `git clone https://github.com/Stegoo/lol-senpai.git`
- `docker build -t lol-senpai lol-senpai/`
- `docker run --name lol-senpai -p 5000:5000 -d lol-senpai`
