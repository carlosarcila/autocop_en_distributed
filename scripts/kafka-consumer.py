# AutoCop, prueba de concepto del Observatorio de Contenidos Audiovisuales (OCA), financiado por la Fundación General de la Universidad de Salamanca [Plan TCUE 2015-2017 Fase 2].
# Investigador principal:
# Carlos Arcila Calderón
# Investigadores:
# Félix Ortega, Javier Amores, Sofía Trullenque, Miguel Vicente, Mateo Álvarez, Javier Ramírez

import os
import datetime
import pyspark
from pyspark import SparkConf
from pyspark.sql.functions import lit
from pyspark import SparkConf



conf = SparkConf()
sc = pyspark.SparkContext(appName="streaming_app", conf=conf).getOrCreate()
spark = pyspark.sql.SparkSession(sc)

from pyspark.streaming import StreamingContext
ssc = StreamingContext(sc, 10)

kafka_configuration_params = {
    "topic": ["BigData"],
    "connectionstring": "<kafka-hostname>:<kafka-port>"
}

from pyspark.streaming.kafka import KafkaUtils
directKafkaStream = KafkaUtils.createDirectStream(
    ssc, kafka_configuration_params["topic"],
    {"metadata.broker.list": kafka_configuration_params["connectionstring"]})

from pyspark.mllib.classification import SVMModel, LogisticRegressionModel, NaiveBayesModel

# LR_model = LogisticRegressionModel.load(sc, "../../notebooks/LR_model")
# SVM_model = SVMModel.load(sc, "../../notebooks/SVM_model")
# NB_model = NaiveBayesModel.load(sc, "../../notebooks/NB_model")

LR_model = LogisticRegressionModel.load(sc, "<path-to-LR-model>")
SVM_model = SVMModel.load(sc, "<path-to-SVM-model>")
NB_model = NaiveBayesModel.load(sc, "<path-to-NB-model>")


import nltk
import random
from nltk.tokenize import word_tokenize

#allowed_word_types = ["JJ"]
allowed_word_types = ["<selected-word-type>"]

#rdd_all_words = sc.textFile("../../notebooks/all_words/part-00000")
rdd_all_words = sc.textFile("<path-to-words-file>")
rdd_broadcast_all_words = sc.broadcast(rdd_all_words.collect())

def convert_tweet_to_instance(tweets):

    rdd_tweets = tweets.map( \
    lambda tweet: [word[0] for word in nltk.pos_tag(word_tokenize(tweet)) if word[1] in allowed_word_types])

    rdd_instances = rdd_tweets.map(lambda instance: find_features(instance))

    return rdd_instances

def find_features(instance):
    features = []
    for word in rdd_broadcast_all_words.value:
        if word in instance:
            features.append(1)
        else:
             features.append(0)
    return features

rdd_input = directKafkaStream.map(lambda output: output[1])

instances = convert_tweet_to_instance(rdd_input)

classification = instances.map(lambda instance: SVM_model.predict(instance))

classification.pprint()

ssc.start()
ssc.awaitTermination()
