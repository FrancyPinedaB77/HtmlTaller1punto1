import subprocess
from time import time
from os.path import realpath

def run(command):
    subp = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = subp.communicate()
    return(out)

PATH = realpath('./bin')
dt = 60
now = int(time())
last = now - dt

while True:
    now = int(time())
    if now - last >= dt:
        print(now-last,'seconds since last download... Getting the latest news')
        last = now
        run('sh {}/descargaParalela.sh'.format(PATH))

