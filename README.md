# ValorantBot
A Discord bot that gives information about VALORANT, including agents, maps, weapons, and players 

Developed with Python and hosted online with Replit 

Want to add this bot to your server? [Click here](https://discord.com/api/oauth2/authorize?client_id=1026641128004517959&permissions=8&scope=bot)

# Goal
The goal of this project was to learn how to use a more complex API and create a bot that 
can provide users with easy access to userful VALORANT information. 

# Commands
- !valorant: Links to the official VALORANT website
- !agents: Lists all currently playable agents in VALORANT (As of 5/2023)
- !agent (name): Lists information about the specified VALORANT agent (name, description, abilities, agent portrait)
- !maps: Lists all currently playable maps in VALORANT (As of 5/2023)
- !map (name): Lists information about the specified VALORANT map (name, coordinates, thunbnail, map image)
- !weapons: Lists all currently useable weapons in VALORANT (As of 5/2023)
- !weapon (name): Lists informaiton about the specified VALORANT weapon (name, magazine count, fire rate, cost, damage ranges)
- !player (name) (tag): Lists information about the specified player, given name and tag. If the name is more than one word, seperate each with with a "_" 
- !rank (region) (name) (tag): Lists current and peak ranking of the specified player. If the name is more than one word, seperate each with with a "_" 
- !history (region) (name) (tag): Lists the 5 most recent matches and stats of the specified palyer. If the name is more than one word, seperate each with with a "_" 

# Command Examples
- !agent Phoenix will list information about Phoenix
- !map Ascent will list information about Ascent
- !weapon Vandal will list information about the Vandal
- !player kigeki 3445 will list kigeki's information 
- !rank na kigeki 3445 will list kigeki's rank history 
- !history na SEN_tarik 1337 will list tarik's 5 most recent matches 

# Technologies
- Python
- Discord API
- VALROANT API (https://valorant-api.com/)
- Henrik's Unofficial API (https://docs.henrikdev.xyz/valorant.html) 
- Replit

# Credits
- Justin Yamamoto (@JustinYSJSU)
