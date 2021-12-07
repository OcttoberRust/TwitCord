import os
import time
import threading
import discordbot
import twitterbot
from replit import db
import DBConnections


"""tapi = twitterbot.api"""
#tclient = twitterbot.tclient

"""
public_tweets = twitterbot.home_timeline()

for tweet in public_tweets:
    print(tweet.text)
    
"""

#twitterbot.check_for_new_follows()


#twitterbot.tweet_grab_cycle()

#disc_processing_thread = threading.Thread(target=discordbot.disclient_run)
#disc_processing_thread.start()
#disc_processing_thread.join()

twit_processing_thread = threading.Thread(target=twitterbot.initial_tweet_grab)
fact_processing_thread = threading.Thread(target=twitterbot.test_while)

twit_processing_thread.start()
#fact_processing_thread.start()
twit_processing_thread.join()
#fact_processing_thread.join()



discordbot.test_loop_message.start()
discordbot.client.run(os.getenv("DISCORD_TOKEN")) #get your bot token and create a key named `TOKEN` to the secrets panel then paste your bot token as the value. 
#to keep your bot from shutting down use https://uptimerobot.com then create a https:// monitor and put the link to the website that appewars when you run this repl in the monitor and it will keep your bot alive by pinging the flask server
#enjoy!

#discordbot.auto_send()