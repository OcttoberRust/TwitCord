import tweepy
import time
import os
import DBConnections

consumer_key = os.getenv("TWITTER_API_KEY")
consumer_secret = os.getenv("TWITTER_API_KEY_SECRET")

access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

bearer_token = os.getenv("TWITTER_BEARER_TOKEN")


def get_users_tweets_exp_init(tclient, user_id):
  print()
  user_tweets = tclient.get_users_tweets(
        id=user_id,
        exclude=['retweets'],
        expansions = ['author_id','referenced_tweets.id','referenced_tweets.id.author_id','in_reply_to_user_id','attachments.media_keys','entities.mentions.username'],
                       tweet_fields=['id','text','author_id','created_at','conversation_id','entities','public_metrics','referenced_tweets'],
                       user_fields=['id','name','username','created_at','description','public_metrics','verified','profile_image_url'],
                       place_fields=['full_name','id'],
                       media_fields=['type','url','alt_text','public_metrics'])

  return user_tweets

def get_users_tweets_exp_existing(tclient, user_id, tweet_since_id):
  print()
  users_tweets = tclient.get_users_tweets(
        id=user_id, since_id=tweet_since_id,
        exclude=['retweets'],
        expansions = ['author_id','referenced_tweets.id','referenced_tweets.id.author_id','in_reply_to_user_id','attachments.media_keys','entities.mentions.username'],
                       tweet_fields=['id','text','author_id','created_at','conversation_id','entities','public_metrics','referenced_tweets'],
                       user_fields=['id','name','username','created_at','description','public_metrics','verified','profile_image_url'],
                       place_fields=['full_name','id'],
                       media_fields=['type','url','alt_text','public_metrics'])
  return users_tweets


def initial_tweet_grab():

  db_connection = DBConnections.create_connection("localhost", "root", "")
  cursor_object = db_connection.cursor()
  sql = "use sys"
  cursor_object.execute(sql)
  sql = ("INSERT INTO TWEET_INFO_TEST(twt_author_id, twt_id, twt_created_at, twt_text, twt_retweet_count, twt_reply_count, twt_like_count, twt_quote_count, twt_url)"
  "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")


  
  tclient = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)

  certain_user_id = tclient.get_user(username="twitcordtestbot").data.id
  users_following = tclient.get_users_following(id=certain_user_id)

  for user in users_following.data:
      user_id = user.id
      print("user id " + str(user.id))
      users_tweets = get_users_tweets_exp_init(tclient, user_id)


      
      
      for info in users_tweets.data:
        try:
          val = (info.author_id, info.id, info.created_at, info.text, info.public_metrics['retweet_count'], info.public_metrics['reply_count'], info.public_metrics['like_count'], info.public_metrics['quote_count'], "https://twitter.com/twitter/status/" + str(info.id))

          cursor_object.execute(sql,val)
          db_connection.commit()
          

        except KeyError:
          print("KEY ERROR FOR FILL IN THE BLANK LATER")
          #let the query now there was no key for this!
          continue
        except TypeError as e:
          if str(e) == "'NoneType' object is not subscriptable":
            continue
          #elif str(e) == "AttributeError: \'list\' object has no attribute \'url\'" 

        


  db_connection.close()
    

        

def check_for_new_follows(tclient):
  #pull from get_users_followers
  #pull from tweet author ids from db
  #compare and make distinct list of new additions
  #return list of new follows
  db_connection = DBConnections.create_connection("localhost", "root", "")
  cursor_object = db_connection.cursor()
  sql = "use sys"
  cursor_object.execute(sql)

  sql = "SELECT DISTINCT(twt_author_id) FROM TWEET_INFO_TEST;"

  cursor_object.execute(sql)
  rows = cursor_object.fetchall()
  print(rows)

  certain_user_id = tclient.get_user(username="twitcordtestbot").data.id
  users_following = tclient.get_users_following(id=certain_user_id)

  list_of_db_users = []

  list_of_twp_users = []

  for info in rows:
    for user_id in info:
      list_of_db_users.append(int(user_id))
      

  print(list_of_db_users)

 #tweepy will have list of new users
  for info in users_following.data:
    list_of_twp_users.append(info.id)

  print(list_of_twp_users)


  #return only new users
  new_followers_to_add = list(set(list_of_twp_users) - set(list_of_db_users))

  print(new_followers_to_add)
  db_connection.close()
  return new_followers_to_add
  

