Copy `.bash_profile` and `.bashrc` to User Dir:
-------------
```sh
cp .bash_profile ~/.bash_profile
cp .bashrc ~/.bashrc
source .bashrc
```

Change Message of the Day (MotD):
-------------
```sh
cp motd /etc/motd
```


Create Backup USB Installer (OS X Yosemite):
-------------
```sh
sudo /Applications/Install\ OS\ X\ Yosemite.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume --applicationpath /Applications/Install\ OS\ X\ Yosemite.app
```
