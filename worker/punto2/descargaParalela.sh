#!/bin/bash

PARAMS_DESCARGA=''
FEEDS=''
n=0
for i in $(cat fuentesRSS.csv)
do c=$(echo $i -O feed$n.xml)
FEEDS+=feed$n.xml' '
n=$(($n+1))
PARAMS_DESCARGA+=$c' '
done
mkdir -p tmp; cd tmp
echo $PARAMS_DESCARGA | xargs -n 3 -P 4 wget -q
echo $FEEDS | xargs -n 1 -P 4 python ../limpiezaFeeds.py
FEED_FINAL='db_feed.xml'
echo "<?xml version='1.0' encoding='UTF-8'?>" > $FEED_FINAL
echo "<resultados>" >> $FEED_FINAL
cat feed* >> $FEED_FINAL
echo "</resultados>" >> $FEED_FINAL
mv $FEED_FINAL ../
cd ..
rm -rf tmp
