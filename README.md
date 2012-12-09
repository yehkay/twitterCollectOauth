twitterCollectOauth
===================

## oauth_stream_collect.py
* Feeds on twitter sample stream (<a href="https://dev.twitter.com/docs/api/1.1/get/statuses/sample">GET statuses/sample</a>)
* collects the tweets every hour in a new file (yyyy-mm-dd-hh.json)
* Uses oAuth
* Uses <a href='http://twistedmatrix.com/trac/'>twisted</a> an event driven networking engine in Python

## Install dependencies

       Twisted==11.0.0
       httplib2==0.7.4
       oauth2==1.5.170
       pyOpenSSL==0.13
       wsgiref==0.1.2
       zope.interface==3.6.3
      
## Get the oAuth credentials
* Register an application with Twitter here: https://dev.twitter.com/apps/new
* Fill in your details. All details are mandatory.
* Your website can be fictional, but it does require a http:// prefix. Make sure you select 'Client' as the application type. You only need Read-only permissions.
* At the application settings page take note of your consumer key, consumer secret, Access token and Access token secret
* Add these four values to the top of the oauth_stream_collect.py script. Search for 'consumer key', 'consumer secret', 'access token' and 'access token secret' and replace with appropriate values inside quotes.

## Running the script
* Start the script from the folder where the tweets should be saved

    ```python oauth_stream_collect.py```
* The tweets will be saved in the file yyyy-mm-dd-hh.json. A new file will be created every one hour

## Parsing the JSON files
#### A simple way to parse the json files (replace yyyy-mm-dd-hh.json with the filename.) Run this script from the folder where the json files are stored.

       import json
       tweets = []
       for line in open('yyyy-mm-dd-hh.json'):
        try: 
          tweets.append(json.loads(line))
        except:
          pass
          
#### This creates a list of json objects called tweets[] which can be manipulated depending on the use case. Some examples:

        print len(tweets)   #print the length of the tweets list
        
        tweet = tweets[0]   #look at a single tweet
        print tweet

#### This <a href='http://mike.teczno.com/notes/streaming-data-from-twitter.html'>Blog Post</a> by Michal Migurski demonstrates how to convert this tweets list into a .csv file which can easily be read by Excel, MySql etc,.
      