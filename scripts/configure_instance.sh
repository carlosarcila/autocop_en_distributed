# AutoCop, prueba de concepto del Observatorio de Contenidos Audiovisuales (OCA), financiado por la Fundación General de la Universidad de Salamanca [Plan TCUE 2015-2017 Fase 2]. 
# Investigador principal:
# Carlos Arcila Calderón
# Investigadores:
# Félix Ortega, Javier Amores, Sofía Trullenque, Miguel Vicente, Mateo Álvarez, Javier Ramírez

#!/bin/bash
# install docker
yum install -y docker
# start docker daemon
service docker restart
# add shared volume for data
mkdir /root/data
# start mongodb
docker run -d -P -v /root/data:/data/db --name mongo mongo
# install python35
yum -y install python35
# install pip3
wget -O /tmp/get-pip.py https://bootstrap.pypa.io/get-pip.py
/usr/bin/python35 /tmp/get-pip.py
# install necessary libraries
/usr/local/bin/pip3.5 install kafka tweepy configparser datetime
#download and uncompress kafka
wget -O /tmp/kafka_2.11-0.8.2.2.tgz http://mirror.jax.hugeserver.com/apache/kafka/0.8.2.2/kafka_2.11-0.8.2.2.tgz
tar -xzvf /tmp/kafka_2.11-0.8.2.2.tgz -C /root
# create scripts directory
mkdir /root/scripts
