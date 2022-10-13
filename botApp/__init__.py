from discord.ext.commands import Bot as BotBase
import discord

prefix = "!" #command prefix
owner_ids = [229268111080161290] #my discord id

class Bot(BotBase):
 def __init__(self):
  self.prefix = prefix 
  self.guild = None
  self.ready = False

  super().__init__(command_prefix = prefix, owner_ids = owner_ids, intents = discord.Intents.default())
    
 def run(self, version):
  self.VERSION = version
  
  with open("./botApp/token.0", "r", encoding = "utf-8") as tf:
   self.TOKEN = tf.read()

  print("running bot...")
  super().run(self.TOKEN, reconnect = True)
 async def on_connect(self):
  print("Bot has connected")

 async def on_ready(self):
  if not self.ready:
   self.ready = True
   print("Bot is ready")
  else:
   print("Bot reconnecing")

 async def on_disconnect(self):
  print("Bot has disconnected")

bot = Bot()
