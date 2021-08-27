# Usb-config
Script per configurare l'indirizzo IP statico di un computer usando una chiavetta contenente un file **config.json**.

Il programma viene eseguito all'avvio del computer e rimane in attesa fino a qunando viene collegata una chiavetta USB. 

Quando la chiavetta viene collegata per prima cosa viene controllato se è presente il file config.json, un file di configurazione composto in questo modo:

```json
[
  {
    "ip": "172.0.0.13",
    "login": "admin",
    "password": "admin123"
  },
  {
    "ip": "172.0.0.13",
    "login": "admin",
    "password": "admin123"
  },
  {
    "ip": "172.0.0.11",
    "port": 10000
  },
  {
    "ip": "172.0.0.15",
    "mask": "255.255.255.0",
    "gateway": "172.0.0.1"
  }
]
```

I quattro blocchi fannno riferimento rispettivamente a.

1. telecamera 1;
2. telecamera 2;
3. indirizzo del CN;
4. configurazione del PC.

Per prima cosa il programma imposta l'indirizzo IP sul PC, poi copia il file **config.json** nel Desktop del PC per la configurazione del programma per le telecamere e infine torna ad aspettare un altro collegamento con un dispositivo USB.
