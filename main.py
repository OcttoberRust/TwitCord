import os
import time
import discordbot
import twitterbot

disclient = discordbot.discord.Client()

disclient = discordbot.commands.Bot(command_prefix = '!') #put your own prefix here

"""tapi = twitterbot.api"""
tclient = twitterbot.tclient

"""
public_tweets = twitterbot.home_timeline()

for tweet in public_tweets:
    print(tweet.text)
    
"""

certain_user_id = tclient.get_user(username="twitcordtestbot").data.id

"""for info in certain_user:
    print(info)
"""
print("\n\n\n\n")
print(certain_user_id)

users_following = tclient.get_users_following(id=certain_user_id)

for user in users_following.data:
  print(user.id)

  

"""import discord
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
#^ basic imports for other features of discord.py and python ^



@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

    
@client.command()
async def ping(ctx):
    await ctx.send("pong!") #simple command so that when you type "!ping" the bot will respond with "pong!"



@client.event
async def on_message(message):
  if message.author == client:
    return

  msg = message.content

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  options = starter_encouragements
  if "encouragements" in db.keys():
    options = options + db["encouragements"]

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ", 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
"""

disclient.run(os.getenv("DISCORD_TOKEN")) #get your bot token and create a key named `TOKEN` to the secrets panel then paste your bot token as the value. 
#to keep your bot from shutting down use https://uptimerobot.com then create a https:// monitor and put the link to the website that appewars when you run this repl in the monitor and it will keep your bot alive by pinging the flask server
#enjoy!