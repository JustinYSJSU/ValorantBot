#author: Justin Yamamoto
#date: 10/1/2022
#Creates a connection to Discord: Creates an instance
#of Client, which represents a connection of Discord

import os
import discord
from dotenv import load_dotenv

from aiohttp import request

#allows your bot to actually function as a bot
#bot is a subclass of Client
from discord.ext import commands 
from discord import Embed

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') #get DISCORD_TOKEN from .env file
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
#client = discord.Client(intents=intents)

#setup the bot, the command prefix is !
botObj = commands.Bot(command_prefix='!', intents = intents)

#on_ready() is called when client 
#is ready for further action 
#essentially this is what happens when the bot connects 
#it's an "event", as indicated by the client.event wrapper
#an event is something that happens on Discord that you can
#use to trigger a bot action
@botObj.event
async def on_ready():
 print(f'{botObj.user.name} has connected to Discord!') #successful connection
 #print all guilds the bot is in
 #uses discord.utills.get, which takes two parameters
 #where you serach, what you search for
 guild = discord.utils.get(botObj.guilds, name = GUILD)
 print(
     f'{botObj.user.name} is connected to the following guild: \n'
     f'{guild.name}(id: {guild.id})'
 
 )
 
 #get all members of the server using Discord API
 members = '\n - '.join([member.name for member in guild.members])
 print(f'Guild Members:\n - {members}')

#Sends a link to the offical VALORANT website
@botObj.command(name='valorant',brief = 'use !help valorant for more info', help='Link to the official VALORANT website')
async def valorant(ctx):
 url = "https://playvalorant.com/"
 await ctx.send(url)

#dictionary of all agents (up to Harbor) and their corresponding uuid
#for API data access
agent_uuid_dict = {
 "astra": "41fb69c1-4189-7b37-f117-bcaf1e96f1bf", 
 "breach": "5f8d3a7f-467b-97f3-062c-13acf203c006", 
 "brimstone": "9f0d8ba9-4140-b941-57d3-a7ad57c6b417", 
 "chamber": "22697a3d-45bf-8dd7-4fec-84a9e28c69d7", 
 "cypher": "117ed9e3-49f3-6512-3ccf-0cada7e3823b", 
 "fade": "dade69b4-4f5a-8528-247b-219e5a1facd6", 
 "jett": "add6443a-41bd-e414-f6ad-e58d267f4e95", 
 "kay/o": "601dbbe7-43ce-be57-2a40-4abd24953621", 
 "killjoy": "1e58de9c-4950-5125-93e9-a0aee9f98746", 
 "neon": "bb2a4828-46eb-8cd1-e765-15848195d751", 
 "omen": "8e253930-4c05-31dd-1b6c-968525494517", 
 "phoenix": "eb93336a-449b-9c1b-0a54-a891f7921d69", 
 "raze": "f94c3b30-42be-e959-889c-5aa313dba261", 
 "reyna": "a3bfb853-43b2-7238-a4f1-ad90e9e46bcc", 
 "sage": "569fdd95-4d10-43ab-ca70-79becc718b46", 
 "skye": "6f2a04ca-43e0-be17-7f36-b3908627744d", 
 "sova": "ded3520f-4264-bfed-162d-b080e2abccf9",
 "viper": "707eab51-4836-f488-046a-cda6bf494859", 
 "yoru": "7f94d92c-4234-0a36-9646-3a87eb8b5c89",
 }

#Lists all agents in VALORANT
@botObj.command(name = 'agents', brief = 'use !help agents for more info', help = 'Lists all playable agents in VALORANT')
async def agents(ctx):
 agents = """```Here are all the currently playable agents in VALORANT \n  \nDUELIST: Phoenix, Jett, Yoru, Reyna, Raze, Neon \nINITIATOR: Breach, Fade, KAYO, Skye, Sova \nCONTROLLER: Astra, Brimstone, Omen, Viper \nSENTINEL: Chamber, Cypher, Killjoy, Sage \n \nFor more information on an agent, use the !agent <name> command```"""
 await ctx.send(agents)


@botObj.command(name = 'agent', brief = "use !help agent for more info", help =  "Format: !agent <name>. Lists agent name, description, abilities")
async def agent(ctx, agent: str):
 if agent.lower() in agent_uuid_dict.keys(): #valid agent name
  uuid = agent_uuid_dict[agent.lower()] #get uuid
  URL = f"https://valorant-api.com/v1/agents/{uuid}"
  async with request("GET", URL) as response: #getting API data
   if response.status == 200: #success
    all_data = await response.json()
    data = all_data["data"]

    #get data for agent name, description, portrait and abilities
    agent_name = data["displayName"]
    agent_description = data["description"]
    agent_role = data["role"]
    agent_class = agent_role["displayName"]

    if agent.lower() == "sova":
     agent_image = "https://media.valorant-api.com/agents/320b2a48-4d9b-a075-30f1-1f93a9b638fa/fullportrait.png"
    else:
     agent_image = data["fullPortrait"]

    agent_abilities = data["abilities"]

    #separating abilites: E ability, Q ability, C ability, Ulimate (X) ability

    #E
    agent_ability_one_name = agent_abilities[0]["displayName"] 
    agent_ability_one_description = agent_abilities[0]["description"]

    #C
    agent_ability_two_name = agent_abilities[1]["displayName"]
    agent_ability_two_description = agent_abilities[1]["description"]

    #Q
    agent_ability_three_name = agent_abilities[2]["displayName"]
    agent_ability_three_description = agent_abilities[2]["description"]

    #Ultimate (X)
    agent_ultimate_ability_name = agent_abilities[3]["displayName"]
    agent_ultimate_ability_description = agent_abilities[3]["description"]

    embed = Embed(title = agent_name + f" ({agent_class})", description = agent_description)
    embed.add_field(name = chr(173), value = chr(173))
    embed.set_image(url = agent_image)
    embed.add_field(name = "Ability: " +  agent_ability_one_name, value = agent_ability_one_description, inline = False)
    embed.add_field(name = "Ability: " + agent_ability_two_name, value = agent_ability_two_description, inline = False)
    embed.add_field(name = "Ability: " + agent_ability_three_name, value = agent_ability_three_description, inline = False)
    embed.add_field(name = "Ultiamte Ability: " + agent_ultimate_ability_name, value = agent_ultimate_ability_description, inline = False)
    embed.add_field(name = chr(173), value = chr(173))
    await ctx.send(embed = embed)
   else:
    print("failed call")
 else:
  await ctx.send("Invalid agent name. Use !agents for a list of available agents")

#Here is how Discord handles errors 
@botObj.event
async def on_error(event, *args, **kwargs):
 with open('err.log', 'a') as f:
  if event == 'on_message':
   f.write(f'Unhandled message: {args[0]}\n')
  else:
   raise

botObj.run(TOKEN)
