#!bin/bash
OPTIND=1
p=$(dirname $(readlink -e -s $0))

#opciones de comando
ignore_case=""
update=0
log_op=" and "
while getopts "ui" opt; do
  case $opt in
    u)update=1;;
    i)ignore_case="lower-case";;
  esac
done

queryAnd="for \$x in doc(\"$p/db_feed.xml\")//item\n"
queryOr="$queryAnd"

#campo de busqueda
campo=${!OPTIND}
OPTIND=$OPTIND+1

#construir la query segun el campo de busqueda
case $campo in
    
    "description"|"title")
        queryAnd+="where("
        queryOr+="where("
        for i in $(seq $OPTIND $(($# - 1)))
            do
                queryAnd+="contains($ignore_case(\$x/$campo),$ignore_case(\"${!i}\")) and "
                queryOr+="contains($ignore_case(\$x/$campo),$ignore_case(\"${!i}\")) or "
        done
        queryAnd+="contains($ignore_case(\$x/$campo),$ignore_case(\"${@: -1}\"))"
        queryOr+="contains($ignore_case(\$x/$campo),$ignore_case(\"${@: -1}\"))"
        queryAnd+=")\nreturn data(\$x/id)"
        queryOr+=")\nreturn data(\$x/id)";;
    
    "category")
        queryAnd+="return\n(\n        for \$y in \$x/category\n        where ("
        queryOr+="return\n(\n        for \$y in \$x/category\n        where ("
        for i in $(seq $OPTIND $(($# - 1)))
            do
            queryAnd+="contains($ignore_case(\$y),$ignore_case(\"${!i}\")) and "
            queryOr+="contains($ignore_case(\$y),$ignore_case(\"${!i}\")) or "
        done
        queryAnd+="contains($ignore_case(\$y),$ignore_case(\"${@: -1}\")))"
        queryOr+="contains($ignore_case(\$y),$ignore_case(\"${@: -1}\")))"
        queryAnd+="return data(\$x/id)\n    )[1]"
        queryOr+="return data(\$x/id)\n    )[1]";;
    
    "all")  echo Vamos a buscar en todas;;
    *)  echo $campo no es un Campo valido;exit 1;;
esac
echo -e $queryAnd > tmpfileAnd
echo -e $queryOr > tmpfileOr
xqilla tmpfileAnd > and
xqilla tmpfileOr > or
cat and or |  awk '!x[$0]++'
rm  tmpfileAnd tmpfileOr and or
