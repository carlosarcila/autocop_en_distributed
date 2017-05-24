# autocop_es_distributed
## AutoCop in English to run in Spark. 
This tool runs supervised sentiment analysis in Spark using the streaming of Twitter. Tweets are filtered by a word or hashtag and are  classified in real-time. Positive or negative sentiments are trained with algortithms contained in MlLib. Kakfa and Zookeeper are used to conect to the Twitter stream. Tweets and sentiments are stored in no-Sql MongoDB and can be visualized in real-time. All scripts can run in Amanzon Web Services for Big Data challenges.
