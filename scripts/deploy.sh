
export ENV=$1
export VERSION=$2
docker-compose up app-$ENV -d --force-recreate
