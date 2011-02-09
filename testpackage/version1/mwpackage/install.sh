mkdir /opt/milkywhite/apps/testpackage/logs/nginx/
mkdir /opt/milkywhite/apps/testpackage/logs/apache/

ln -s /opt/milkywhite/apps/mwpackage/apache.conf /etc/apache2/sites-available/testpackage.conf
ln -s /opt/milkywhite/apps/mwpackage/nginx.conf /etc/nginx/sites-available/testpackage.conf