def tweet_grab_cycle():

  db_connection = DBConnections.create_connection("localhost", "root", "")
  cursor_object = db_connection.cursor()
  sql = "use sys"
  cursor_object.execute(sql)

  tclient = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)

  list_of_new_follows = check_for_new_follows(tclient)
  print(list_of_new_follows)

  sql = ("INSERT INTO TWEET_INFO_TEST(twt_author_id, twt_id, twt_created_at, twt_text, twt_retweet_count, twt_reply_count, twt_like_count, twt_quote_count, twt_url)"
  "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")

  if list_of_new_follows:
    print("TESTING NEW FOLLOWS")
    
    for user in list_of_new_follows:
      print(user)
      user_id = user
      users_tweets = get_users_tweets_exp_init(tclient, user_id)


      for info in users_tweets.data:
        try:
          val = (info.author_id, info.id, info.created_at, info.text, info.public_metrics['retweet_count'], info.public_metrics['reply_count'], info.public_metrics['like_count'], info.public_metrics['quote_count'], "https://twitter.com/twitter/status/" + str(info.id))

          cursor_object.execute(sql,val)
          db_connection.commit()
          

        except KeyError:
          print("KEY ERROR FOR FILL IN THE BLANK LATER")
        
          continue
        except TypeError as e:
          if str(e) == "'NoneType' object is not subscriptable":
            continue
          
      
      


  

    
    
    #just pull from existing
    #pull latest one for each user id
  sql = ("select tt.twt_author_id, tt.twt_id, tt.twt_created_at\n"
            "from TWEET_INFO_TEST as tt\n"
            "where tt.twt_created_at = (SELECT MAX(tt2.twt_created_at)\n"
            "						                FROM TWEET_INFO_TEST as tt2\n"
            "                           WHERE tt2.twt_author_id = tt.twt_author_id)\n"
            )

  cursor_object.execute(sql)
  no_new_follows_list = cursor_object.fetchall()
  print(no_new_follows_list)

  ref_nnfl = []

  for info in no_new_follows_list:
    print(info[0])
    ref_nnfl.append( [int(info[0]) , int(info[1])] )
     

    
    #ref_nnfl stands for refined no new followers list
    #ref_nnfl[0]=author_id
    #ref_nnfl[1]=tweet_id

  for user in ref_nnfl:

    user_id = user[0]
    tweet_since_id = user[1]
    users_tweets = get_users_tweets_exp_existing(tclient, user_id, tweet_since_id)
      

    
    if None == users_tweets.data:
      print("NO DATA in USERS_TWEETS")
      continue

    for info in users_tweets.data:
          print("IN SQL EXECUTE FOR LOOP")
          print("IN SQL EXECUTE FOR LOOP !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
          print("printing info")
          print(info)

          val = (info.author_id, info.id, info.created_at, info.text, info.public_metrics['retweet_count'], info.public_metrics['reply_count'], info.public_metrics['like_count'], info.public_metrics['quote_count'], "https://twitter.com/twitter/status/" + str(info.id))


          print("IN SQL EXECUTE FOR LOOP 2")  
          sql = ("INSERT INTO TWEET_INFO_TEST(twt_author_id, twt_id, twt_created_at, twt_text, twt_retweet_count, twt_reply_count, twt_like_count, twt_quote_count, twt_url)"
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            )
          print("printing val")
          print(val)
          cursor_object.execute(sql,val)
          db_connection.commit()
      
  
   

 
  db_connection.close()


def test_while():
    while True:
      time.sleep(1)
      print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!/n")
      print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!/n")
      print("TESTING TESTING TESTING TESTING TESTING TESTING /n")
      print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!/n")
      print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!/n")
