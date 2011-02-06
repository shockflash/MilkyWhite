# download package
sudo su 
rm -rf /opt/milkywhite/milkywhite/
mkdir -p /opt/milkywhite/
cd /opt/milkywhite
rm -f *.gz
wget -c --no-check-certificate "http://github.com/shockflash/MilkyWhite/tarball/master" -O milkywhite.tar.gz
tar -zxf *.gz
mv shockflash* milkywhite

# install dependencies
easy_install pip
pip install boto

# setup settings 
mkdir /etc/milkywhite/
touch /etc/milkywhite/settings.py
ln -s /etc/milkywhite/settings.py settings.py

# setup cron 
ln -s cron /etc/cron.d/milkywhite

# setup cache for apache and nginx
mkdir -p /var/milkywhite/cache/tmp
chmod 777 /var/milkywhite/cache/
chmod 777 /var/milkywhite/cache/tmp

# setup init script 
ln -s init.sh /etc/init.d/milkywhite
update-rc.d milkywhite defaults
chmod +x /etc/init.d/milkywhite

echo "\n\nREMEMBER TO CONFIGURE /etc/milkywhite/settings.py!\n\n"