# AutoCop, prueba de concepto del Observatorio de Contenidos Audiovisuales (OCA), financiado por la Fundación General de la Universidad de Salamanca [Plan TCUE 2015-2017 Fase 2].
# Investigador principal:
# Carlos Arcila Calderón
# Investigadores:
# Félix Ortega, Javier Amores, Sofía Trullenque, Miguel Vicente, Mateo Álvarez, Javier Ramírez

import json
from kafka import SimpleProducer, KafkaClient
import tweepy
import configparser

twitter_credentials = {
    "consumer_key": "bWzJx7DkIehLPBLsFuB0Q0HeG",
    "consumer_secret": "wYk2PgEqDm0b9h5fHJTM4GGeIqyO9epWck7rHheLa615i2CCid",
    "access_key": "13291482-SeGkyyTUTikUaEM8Q4vnJBHVnsCBR0cz3v6rhMAt1",
    "access_secret": "ZGzaXe68bFwy7hT65Lbpi8WT5lh6cplRUU6FkbEx1IzLz"
}

twitter_parameters = {
    "hashtag": ["#BigData"]
}

kafka_producer_parameters = {
    "batch_send_freq_t": 1000,
    "batch_send_freq_n": 10,
    "topic": twitter_parameters["hashtag"][0][1:],
    "connection_string": "localhost:9092"
}

class TwitterStreamingListener(tweepy.StreamListener):

    def __init__(self, api, kafka_producer_parameters):
        self.api = api
        self.kafka_producer_parameters = kafka_producer_parameters
        super(tweepy.StreamListener, self).__init__()
        client = KafkaClient(kafka_producer_parameters["connection_string"])
        self.producer = SimpleProducer(client, async = True,
                          batch_send_every_n = kafka_producer_parameters["batch_send_freq_t"],
                          batch_send_every_t = kafka_producer_parameters["batch_send_freq_n"])

    def on_status(self, status):
        """ This method is called whenever new data arrives from live stream.
        We asynchronously push this data to kafka queue"""
        msg =  status.text.encode('utf-8')
        try:
            self.producer.send_messages(kafka_producer_parameters["topic"], msg)
        except Exception as e:
            print(e)
            return False
        return True

    def on_error(self, status):
        # Error in Kafka producer
        print(status)
        return True

    def on_timeout(self):
        print("Timeout on twitter API")
        return True # Don't kill the stream

# Create Auth object
auth = tweepy.OAuthHandler(twitter_credentials["consumer_key"], twitter_credentials["consumer_secret"])
auth.set_access_token(twitter_credentials["access_key"], twitter_credentials["access_secret"])
api = tweepy.API(auth)

# Create stream and bind the listener to it
stream = tweepy.Stream(auth, listener = TwitterStreamingListener(api, kafka_producer_parameters))

#Custom Filter rules pull all traffic for those filters in real time.
stream.filter(track=twitter_parameters["hashtag"])
#stream.filter(track = twitter_parameters["hashtag"], languages = ['es'])
