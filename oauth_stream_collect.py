#!/usr/bin/python
import datetime         #
import oauth2 as oauth
import time
from twisted.internet import reactor, protocol, ssl
from twisted.web import http
import simplejson as sj

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
CONSUMER = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)

ACCESS_KEY=''
ACCESS_SECRET=''
ACCESS = oauth.Token(ACCESS_KEY, ACCESS_SECRET)

TWITTER_STREAM_API_HOST = 'stream.twitter.com'
TWITTER_STREAM_API_PATH = '/1.1/statuses/sample.json'



def daemon(tweet):
    '''Loop continuously, saving data to files.''' 
    print tweet
   
class TwitterStreamer(http.HTTPClient):
    def connectionMade(self):
        self.sendCommand('GET', self.factory.url)
        self.sendHeader('Host', self.factory.host)                                                                                                                                                                                                                                                                                                                                                  
        self.sendHeader('User-Agent', self.factory.agent)                                                                                                                            
        self.sendHeader('Authorization', self.factory.oauth_header)
        self.endHeaders()                                                                                                                               

    def handleStatus(self, version, status, message):
        #http status code 200 = success
        if status != '200':
            self.factory.tweetError(ValueError("bad status"))

    def lineReceived(self, line):
        self.factory.tweetReceived(line)

    def connectionLost(self, reason):
        self.factory.tweetError(reason)


class TwitterStreamerFactory(protocol.ClientFactory):
#twitterStreamerFactory(auth_header)
    protocol = TwitterStreamer

    def __init__(self, oauth_header):
        self.url = TWITTER_STREAM_API_PATH
        self.agent = 'Twisted/TwitterStreamer'
        self.host = TWITTER_STREAM_API_HOST
        self.oauth_header = oauth_header

    def clientConnectionFailed(self, _, reason):
        self.tweetError(reason)

    #call back function
    def tweetReceived(self, tweet):
        daemon(tweet)

    def tweetError(self, error):
        print error


def build_authorization_header(access_token):
    #Create and sign our request using our Consumer keys and access tokens. 
    #This indicates to Twitter what application is accessing the API 
    #and which User authorized the access.

    url = "https://%s%s" % (TWITTER_STREAM_API_HOST, TWITTER_STREAM_API_PATH)
    params = {
        'oauth_version': "1.0",
        'oauth_nonce': oauth.generate_nonce(),
        'oauth_timestamp': int(time.time()),
        'oauth_token': access_token.key,
        'oauth_consumer_key': CONSUMER.key
    }

    # Sign the request.
    # For some messed up reason, we need to specify is_form_encoded to prevent
    # the oauth2 library from setting oauth_body_hash which Twitter doesn't like.
    req = oauth.Request(method="GET", url=url, parameters=params, is_form_encoded=True)
    req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), CONSUMER, access_token)

    # Grab the Authorization header
    header = req.to_header()['Authorization'].encode('utf-8')
    print "Authorization header:"
    print "     header = %s" % header
    return header

if __name__ == '__main__':
    global file_dt
    file_dt = datetime.datetime.now()
    # Build Authorization header from the access_token.
    auth_header = build_authorization_header(ACCESS)

    # Twitter stream using the Authorization header.
    # Create a TwistedStreamerFactory object using our Authorization header. 
    # Twisted now has everything it needs to access Twitter.
    twsf = TwitterStreamerFactory(auth_header)
    reactor.connectSSL(TWITTER_STREAM_API_HOST, 443, twsf, ssl.ClientContextFactory()) 
    #(host, port(ssl), factory, contextfactory, timeout, bindaddress)
    
    reactor.run()
    
    
