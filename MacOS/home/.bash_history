chsh -s /bin/zsh
docker run --name repo alpine/git clone https://github.com/docker/getting-started.git
docker cp repo:/git/getting-started/ .
ll
la
ls -lah
cd getting-started/
la
ls -lah
docker build -t docker101tutorial .
docker run -d -p 80:80 --name docker-tutorial docker101tutorial
