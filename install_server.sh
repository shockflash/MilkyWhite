# download package
rm -rf /opt/milkywhite/milkywhite/
mkdir -p /opt/milkywhite/
cd /opt/milkywhite
rm -f *.gz
wget -c --no-check-certificate "http://github.com/shockflash/MilkyWhite/tarball/master" -O milkywhite.tar.gz
tar -zxf *.gz
mv shockflash* milkywhite
rm -f *.gz
cd milkywhite

# install dependencies
apt-get install -y python-virtualenv

# setup settings 
mkdir /etc/milkywhite/
touch /etc/milkywhite/settings.py
ln -s /etc/milkywhite/settings.py settings.py

touch /opt/milkywhite/version.info

# setup cron 
ln -s /opt/milkywhite/milkywhite/cron /etc/cron.d/milkywhite

# setup cache for apache and nginx
mkdir -p /opt/milkywhite/apps/
mkdir -p /opt/milkywhite/cache/tmp
chmod 777 /opt/milkywhite/cache/
chmod 777 /opt/milkywhite/cache/tmp

# setup init script 
ln -s /opt/milkywhite/milkywhite/init.sh /etc/init.d/milkywhite
update-rc.d milkywhite defaults
chmod +x init.sh

# setup virtual env, since the local boto is outdated

virtualenv --no-site-packages /opt/milkywhite/env
/opt/milkywhite/env/bin/easy_install pip
/opt/milkywhite/env/bin/pip install -E /opt/milkywhite/env boto==2.0b3

echo "\n\nREMEMBER TO CONFIGURE /etc/milkywhite/settings.py!\n\n"