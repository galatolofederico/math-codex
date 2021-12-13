#!/bin/sh

mkdir -p ./tmp
mkdir -p ./completions

wget http://131.114.50.176/owncloud/s/0uq5NQmZpHUeMBe/download -O ./tmp/completions.zip
unzip ./tmp/completions.zip -d .