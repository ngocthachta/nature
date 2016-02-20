#!/bin/bash
# Usage ./sync_iphone4s_thach.sh remote_passwd
# remote_passwd : alpine
# Stockage de la sauvegarde
LOCAL_DIR=/home/nature/backup/iphone4s

#Telephone
REMOTE_IP=192.168.1.19
REMOTE_PORT=22
REMOTE_LOGIN=root
REMOTE_PASSWORD=${1-alpine}
REMOTE_DIR=/User/MyData

#Mode test
#Vide : pas de simulation
#TEST=n : Simulation
TEST=n

#on tente de creer le dossier LOCAL_DIR
mkdir -p $LOCAL_DIR

if [ $? -ne 0 ] ; then
    echo "Erreur a la creation du dossier : $LOCAL_DIR"
    exit 1
fi

#Sauvegarde
sshpass -p $REMOTE_PASSWORD rsync -e "ssh -p $REMOTE_PORT" -avz$TEST $REMOTE_LOGIN@$REMOTE_IP:$REMOTE_DIR $LOCAL_DIR
