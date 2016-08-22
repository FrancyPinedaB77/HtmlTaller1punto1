import sys
from lxml.etree import parse, Element, ElementTree, SubElement

name = sys.argv[1]
file = open(name)
doc = parse(file)
file.close()
n = name[4:name.find('.')]
root = Element('feed', num=n)
i = 1000*int(n)
for df in doc.xpath('//item'):
    item = SubElement(root,'item')
    SubElement(item,'id').text = str(i)
    SubElement(item,'title').text = df.find('title').text
    SubElement(item,'pubDate').text = df.find('pubDate').text
    SubElement(item,'link').text = df.find('link').text
    desc = df.find('lead')
    if desc is not None: SubElement(item,'description').text = desc.text
    else: SubElement(item,'description').text = df.find('description').text
    categorias = df.findall('category')
    if len(categorias) > 0:
        for c in categorias:
            SubElement(item,'category').text = c.text
    else: SubElement(item,'category').text = df.getparent().find('title').text
    i+=1
outFile = open(name, 'wb')
ElementTree(root).write(outFile, xml_declaration=True, encoding='utf-16') 
outFile.close()
