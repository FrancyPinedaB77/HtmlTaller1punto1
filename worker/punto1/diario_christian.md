En este documento esta registrado mi progreso sobre el scapping de los eventos de la universidad - Christian Poveda

### Agosto 23, 18:51
He estado trabajando con `Python` y su modulo de expresiones regulares `re` para el trabajo de exploración. Hasta el momento he podido recuperar los enlaces a las distintas unidades académicas de la universidad desde la página http://uniandes.edu.co/institucional/facultades/facultades. Se reportan las siguientes unidades académicas: 
#### Actualizada en Agosto 23, 18:51
| Unidad académica | URL |
| ---------------- | --- |
| Centro Interdisciplinario de Estudios sobre Desarrollo (CIDER) |  http://cider.uniandes.edu.co  |
| Centro de Estudios en Periodismo - Ceper |  http://ceper.uniandes.edu.co  |
| Departamento de Antropología |  http://antropologia.uniandes.edu.co  |
| Departamento de Arquitectura |  http://arquitectura.uniandes.edu.co  |
| Departamento de Arte |  http://arte.uniandes.edu.co  |
| Departamento de Ciencia Politica |  http://c-politica.uniandes.edu.co  |
| Departamento de Ciencias Biológicas |  http://cienciasbiologicas.uniandes.edu.co  |
| Departamento de Diseño |  http://design.uniandes.edu.co  |
| Departamento de Filosofia |  http://filosofia.uniandes.edu.co  |
| Departamento de Fisica |  http://fisica.uniandes.edu.co  |
| Departamento de Geociencias |  http://geociencias.uniandes.edu.co  |
| Departamento de Historia |  http://historia.uniandes.edu.co  |
| Departamento de Humanidades y Literatura |  http://humlit.uniandes.edu.co  |
| Departamento de Ingenieria Civil y Ambiental |  http://civil.uniandes.edu.co  |
| Departamento de Ingeniería Biomédica |  http://ingbiomedica.uniandes.edu.co  |
| Departamento de Ingeniería Eléctrica y Electrónica |  http://electrica.uniandes.edu.co  |
| Departamento de Ingeniería Industrial |  http://industrial.uniandes.edu.co  |
| Departamento de Ingeniería Mecánica |  http://mecanica.uniandes.edu.co  |
| Departamento de Ingeniería Química |  http://ingquimica.uniandes.edu.co  |
| Departamento de Ingeniería de Sistemas y Computación |  http://sistemas.uniandes.edu.co  |
| Departamento de Lenguas y Cultura |  http://lenguas.uniandes.edu.co  |
| Departamento de Matemáticas |  http://matematicas.uniandes.edu.co  |
| Departamento de Musica |  http://musica.uniandes.edu.co  |
| Departamento de Psicología |  http://psicologia.uniandes.edu.co  |
| Departamento de Química |  http://quimica.uniandes.edu.co  |
| Escuela de Gobierno Alberto Lleras Camargo |  http://gobierno.uniandes.edu.co  |
| Facultad de Administración |  http://administracion.uniandes.edu.co  |
| Facultad de Arquitectura y Diseño |  http://arqdis.uniandes.edu.co  |
| Facultad de Artes y Humanidades |  http://facartes.uniandes.edu.co  |
| Facultad de Ciencias |  http://ciencias.uniandes.edu.co  |
| Facultad de Ciencias Sociales |  http://faciso.uniandes.edu.co  |
| Facultad de Derecho |  http://derecho.uniandes.edu.co  |
| Facultad de Economía |  http://economia.uniandes.edu.co  |
| Facultad de Educación |  http://cife.uniandes.edu.co  |
| Facultad de Ingeniería |  http://ingenieria.uniandes.edu.co  |
| Facultad de Medicina |  http://medicina.uniandes.edu.co  |


Esto se logró utilizando la expresión regular
```
<li><a\s+href="https?://([^"]+uniandes\.edu\.co)[^"]*"\s+[^>]*>([^<]*(Facultad|Centro|Escuela|Departamento)[^<]*)</a></li>
```
Y luego removiendo las repeticiones. En este momento estoy intentando recuperar los enlaces a las distintas páginas de eventos. Con la siguiente expresión regular se han podido filtrar todos los links a otras páginas que contengan las palabras: Eventos, icagenda e icalrepeat. 
```
href=["\']([^\'"]*([Ee]ventos|icagenda|icalrepeat)[^\'"]*)["\']
```
Se filtraron estos links porque todas las unidades parecen tener un link a su página de eventos de esta forma. Sin embargo, algunas unidades tienen mas de un link con estas caracteristicas. A continuación se encuentran los links a la página de eventos de cada unidad:

