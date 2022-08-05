mkdir -p ~/rar
cd ~/rar
wget http://www.rarlab.com/rar/rarlinux-x64-5.3.0.tar.gz
tar xvf rarlinux-x64-5.3.0.tar.gz
cd rar
make
make install
cd ..
rm -rf ~/rar