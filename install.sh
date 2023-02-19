#!/bin/sh

pip3 install -r requirements.txt

mkdir -p bin && cd bin

curl -L https://github.com/skylot/jadx/releases/download/v1.3.3/jadx-1.3.3.zip -o jadx.zip
7z x -ojadx jadx.zip 
rm jadx.zip

git clone https://github.com/ndrancs/AIK-Linux-x32-x64.git aik
chmod +x aik/*.sh

git clone https://github.com/anestisb/android-simg2img.git simg2img
cd simg2img && make

cd ../../

mkdir -p ~/.local/bin/candy
ln -s $PWD/candy.py ~/.local/bin/candy