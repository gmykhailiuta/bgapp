#/bin/sh
export ENV=$1
cd nginx
envsubst '$ENV' < app.conf.template > app.conf
docker-compose exec nginx /bin/sh -c 'nginx -s reload'
curl -s $(docker-compose port nginx 8000)/api
echo  "\n"
