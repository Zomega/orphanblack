#!/usr/bin/env bash

apt-get update
apt-get install -y python-pip git
if ! [ -L /var/www ]; then
  rm -rf /var/www
  ln -fs /vagrant /var/www
fi

# Install orphanblack's dependancies (many are not on testpypi.)
pip install Jinja2 click tabulate

# Install orphanblack from the test server.
pip install -i https://testpypi.python.org/pypi --no-dependencies orphanblack

# Clone a python repo for testing.
git clone https://github.com/zomega/gooey python-repo
