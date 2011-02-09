mkdir -p /opt/milkywhite/apps/testpackage/logs/apache/
mkdir -p /opt/milkywhite/apps/testpackage/logs/nginx/

chown www-data.adm /opt/milkywhite/apps/testpackage/logs/apache/
chown www-data.adm /opt/milkywhite/apps/testpackage/logs/nginx/

ln -s /opt/milkywhite/apps/testpackage/mwpackage/apache.conf /etc/apache2/sites-enabled/testpackage.conf
ln -s /opt/milkywhite/apps/testpackage/mwpackage/nginx.conf /etc/nginx/sites-enabled/testpackage.conf

ln -s /opt/milkywhite/apps/testpackage/mwpackage/logrotate /etc/logrotate.d/testpackage