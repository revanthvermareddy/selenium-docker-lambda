#!/bin/bash
# download and install latest geckodriver for linux.
# required for selenium to drive a firefox browser.

install_dir="/usr/local/bin"
json=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest)
yum install jq -y
url=$(echo "$json" | jq -r '.assets[].browser_download_url | select(contains("linux64") and endswith("gz"))')
curl -s -L "$url" | tar -xz
chmod +x geckodriver
mv geckodriver "$install_dir"
rm -f geckodriver*tar*
echo "installed geckodriver binary in $install_dir"