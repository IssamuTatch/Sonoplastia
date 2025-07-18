import os
from dotenv import load_dotenv
from discord.ext import commands
import requests
import json


load_dotenv()
RIOT_API_KEY = os.getenv("RIOT_API_KEY")
BaseURL = "https://americas.api.riotgames.com"

def getUserRiotID(name, nametag):
    url = f"{BaseURL}/riot/account/v1/accounts/by-riot-id/{name}/{nametag}"
    headers = {
        "X-Riot-Token": RIOT_API_KEY
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()['puuid']
    elif response.status_code == 401:
        return 401
    if response.status_code == 404:
        return 404
    else:
        print(f"r {response.status_code}: {response.text}")
        return None
    
def getMatchHistory(puuid, index):
    url = f"{BaseURL}/lol/match/v5/matches/by-puuid/{puuid}/ids?start={index}&count=1"
    headers = {
        "X-Riot-Token": RIOT_API_KEY
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"r {response.status_code}: {response.text}")
        return None

def getMatchDetails(match_id):
    url = f"{BaseURL}/lol/match/v5/matches/{match_id}"
    headers = {
        "X-Riot-Token": RIOT_API_KEY
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def filterMatchDetails(match_details):
    s = "```LOL HISTORY\n"
    # Filter Game mode
    gamemode = match_details.get('info', {}).get('gameMode')
    if gamemode not in ["CHERRY", "ARAM", "CLASSIC"]:
        print(f"Unsupported game mode: {gamemode}")
        s = f"{gamemode} isn't Supported."
        return s
    

    if gamemode == "CLASSIC":
        s += "Game Mode: CLASSIC\n"
        s = f"{s}\n{"Summoner".ljust(20)}{"Champion".ljust(14)}{"K/D/A".ljust(9)}{"Damage".rjust(8)}{"Gold".rjust(8)}\n"
        # Order Teams by teamId
        participants = sorted(
                    match_details.get("info", {}).get("participants", []),
                    key=lambda p: p.get("teamId", 0)
                )
        for i, participant in enumerate(participants):
            if i % 5 == 0:
                s += "------------------------------------------------------------\n"
                if i == 0:
                    s += "BLUE TEAM\n"
                else:
                    s += "RED TEAM\n"
            
            riotIdGameName = participant.get('riotIdGameName')
            championName = participant.get('championName')
            kills = participant.get('kills', 0)
            deaths = participant.get('deaths', 0)
            assists = participant.get('assists', 0)
            damage = participant.get('totalDamageDealtToChampions', 0)
            goldEarned = participant.get('goldEarned', 0)
            kda = f"{kills}/{deaths}/{assists}".ljust(9)
            row = f"{riotIdGameName.ljust(20)}{championName.ljust(14)}{kda}{str(damage).rjust(8)}{str(goldEarned).rjust(8)}\n"
            s = f"{s}{row}" 



    elif gamemode == "ARAM":
        s += "Game Mode: ARAM\n"
        s = f"{s}\n{"Summoner".ljust(20)}{"Champion".ljust(14)}{"K/D/A".ljust(9)}{"Damage".rjust(8)}{"Gold".rjust(8)}\n"
        # Order Teams by playerSubteamId
        participants = sorted(
                    match_details.get("info", {}).get("participants", []),
                    key=lambda p: p.get("teamId", 0)
                )
        for i, participant in enumerate(participants):
            if i % 5 == 0:
                s += "------------------------------------------------------------\n"
                if i == 0:
                    s += "BLUE TEAM\n"
                else:
                    s += "RED TEAM\n"
            
            riotIdGameName = participant.get('riotIdGameName')
            championName = participant.get('championName')
            kills = participant.get('kills', 0)
            deaths = participant.get('deaths', 0)
            assists = participant.get('assists', 0)
            damage = participant.get('totalDamageDealtToChampions', 0)
            goldEarned = participant.get('goldEarned', 0)
            kda = f"{kills}/{deaths}/{assists}".ljust(9)
            row = f"{riotIdGameName.ljust(20)}{championName.ljust(14)}{kda}{str(damage).rjust(8)}{str(goldEarned).rjust(8)}\n"
            s = f"{s}{row}"
    
    
    elif gamemode == "CHERRY":
        s += "Game Mode: ARENA\n"
        s = f"{s}\n{"Summoner".ljust(20)}{"Champion".ljust(14)}{"K/D/A".ljust(9)}{"Damage".rjust(8)}{"Gold".rjust(8)}\n"
        # Order Teams by playerSubteamId
        participants = sorted(
                    match_details.get("info", {}).get("participants", []),
                    key=lambda p: p.get("playerSubteamId", 0)
                )
        count = 0
        for i, participant in enumerate(participants):
            if i % 2 == 0:
                s += "------------------------------------------------------------\n"
            
            riotIdGameName = participant.get('riotIdGameName')
            championName = participant.get('championName')
            kills = participant.get('kills', 0)
            deaths = participant.get('deaths', 0)
            assists = participant.get('assists', 0)
            damage = participant.get('totalDamageDealtToChampions', 0)
            goldEarned = participant.get('goldEarned', 0)
            kda = f"{kills}/{deaths}/{assists}".ljust(9)
            row = f"{riotIdGameName.ljust(20)}{championName.ljust(14)}{kda}{str(damage).rjust(8)}{str(goldEarned).rjust(8)}\n"
            s = f"{s}{row}"
    print(s)
    s += "```"
    return s

def setup(bot):
    @bot.command()
    async def lolhistory(ctx, name, nametag, index: int = 0):
        try:
            # Get User Riot ID
            puuid = getUserRiotID(name, nametag)
            if puuid == 401:
                await ctx.send("Unauthorized Key. Call the dev to update it.")
                return
            elif puuid == 404:
                await ctx.send("Error to find Riot ID.\n Please check the name and name tag(Without #).")
                return
            elif not puuid:
                await ctx.send("Some error occurred while getting the Riot ID. Please try again later.")
                return
            
            # Get Match History
            matchList = getMatchHistory(puuid, index)
            if not matchList:
                await ctx.send("No match history found or invalid index.")
                return
            
            # Filter Details
            match_details = getMatchDetails(matchList[0])
            if not match_details:
                await ctx.send("Error to get match details.")
                return
            
            # Filter Match Details, Create Message and send it
            msg = filterMatchDetails(match_details)
            if msg:
                await ctx.send(msg)
            else:
                await ctx.send("No valid match history found or game mode not supported.")

        except Exception as e:
            print(f"An error occurred: {e}")