# Usb-Config
Usb-Config è uno script per configurare l'indirizzo IP statico di un computer usando una chiavetta contenente un file **config.json**.

Il programma viene eseguito all'avvio del computer e rimane in attesa per 30 minuti che un supporto usb venga collegato.

Quando il supporto viene collegato per prima cosa viene controllato se è presente il file config.json, un file di configurazione composto in questo modo:

```json
[
  {
    "ip":           "172.0.0.13",
    "login":        "admin",
    "password":     "admin123"
  },
  {
    "ip":           "172.0.0.13",
    "login":        "admin",
    "password":     "admin123"
  },
  {
    "ip":           "172.0.0.11",
    "port":         10000
  },
  {
    "ip":           "172.0.0.15",
    "mask":         "255.255.255.0",
    "gateway":      "172.0.0.1"
  }
]
```

I quattro blocchi fannno riferimento rispettivamente a.

1. telecamera 1;
2. telecamera 2;
3. indirizzo del CN;
4. configurazione del PC.

Se il file è presente il programma imposta l'indirizzo IP sul PC, poi copia il file **config.json** nel Desktop del PC per la configurazione del programma per le telecamere e infine torna ad aspettare un altro collegamento con un dispositivo USB (fino allo scadere dei 30 minuti)

### Eseguibile
Per eseguire **usb-config.py** viene usato un file batch che punta all'interprete di python che si vuole usare e al file python da eseguire. Il file batch viene eseguito tramite un collegamento con **permessi di amministrazione** creto in [questo modo](https://www.tenforums.com/tutorials/57690-create-elevated-shortcut-without-uac-prompt-windows-10-a.html). 
