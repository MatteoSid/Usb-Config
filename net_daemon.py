from pathlib import Path
import win32file as wf
import subprocess
import shutil
import time
import json
import os

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

flag = []

# tramite un ciclo controllo ogni secondo se viene inserita una chiavetta USB
while True:

    # ogni volta che flag cambia vuol dire che sono state collegate nuove periferiche
    if locate_usb() != flag:
        flag = locate_usb()
        print(flag)

        # se flag è diverso dalla lista vuota vuol dire che ci sono dispositivi connessi
        if flag != []:

            # salvo una lista con tutti i file
            files = os.listdir(flag[0])
            
            #cerco se tra tutti i file c'è il file di configurazione
            if 'config.json' in files:

                # carico il file di configurazione
                outputs = load_data(flag[0] + "config.json")

                # divido il file di configurazione in 4 dizionari diversi
                camera1 = outputs[0]        # parametri per la camera 1 
                camera2 = outputs[1]        # parametri per la camera 2
                cn_config = outputs[2]      # parametri per la connessione con il CN
                pc_config = outputs[3]      # parametri di configurazione del PC

                print(camera1)
                print(camera2)
                print(cn_config)
                print(pc_config)
                
                print('netsh interface ipv4 set address name="Ethernet" static ' +
                    pc_config['ip'] + ' ' + pc_config['mask'] + ' ' + pc_config['gateway'])
                
                staticIP = 'netsh interface ipv4 set address name="Ethernet" static ' + \
                            pc_config['ip'] + ' ' + pc_config['mask'] + ' ' + pc_config['gateway']

                command = staticIP.split()
                subprocess.run(command)

                original = Path(flag[0] + "config.json")
                #target = r'C:\Users\PARPAS\Desktop\config.json'
                target = r'C:\Users\Parpas Matteo Donato\Desktop\config.json'

                print(original)
                print(target)

                shutil.copyfile(original, target)
            
    time.sleep(1)