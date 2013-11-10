#! /bin/bash

HOME=/home/proj3
USERNAME=proj3

PACKAGES=(gcc-c++ git wget vim tmux kernel-modules-extra)

STARTER_REPO="https://github.com/dtnaylor/bitrate-project-starter.git"

WWW_DOWNLOAD="http://gs11697.sp.cs.cmu.edu:15441/www.tar.gz"
WWW_TARBALL="www.tar.gz"
WWW_SRC_DIR="www"

CLICK_DOWNLOAD="http://www.read.cs.ucla.edu/click/click-2.0.1.tar.gz"
CLICK_TARBALL="click-2.0.1.tar.gz"
CLICK_SRC_DIR="click-2.0.1"
APACHE_DOWNLOAD="http://apache.mirrors.pair.com//httpd/httpd-2.2.25.tar.gz"
APACHE_TARBALL="httpd-2.2.25.tar.gz"
APACHE_SRC_DIR="httpd-2.2.25"
F4F_DOWNLOAD="http://gs11697.sp.cs.cmu.edu:15441/adobe_f4f_apache_module_4_5_1_linux_x64.tar.gz"
F4F_TARBALL="adobe_f4f_apache_module_4_5_1_linux_x64.tar.gz"
F4F_SRC_DIR="adobe_f4f_apache_module_4_5_1_linux_x64"
F4F_CONF="LoadModule f4fhttp_module modules/mod_f4fhttp.so\n
<IfModule f4fhttp_module>\n
<Location /vod>\n
HttpStreamingEnabled true\n
HttpStreamingContentPath \"/var/www/vod\"\n
</Location>\n
</IfModule>\n"

TC=/usr/sbin/tc
CLICK=/usr/local/bin/click
APACHE=/usr/local/apache2/bin/httpd
APACHE_CONF_DIR=/usr/local/apache2/conf
APACHE_MODULES_DIR=/usr/local/apache2/modules

install_tarball() {
	cd $HOME
	wget $1
	tar -xzf $2
	cd $3
	./configure
	make
	make install
}



# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# Make sure user's home dir exists where we think it does
if [ ! -d "$HOME" ]; then
	echo "Could not find home directory: $HOME"
	exit 1
fi

# Install packages
echo "Installing packages..."
for package in ${PACKAGES[*]}
do
	yum install $package
done

# Removing fedora firewall
echo "removing fedora firewall"
yum remove firewalld

# Install Click 2.0.1
echo "Installing click..."
install_tarball $CLICK_DOWNLOAD $CLICK_TARBALL $CLICK_SRC_DIR

# Install Apache 2.2.5
echo "Installing apache..."
install_tarball $APACHE_DOWNLOAD $APACHE_TARBALL $APACHE_SRC_DIR

## Update Firefox
#echo "Updating Firefox..."
#yum update firefox
#
## Install flash plugin
#echo "Installing Flash plugin..."
#yum install http://linuxdownload.adobe.com/adobe-release/adobe-release-x86_64-1.0-1.noarch.rpm -y  # 64-bit
##yum install http://linuxdownload.adobe.com/adobe-release/adobe-release-i386-1.0-1.noarch.rpm -y   # 32-bit
#rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-adobe-linux
#yum install flash-plugin -y

# Install Adobe f4f origin module for apache
echo "Installing Adobe f4f origin module for apache..."
cd $HOME
wget $F4F_DOWNLOAD
tar -xzf $F4F_TARBALL
cp ./$F4F_SRC_DIR/* /$APACHE_MODULES_DIR
if ! grep -q "f4f" $APACHE_CONF_DIR/httpd.conf
then
    echo -e $F4F_CONF >> $APACHE_CONF_DIR/httpd.conf
fi

# Copy www files to /var/www
echo "Installing www files..."
cd $HOME
wget $WWW_DOWNLOAD
tar -xzf $WWW_TARBALL
mv $WWW_SRC_DIR /var/

# Set permissions
echo "Setting file permissions..."
chmod 6755 $TC
chmod 6755 $CLICK
chmod 6755 $APACHE
chmod 777 $APACHE_CONF_DIR
chmod 777 $APACHE_CONF_DIR/httpd.conf

# Clone starter code
echo "Cloning starter code..."
cd $HOME
sudo -u $USERNAME git clone $STARTER_REPO


echo "Done."
