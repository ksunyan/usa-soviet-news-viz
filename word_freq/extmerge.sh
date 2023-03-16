tar -xf $1 '*.txt' && rsync -a sn83045462/ . && rm -r sn83045462 && rm $1
echo "Done"


