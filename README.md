# ChatRoom | Python

## 📌 Sommaire
1. [Description du Projet](#📋-description)
2. [Fonctionalités](#🌟-fonctionalités)
3. [Utilisation](#💻-utilisation)

## 🎯 Badges

[![License MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Protocol TCP](https://img.shields.io/badge/Protocol-TCP/IP-red.svg)](https://www.ibm.com/docs/fr/aix/7.3?topic=protocol-tcpip-protocols)
[![Langage Python](https://img.shields.io/badge/Langage-Python-blue.svg)](https://www.python.org)

## 📋 Description

Ce projet a pour but de mettre en place une ChatRoom utilisant le protocol TCP/IP afin de communiquer du texte et des images.
Les communications sont encodées à l'aide d'un encodage maison.

## 🌟 Fonctionalités

- Lancer une ChatRoom et la rejoindre

- Communication via le protocol TCP/IP

- Changer le type de données envoyer (Image ou Texte)

- Encodage maison

## 💻 Utilisation

### Lancement du serveur :

```bash
py chat_server.py
```


### Lancement d'un client :

```bash
py chat_client.py
```

### Changement de type de données :

| Entrée  | Action |
| :--------------- | -----:|
| **UPLOAD** | Changement vers le mode transfert d'image. |
| **TEXT** | Changement vers le mode transfert de texte. |
| **msg** | En mode texte demande un message, en mode upload demande le chemin vers une image. |
