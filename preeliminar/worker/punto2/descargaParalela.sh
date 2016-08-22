PARAMS=''
n=0
for i in $(cat fuentesRSS.csv)
do c=$(echo $i -O feed$n.xml)
n=$(($n+1))
PARAMS+=$c' '
done
echo $PARAMS | xargs -n 3 -P 8 wget -q 
