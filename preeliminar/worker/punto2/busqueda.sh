#!bin/bash
OPTIND=1

#opciones de comando
ignore_case=""
update=0
log_op=" and "
while getopts "uio" opt; do
  case $opt in
    u)update=1;;
    i)ignore_case="lower-case";;
    o)log_op=" or "
  esac
done

query="for \$x in doc(\"db_feed.xml\")//item\n"
#campo de busqueda
campo=${!OPTIND}
OPTIND=$OPTIND+1
case $campo in
  "description"|"title")
    query+="where("
    for i in $(seq $OPTIND $(($# - 1)))
      do query+="contains($ignore_case(\$x/$campo),$ignore_case(\"${!i}\"))"$log_op
    done
    query+="contains($ignore_case(\$x/$campo),$ignore_case(\"${@: -1}\"))"
    query+=")\nreturn data(\$x/id)";;
        #"title")  echo Vamos a buscar por titulo;;
     "category")  echo Vamos a buscar por categoria;;
          "all")  echo Vamos a buscar en todas;;
              *)  echo $campo no es un Campo valido;exit 1;;
esac
echo -e $query > tmpfile
xqilla tmpfile
rm tmpfile
