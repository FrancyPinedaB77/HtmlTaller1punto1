import re
import sys
from itertools import permutations

numargs = len(sys.argv)
if numargs < 3:
    print('insuficientes argumentos')
    sys.exit(1)

if '-i' ==  sys.argv[1]:
    ignoreCase = True
    campo = sys.argv[2]
    if numargs >= 3:
        palabras = sys.argv[3:]
    else:
        print('insuficientes argumentos')
        sys.exit(1)
else:
    ignoreCase = False
    campo = sys.argv[1]
    palabras = sys.argv[2:]

c = r"[^<]*"

qT0 = "<item><id>(\d+)</id><title>"
qT1 = "</t"

qD0 = "<item><id>(\d+)</id>(<[^>]+>[^<]+</[^>]+>){3}<description>"
qD1 = "</d"

qC0 = "<item><id>(\d+)</id>(<[^>]+>[^<]+</[^>]+>){4}(<category>[^<]+</category>)*(<category>"
qC1 = "</category>)+(<category>[^<]+</category>)*"
regexOr = c + "("
for w in palabras[:-1]:
    regexOr += w + "|"
regexOr+=palabras[-1] + ")" + c

perm = list(permutations(palabras))
regexAnd = ""
for per in perm[:-1]:
    regexAnd += "(" + c
    for w in list(per):
        regexAnd += str(w) + c 
    regexAnd += ")|"
regexAnd += "(" + c
for w in list(perm[-1]):
    regexAnd += str(w) + c 
regexAnd+=")"

print(regexOr)
print(regexAnd)

if campo == 'title':
    queryAnd = 
    print('Busqueda por', campo)
elif campo == 'description':
    print('Busqueda por', campo)
elif campo == 'category':
    print('Busqueda por', campo)
elif campo == 'all':
    print('Busqueda por', campo)
else:
    print('Campo invalido')
    sys.exit(1)

print('palabras de busqueda',palabras)