#### Actualizada en Agosto 23, 18:51
| Unidad académica | URL de eventos | Se encontró |
| ---------------- | -------------- | ----------- |
| Centro Interdisciplinario de Estudios sobre Desarrollo (CIDER) |  http://cider.uniandes.edu.co/Paginas/Eventos.aspx  | Si |
| Centro de Estudios en Periodismo - Ceper | Redirige a  http://eventos.uniandes.edu.co  | Si |
| Departamento de Antropología |  http://antropologia.uniandes.edu.co/index.php/noticias-y-eventos  |
| Departamento de Arquitectura |  http://arquitectura.uniandes.edu.co/eventos/  | Request timeout (Si) |
| Departamento de Arte |  http://arte.uniandes.edu.co/eventos/  | Si |
| Departamento de Ciencia Politica |  https://c-politica.uniandes.edu.co/index.php/noticias-y-eventos  | Si |
| Departamento de Ciencias Biológicas |  https://cienciasbiologicas.uniandes.edu.co/index.php/component/jevents/year.listevents/2016/08/23/-  | Parcial |
| Departamento de Diseño |  http://design.uniandes.edu.co/eventos/  | Request timeout (Si) |
| Departamento de Filosofia |  https://filosofia.uniandes.edu.co/index.php/noticias-y-eventos  | Si |
| Departamento de Fisica |  http://fisica.uniandes.edu.co/index.php/agenda/year.listevents/2016/08/23/-  | Parcial |
| Departamento de Geociencias | No tiene | No |
| Departamento de Historia |  http://historia.uniandes.edu.co/index.php/noticias-y-eventos  | Si |
| Departamento de Humanidades y Literatura | No tiene | No |
| Departamento de Ingenieria Civil y Ambiental |  http://civil.uniandes.edu.co/eventos  | Si |
| Departamento de Ingeniería Biomédica | No tiene | No |
| Departamento de Ingeniería Eléctrica y Electrónica | No tiene | No |
| Departamento de Ingeniería Industrial |  http://industrial.uniandes.edu.co/informacion-general/ciclo-de-seminarios-iind  | No |
| Departamento de Ingeniería Mecánica | No tiene | No |
| Departamento de Ingeniería Química |  http://ingquimica.uniandes.edu.co/eventos  | Si |
| Departamento de Ingeniería de Sistemas y Computación |  http://sistemas.uniandes.edu.co/es/inicio/eventos  | Si |
| Departamento de Lenguas y Cultura |  http://lenguas.uniandes.edu.co/index.php/noticias/eventos-futuros  | No |
| Departamento de Matemáticas |  http://matematicas.uniandes.edu.co/index.php/evento  | No |
| Departamento de Musica | No tiene | No
| Departamento de Psicología |  http://psicologia.uniandes.edu.co/index.php/noticias/eventos-futuros  | No |
| Departamento de Química |  http://quimicapr.uniandes.edu.co/index.php?option=com_jevents&task=year.listevents&year=2016&month=08&day=23&Itemid=1  | No |
| Escuela de Gobierno Alberto Lleras Camargo |  http://egob.uniandes.edu.co/index.php/es/me-noticias-y-eventos/me-eventos/month_calendar/2016/08/-  | Si |
| Facultad de Administración |  http://administracion.uniandes.edu.co/index.php/es/facultad/sobre-la-facultad/eventos/cat.listevents/2016/08/23/-  | Si |
| Facultad de Arquitectura y Diseño |  http://arqdis.uniandes.edu.co/eventos/  | Request timeout (Si) | 
| Facultad de Artes y Humanidades |  http://facartes.uniandes.edu.co/index.php/eventos/day.listevents/2016/08/23/-  | Si |
| Facultad de Ciencias |  http://ciencias.uniandes.edu.co/eventos  | Si |
| Facultad de Ciencias Sociales |  http://faciso.uniandes.edu.co/index.php?option=com_icagenda&view=list&Itemid=504  | Si |
| Facultad de Derecho |  http://derecho.uniandes.edu.co/es/facultad/eventos/month.calendar/2016/08/23/-  | Si |
| Facultad de Economía |  http://economia.uniandes.edu.co/facultad/eventos-economia/cat.listevents/2016/08/23/-  | Si |
| Facultad de Educación |  http://cife.uniandes.edu.co  | No |
| Facultad de Ingeniería |  http://ingenieria.uniandes.edu.co/Paginas/Eventos.aspx  | Si |
| Facultad de Medicina |  http://medicina.uniandes.edu.co/index.php/es/facultad/eventos/proximos.display/2016/08/23/-  | Si |
