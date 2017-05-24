# AutoCop, prueba de concepto del Observatorio de Contenidos Audiovisuales (OCA), financiado por la Fundación General de la Universidad de Salamanca [Plan TCUE 2015-2017 Fase 2].
# Investigador principal:
# Carlos Arcila Calderón
# Investigadores:
# Félix Ortega, Javier Amores, Sofía Trullenque, Miguel Vicente, Mateo Álvarez, Javier Ramírez

#!/bin/bash
# install python35
yum -y install python35
# install pip3
wget -O /tmp/get-pip.py https://bootstrap.pypa.io/get-pip.py
/usr/bin/python35 /tmp/get-pip.py
# install necessary libraries
/usr/local/bin/pip3.5 install nltk
# download nltk corpus and tokenizers
echo "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')" >> download_nltk.py
chmod +x download_nltk.py
/usr/bin/python35 download_nltk.py
cp -rp /root/nltk_data /home/nltk_data
