Copy .bash_profile and .bashrc to User Dir:
-------------
cp .bash_profile ~/.bash_profile
cp .bashrc ~/.bashrc
source .bashrc


Change Message of the Day:
-------------
cp motd /etc/motd


Create Backup USB Installer (OS X Yosemite):
-------------
sudo /Applications/Install\ OS\ X\ Yosemite.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume --applicationpath /Applications/Install\ OS\ X\ Yosemite.app
