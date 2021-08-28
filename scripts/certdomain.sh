# create or renew certificate for domain given as argument
# $1 is for example dev.ivanne.de

echo $(date)
echo $1
echo
PROXYPATH=/home/shell/projects/web/django/nginx
mkdir -vp $PROXYPATH/cert
sudo certbot certonly -a standalone -d $1 \
 --non-interactive --agree-tos -m admin@ivanne.de
sudo cp /etc/letsencrypt/live/$1/privkey.pem $PROXYPATH/cert/
sudo cp /etc/letsencrypt/live/$1/fullchain.pem $PROXYPATH/cert/
sudo chmod +r $PROXYPATH/cert/*