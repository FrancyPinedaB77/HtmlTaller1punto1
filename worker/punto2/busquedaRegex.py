import sys
import os
import re
from itertools import permutations


numargs = len(sys.argv)

if numargs < 3:
    print('insuficientes argumentos')
    sys.exit(1)

flag = 0
# opcion para que sea ignorecase = True
if '-i' ==  sys.argv[1]:
    flag = re.I
    campo = sys.argv[2]
    if numargs >= 3:
        palabras = sys.argv[3:]
    else:
        print('insuficientes argumentos')
        sys.exit(1)
else:
    campo = sys.argv[1]
    palabras = sys.argv[2:]

path = os.path.dirname(os.path.realpath(__file__))
 
c = r"[^<]*"
# Cadenas iniciales y finales para Titulo (T0,T1)
qT0 = r"<item><id>(\d+)</id><title>"
qT1 = r"</t"

# Cadenas iniciales y finales para Descripcion (D0,D1)
qD0 = r"<item><id>(\d+)</id>(?:<[^>]+>[^<]+</[^>]+>){3}<description>"
qD1 = r"</d"

# Cadenas iniciales y finales para Categoria (C0,C1)
qC0 = r"<item><id>(\d+)</id>(?:<[^>]+>[^<]+</[^>]+>){4}\
      (?:<category>[^<]+</category>)*(?:<category>"
qC1 = r"</category>)+(?:<category>[^<]+</category>)*"

# Juntar cada palabra con el operador "o"
regexOr = c + "(?:"
for w in palabras[:-1]:
    regexOr += w + "|"
regexOr+=palabras[-1] + ")" + c

# Para el operador "Y" se necesitan todas las posibles permutaciones
perm = list(permutations(palabras))
regexAnd = ""
for per in perm[:-1]:
    regexAnd += "(?:" + c
    for w in list(per):
        regexAnd += str(w) + c 
    regexAnd += ")|"
regexAnd += "(?:" + c
for w in list(perm[-1]):
    regexAnd += str(w) + c 
regexAnd+=")"

# Concatenacion de las regex completas
if campo == 'title':
    queryAnd = qT0 + regexAnd + qT1
    queryOr = qT0 + regexOr + qT1
elif campo == 'description':
    queryAnd = qD0 + regexAnd + qD1
    queryOr = qD0 + regexOr + qD1
elif campo == 'category':
    queryAnd = qT0 + regexAnd + qT1
    queryOr = qT0 + regexOr + qT1
    print('Busqueda por', campo)
elif campo == 'all':
    print('Busqueda por', campo)
else:
    print('Campo invalido')
    sys.exit(1)

feed = open(path+'/db_feed.xml','r').read()
results = re.findall(queryAnd,feed,flags=flag)+\
          re.findall(queryOr,feed,flags=flag)
uniq = []
for item in results:
    if item not in uniq:
        uniq.append(item)
print("\n".join(uniq))
