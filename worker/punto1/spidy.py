import re
from urllib import request

with request.urlopen('http://uniandes.edu.co/institucional/facultades/facultades') as response:
   root = response.read().decode()

x = re.findall('<li><a\s+href="https?://([^"]+uniandes\.edu\.co)[^"]*"\s+[^>]*>([^<]*(Facultad|Departamento|Centro|Escuela)[^<]*)</a></li>', root)
x = list(set([i[:2] for i in x]))
x.sort(key=lambda i: i[1])
for i in x:
    print(i)
