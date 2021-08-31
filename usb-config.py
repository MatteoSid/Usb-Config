from threading import Thread
from pathlib import Path
import win32file as wf
import subprocess
import logging
import shutil
import time
import json
import sys
import os

logging.basicConfig(format='[%(levelname)s][%(asctime)s]: %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S',
                    #filename=r"C:\Users\PARPAS\Desktop\usb-config\usb-config.log",
                    filename=r"C:\Users\Parpas Matteo Donato\Documents\GitHub\usb-config\usb-config.log",
                    level=logging.INFO
                    )
logging.info('\n\n------------------------\nusb-config avviato.')

print(
    '''
    USB-CONFIG

    Inserire un supporto usb con il file config.json per la configurazione della rete e del 
    software per la gestione delle telecamere.
    '''
)

# funzione per caricare i dizionari presenti nel file
def load_data(fname):
    with open(fname) as f:
        return json.load(f)

# restituisce una lista di dispositivi USB collegati
def locate_usb():
    drive_list = []
    drivebits = wf.GetLogicalDrives()
    for d in range(1, 26):
        mask = 1 << d
        if drivebits & mask:
            # here if the drive is at least there
            drname = '%c:\\' % chr(ord('A') + d)
            t = wf.GetDriveType(drname)
            if t == wf.DRIVE_REMOVABLE:
                drive_list.append(drname)
    return drive_list
    
def timer():
    time.sleep(1800)

t = Thread(target=timer)
t.start()

flag = []

try:
    # tramite un ciclo controllo ogni secondo se viene inserita una chiavetta USB
    while True:

        # ogni volta che flag cambia vuol dire che sono state collegate nuove periferiche
        if locate_usb() != flag:
            flag = locate_usb()
            logging.info(f'Dispositivi rilevati: {flag}')
            print(flag)

            # se flag è diverso dalla lista vuota vuol dire che ci sono dispositivi connessi
            if flag != []:

                # salvo una lista con tutti i file
                files = os.listdir(flag[0])

                #logging.info('Dispositivi rilevati: {}'.format(flag))
                #cerco se tra tutti i file c'è il file di configurazione
                if 'config.json' in files:

                    logging.info('File config.json trovato')
                    # carico il file di configurazione
                    outputs = load_data(flag[0] + "config.json")

                    # divido il file di configurazione in 4 dizionari diversi
                    camera1   = outputs[0]        # parametri per la camera 1 
                    camera2   = outputs[1]        # parametri per la camera 2
                    cn_config = outputs[2]        # parametri per la connessione con il CN
                    pc_config = outputs[3]        # parametri di configurazione del PC

                    logging.info('Parametri file config.json:\n{}\n{}\n{}\n{}'.format(camera1, camera2, cn_config, pc_config))

                    print(camera1)
                    print(camera2)
                    print(cn_config)
                    print(pc_config)
                    
                    # creo il comando che verrà poi eseguito come subprocess
                    staticIP = 'netsh interface ipv4 set address name="Ethernet" static ' + \
                                pc_config['ip'] + ' ' + pc_config['mask'] + ' ' + pc_config['gateway']
                    print(staticIP)

                    command = staticIP.split()
                    subprocess.run(command)

                    # dopo aver impostato il nuovo IP sul computer sposto il file config.json
                    # sul desktop perché poi servirà anche al programma per le telecamere
                    original = Path(flag[0] + "config.json")
                    #target = r'C:\Users\PARPAS\Desktop\config.json'
                    target = r'C:\Users\Parpas Matteo Donato\Desktop\config.json'

                    if os.path.isfile(target):
                        print('Sostituisco il file config.json esistente')
                        os.remove(target)
                    shutil.copyfile(original, target)
        
        if not t.is_alive():
            logging.info('Timeut scaduto')
            sys.exit()

        # faccio la scansione ogni secondo
        time.sleep(1)
except:
    logging.error('Error: {}. {}, line: {}'.format(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno))

    