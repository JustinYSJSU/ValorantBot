#author: Justin Yamamoto
#date: 10/1/2022
#Creates a connection to Discord: Creates an instance
#of Client, which represents a connection of Discord

import os
import discord
from dotenv import load_dotenv

from aiohttp import request

from webserver import keep_alive

#allows your bot to actually function as a bot
#bot is a subclass of Client
from discord.ext import commands 
from discord import Embed

load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN') #get DISCORD_TOKEN from .env file
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
#client = discord.Client(intents=intents)

#setup the bot, the command prefix is !
botObj = commands.Bot(command_prefix='!', intents = intents)
discord.Game("Type !help for commands")

#Sends a link to the offical VALORANT website
@botObj.command(name='valorant',brief = 'use !help valorant for more info', help='Link to the official VALORANT website')
async def valorant(ctx):
 url = "https://playvalorant.com/"
 await ctx.send(url)

#dictionary of all agents (up to and including Harbor) and their corresponding uuid
#for API data access
agent_uuid_dict = {
 "astra": "41fb69c1-4189-7b37-f117-bcaf1e96f1bf", 
 "breach": "5f8d3a7f-467b-97f3-062c-13acf203c006", 
 "brimstone": "9f0d8ba9-4140-b941-57d3-a7ad57c6b417", 
 "chamber": "22697a3d-45bf-8dd7-4fec-84a9e28c69d7", 
 "cypher": "117ed9e3-49f3-6512-3ccf-0cada7e3823b", 
 "fade": "dade69b4-4f5a-8528-247b-219e5a1facd6", 
 "gekko": "e370fa57-4757-3604-3648-499e1f642d3f",
 "harbor": "95b78ed7-4637-86d9-7e41-71ba8c293152",
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


#dictionary of all maps (up to and including Peral and their corresponding uuid
map_uuid_dict = {
"ascent": "7eaecc1b-4337-bbf6-6ab9-04b8f06b3319", 
"bind": "2c9d57ec-4431-9c5e-2939-8f9ef6dd5cba", 
"breeze": "2fb9a4fd-47b8-4e7d-a969-74b4046ebd53", 
"fracture": "b529448b-4d60-346e-e89e-00a4c527a405", 
"haven": "2bee0dc9-4ffe-519b-1cbd-7fbe763a6047", 
"icebox": "e2ad5c54-4114-a870-9641-8ea21279579a", 
"lotus": "2fe4ed3a-450a-948b-6d6b-e89a78e680a9", 
"pearl": "fd267378-4d1d-484f-ff52-77821ed10dc2", 
"split": "d960549e-485c-e861-8d71-aa9d1aed12a2", 
}

#dictionary of all weapons
weapons_uuid_dict = {
"classic": "29a0cfab-485b-f5d5-779a-b59f85e204a8", 
"shorty": "42da8ccc-40d5-affc-beec-15aa47b42eda", 
"frenzy": "44d4e95c-4157-0037-81b2-17841bf2e8e3", 
"ghost": "1baa85b4-4c70-1284-64bb-6481dfc3bb4e", 
"sheriff": "e336c6b8-418d-9340-d77f-7a9e4cfe0702", 
"stinger": "f7e1b454-4ad4-1063-ec0a-159e56b58941", 
"spectre": "462080d1-4035-2937-7c09-27aa2a5c27a7", 
"bucky": "910be174-449b-c412-ab22-d0873436b21b", 
"judge": "ec845bf4-4f79-ddda-a3da-0db3774b2794", 
"bulldog": "ae3de142-4d85-2547-dd26-4e90bed35cf7", 
"guardian": "4ade7faa-4cf1-8376-95ef-39884480959b", 
"phantom": "ee8e8d15-496b-07ac-e5f6-8fae5d4c7b1a", 
"vandal": "9c82e19d-4575-0200-1a81-3eacf00cf872", 
"marshal": "c4883e50-4494-202c-3ec3-6b8a9284f00b", 
"operator": "a03b24d3-4319-996d-0f8c-94bbfba1dfc7", 
"ares": "55d8a0f4-4274-ca67-fe2c-06ab45efdf58", 
"odin": "63e6c2b6-4a8e-869c-3d4c-e38355226584", 
}

#Lists all agents in VALORANT
@botObj.command(name = 'agents', brief = 'use !help agents for more info', help = 'Lists all playable agents in VALORANT')
async def agents(ctx):
 agents = """```Here are all the currently playable agents in VALORANT \n  \nDUELIST: Phoenix, Jett, Yoru, Reyna, Raze, Neon \nINITIATOR: Breach, Fade, KAY/O, Skye, Sova \nCONTROLLER: Astra, Brimstone, Omen, Viper, Harbor \nSENTINEL: Chamber, Cypher, Killjoy, Sage \n \nFor more information on an agent, use the !agent <name> command \nEx: !agent Chamber```"""
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

    if agent.lower() == "sova":
     agent_image = "https://media.valorant-api.com/agents/320b2a48-4d9b-a075-30f1-1f93a9b638fa/fullportrait.png"
     agent_class = "Initiator"
    else:
     agent_image = data["fullPortrait"]
     agent_class = agent_role["displayName"]
      
    agent_abilities = data["abilities"]

    #separating abilites: E ability, Q ability, C ability, Ulimate (X) ability

    
    agent_ability_one_name = agent_abilities[0]["displayName"] 
    agent_ability_one_description = agent_abilities[0]["description"]

    
    agent_ability_two_name = agent_abilities[1]["displayName"]
    agent_ability_two_description = agent_abilities[1]["description"]

    
    agent_ability_three_name = agent_abilities[2]["displayName"]
    agent_ability_three_description = agent_abilities[2]["description"]

    
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
  await ctx.send("```Invalid agent name. Use !agents for a list of available agents```")

#lists all currently playable maps in VALORANT
@botObj.command(name = 'maps', brief = "use !help maps for more info", help =  "Lists all currently playable maps in VALORANT")
async def maps(ctx):
 maps = """```Here are all the currently playable maps in VALORANT \n  \nAscent \nBind \nBreeze \nFracture \nHaven \nIcebox \nPearl \nSplit \n  \nUse the !map <name> command for more info on a specific map \nEx:!map Ascent```"""
 await ctx.send(maps)

#gives specific information on a specific VALORANT map
@botObj.command(name = 'map', brief = "use !help map for more info", help =  "Format: !map <name>. Lists map name, location, image")
async def agent(ctx, map: str):
 if map.lower() in map_uuid_dict.keys(): #valid agent name
  uuid = map_uuid_dict[map.lower()] #get uuid
  URL = f"https://valorant-api.com/v1/maps/{uuid}"
  async with request("GET", URL) as response: #getting API data
   if response.status == 200: #success
    all_data = await response.json()
    data = all_data["data"]
    map_name = data["displayName"]
    map_coordinates = data["coordinates"]
    map_diagram = data["displayIcon"]
    map_thumbnail = data["listViewIcon"]

    embed = Embed(title = map_name + f" ({map_coordinates})")
    embed.set_image(url = map_diagram)
    embed.set_thumbnail(url = map_thumbnail)
    await ctx.send(embed = embed)
   else:
    print("failed call")
 else:
  await ctx.send("```Invalid map name. Use !maps for a list of available maps```")

#Lists all weapons in VALORANT
@botObj.command(name = 'weapons', brief = 'use !help weapons for more info', help = 'Lists all weapons in VALORANT')
async def weapons(ctx):
 weapons = """```Here are all the weapons in VALORANT \n  \nPISTOL: Classic, Shorty, Frenzy, Ghost, Sheriff \nSMG: Stinger, Spectre \nSHOTGUN: Bucky, Judge \nRIFLE: Bulldog, Guardian, Phantom, Vandal \nSNIPER RIFLE: Marshal, Operator \nHEAVY: Ares, Odin\n \nFor more information on a weapon, use the !weapon <name> command\nEx: !weapon Vandal```"""
 await ctx.send(weapons)

#Get information on a specific weapon in VALORANT
@botObj.command(name = 'weapon', brief = 'use !help weapon for more info', help = 'Lists information about specified weapon (Name, damage, price, image)')
async def weapon(ctx, weapon: str):
 if weapon.lower() in weapons_uuid_dict.keys(): #valid agent name
  uuid = weapons_uuid_dict[weapon.lower()] #get uuid
  URL = f"https://valorant-api.com/v1/weapons/{uuid}"
  async with request("GET", URL) as response: #getting API data
   if response.status == 200: #success
    all_data = await response.json()
    data = all_data["data"]
    weapon_name = data["displayName"]
    weapon_image = data["displayIcon"]

    weapon_shop_data = data["shopData"]
    weapon_price = weapon_shop_data["cost"]

    weapon_stats = data["weaponStats"]
    fire_rate = weapon_stats["fireRate"]
    magazine_count = weapon_stats["magazineSize"]

    weapon_damage = weapon_stats["damageRanges"]

    embed = Embed(title = weapon_name)
    embed.set_image(url = weapon_image)
    embed.add_field(name = "Cost", value = weapon_price, inline = True)
    embed.add_field(name = "Fire Rate (rounds/sec)", value = fire_rate, inline = True)
    embed.add_field(name = "Magazine Size", value = magazine_count, inline = True)

    for range in weapon_damage:
     start_range = range["rangeStartMeters"] 
     end_range = range["rangeEndMeters"]
     headshot = round(range["headDamage"])
     bodyshot = round(range["bodyDamage"])
     legshot = round(range["legDamage"])
     embed.add_field(name = f"Damage range {start_range}m to {end_range}m", value = f"Headshot: {headshot} \nBodyshot: {bodyshot} \nLegshot: {legshot}", inline =  False)

    await ctx.send(embed = embed)
   else:
    print("failed call")
 else:
  await ctx.send("```Invalid weapon name. Use !weapons for a list of available weapons```")

#Get rank information about specified VALORANT player
@botObj.command(name = 'rank', brief = 'use !help rank for more info', help = 'Lists rank information about player. Format: !rank <region> <name> <tag>')
async def rank(ctx, region: str, name: str, tag: str):
 URL = f"https://api.henrikdev.xyz/valorant/v2/mmr/{region}/{name}/{tag}"

 async with request("GET", URL) as response: #getting API data
  if response.status == 200: #success
    all_data = await response.json()
    rank_data = all_data["data"]

    current_data = rank_data["current_data"]
    rank_name = current_data["currenttierpatched"]
    ranked_rating = current_data["ranking_in_tier"]
    images = current_data["images"]
    rank_image = images["small"]

    peak_data = rank_data["highest_rank"]
    peak_rank = peak_data["patched_tier"]
    peak_time = peak_data["season"]

    embed = Embed(title = f"Rank History for {name}#{tag}")
    embed.set_image(url = rank_image)
    embed.add_field(name = "Current Rank", value = f"{rank_name} ({ranked_rating} RR)", inline = True)
    embed.add_field(name = chr(173), value = chr(173))
    embed.add_field(name = "Peak Rank", value = f"{peak_rank} ({peak_time})", inline = False)

    await ctx.send(embed = embed)
  else:
   await ctx.send("```Invalid player name. Remember caps matter; use !help rank for more info```")
     
#Get general information about specified VALORANT player
@botObj.command(name = 'player', brief = 'use !help player for more info', help = 'Lists player name, tag, level, card. If the name is multiple words, separate each word with a "_". Format: !player <name> <tag>')
async def player(ctx, name: str, tag: str):
 URL = f"https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}"
 async with request("GET", URL) as response: #getting API data
  if response.status == 200: #success
   all_data = await response.json()
   player_data = all_data["data"]
   player_cards = player_data["card"]
   player_card = player_cards["large"]
   player_level = player_data["account_level"]

   embed = Embed(title = f"Profile for {name}#{tag}")
   embed.set_image(url = player_card)
   embed.add_field(name = "Level", value = player_level)
   await ctx.send(embed = embed)
  else:
   print(f'{name}')
   await ctx.send("```Invalid player name. Remember caps matter; use !help player for more info```")

#Get the 5 most recent matches of a specified player
@botObj.command(name = 'history', brief = 'use !help history for more info', help = 'Lists the 5 most recent matches for this player. Format: !history <region> <name> <tag>.')
async def history(ctx, region: str, name: str, tag: str):
 URL = f"https://api.henrikdev.xyz/valorant/v3/matches/{region}/{name}/{tag}"
 async with request("GET", URL) as response:
  if response.status == 200:
   all_data = await response.json()
   match_list = all_data["data"] #list of 5 recent matches
   for match in match_list: #go through all the lists
    metadata = match["metadata"] #basic data (map, mode, etc)
    players = match["players"] #all the players (LIST) 
    all_players = players["all_players"]
    teams = match["teams"] #red = attacker start, blue = defended start

    #getting map and mode for match
    map = metadata["map"]
    mode = metadata["mode"]
    embed = Embed(title = f"{name}#{tag}'s Match History")
    embed.add_field(name = "Map", value = map)
    embed.add_field(name = "Mode", value = mode, inline = True)
    
    #get the specific player using the account api 
    URL_2 = f"https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}"
    async with request("GET", URL_2) as response:
     if response.status == 200:
      all_data_player = await response.json()
      player_data = all_data_player["data"]
      puuid = player_data["puuid"]
      for player in all_players: #get the specific player in the given match
       if player["puuid"] == puuid: #found the player
        team = player["team"]
        assets = player["assets"]
        agent = assets["agent"]
        agent_image = agent["small"]

        stats = player["stats"]
        kills = stats["kills"]
        deaths = stats["deaths"]
        assists = stats["assists"]

        win_lost = ""
        if team == 'Red':
         red_info = teams["red"]
         rounds_won = red_info["rounds_won"]
         rounds_lost = red_info["rounds_lost"]

         if bool(red_info["has_won"]) == True:
          win_lost = "Victory"
         else:
          win_lost = "Defeat"

        else:
          blue_info = teams["blue"]
          rounds_won = blue_info["rounds_won"]
          rounds_lost = blue_info["rounds_lost"]

          if bool(blue_info["has_won"]) == True:
           win_lost = "Victory"
          else:
           win_lost = "Defeat"

      embed.add_field(name = "KDA", value = f"{kills}/{deaths}/{assists}", inline = True)
      embed.add_field(name = "Results", value = f"{win_lost} ({rounds_won} - {rounds_lost})", inline = True)
      embed.set_thumbnail(url = agent_image)
    await ctx.send(embed = embed)
  else:
   await ctx.send("```Invalid input. Remember caps matter. Use !help history for more info```")
   

#Here is how Discord handles errors 
@botObj.event
async def on_error(event, *args, **kwargs):
 with open('err.log', 'a') as f:
  if event == 'on_message':
   f.write(f'Unhandled message: {args[0]}\n')
  else:
   raise

keep_alive()
TOKEN = os.environ.get("DISCORD_BOT_SECRET")
botObj.run(TOKEN)
