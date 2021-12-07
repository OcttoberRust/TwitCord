import discord
import os
import time
import discord.ext
import DBConnections
import twitterbot
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
#^ basic imports for other features of discord.py and python ^

client = discord.Client()

client = commands.Bot(command_prefix = '!') #put your own prefix here

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  

    
@client.command()
async def ping(ctx):
    await ctx.send("pong!") #simple command so that when you type "!ping" the bot will respond with "pong!"


@client.command()
async def test(ctx, arg):
  await ctx.send(arg)


@client.event
async def on_message(message):
  if message.author == client:
    return

  msg = message.content


async def disclient_run():
  print("working maybe?")
  client.run(os.getenv("DISCORD_TOKEN"))

print("from discordbot py")  




def pull_from_twt_db():
  print()
  #pull from db and print to channel
  db_connection = DBConnections.create_connection("localhost", "root", "")
  cursor_object = db_connection.cursor()
  sql = "use sys"
  cursor_object.execute(sql)
  sql = "SELECT * FROM TWEET_INFO_TEST ORDER BY twt_created_at ASC;"

  cursor_object.execute(sql)
  rows = cursor_object.fetchall()
  for row in rows:
    print (row[0])
    print (row[1])
    print (row[2])
    print (row[3])
    print (row[9])

  db_connection.close()
  return rows
    
def db_maintain_latest():
  #run script to keep latest date for each user
  print()
  db_connection = DBConnections.create_connection("localhost", "root", "")
  cursor_object = db_connection.cursor()
  sql = "use sys"
  cursor_object.execute(sql)
  
  sql = ("DELETE TWEET_INFO_TEST"
         "FROM TWEET_INFO_TEST" 
         "INNER JOIN("
         "  SELECT *, max(twt_created_at) as last_date  FROM TWEET_INFO_TEST"
				 "  GROUP BY twt_author_id"
         "  HAVING COUNT(*) > 0) TTB on TTB.twt_author_id=TWEET_INFO_TEST.twt_author_id" 
         "  WHERE TWEET_INFO_TEST.twt_created_at < TTB.last_date;"
         )

  cursor_object.execute(sql)
  db_connection.close()
  


@tasks.loop(seconds=5.0)
async def test_loop_message():
    await client.wait_until_ready()
    print("in test_loop discord")
    
    twitterbot.tweet_grab_cycle()
    rows_from_db = pull_from_twt_db()

    for row in rows_from_db:
      channel = client.get_channel(int(os.getenv("DISC_TESTCH_GEN_ID")))
      await channel.send(row[9])
      print("sending to channel: " + row[9])
    
    db_maintain_latest()
    




"""
@test_loop_message.before_loop
async def before_cycle():
      twitterbot.initial_tweet_grab()
      print('before loop waiting...')
      await client.wait_until_ready()"""

#auto_send.start()
#client.run(os.getenv("DISCORD_TOKEN"))
 #get your bot token and create a key named `TOKEN` to the secrets panel then paste your bot token as the value. 
#to keep your bot from shutting down use https://uptimerobot.com then create a https:// monitor and put the link to the website that appewars when you run this repl in the monitor and it will keep your bot alive by pinging the flask server
#enjoy!