import datetime
import csv
import pandas as pd
from pip._internal.commands.list import tabulate

import models
from fpl import fpl, FPL
import asyncio
import aiohttp
from flask_login import current_user
import os

os.environ["EMAIL"]="ruben.varghese@ymail.com"
os.environ["PASSWORD"]="Pokemon456"
os.environ["USER_IS"]="819877"

def get_teamid():
    user = models.User.get(models.User.username == 'rv2')
    user_fplID = user.fplID
    print(user_fplID)
    print(current_user)
    return user_fplID


# access the fpl api to get current team
async def update(email, password, user_id):
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        await fpl.login(email, password)
        user = await fpl.get_user(user_id)
        # to get current gameweek from FPL API in order to get most recent team
        gw = await fpl.get_gameweeks(return_json=True)
        df = pd.DataFrame(gw)
        today = datetime.datetime.now().timestamp()
        df = df.loc[df.deadline_time_epoch > today]
        gameweek = df.iloc[0].id
        # gets picks but does not contain useful info
        picks = await user.get_picks(gameweek - 1)
        team = pd.DataFrame(picks)
        # get information like names and cost for picks
        players = [x['element'] for x in team[gameweek - 1]]
        picked_players = []
        for player in players:
            p = await fpl.get_player(player, return_json=True)
            picked_players.append(p)
        picked_players = pd.DataFrame(picked_players)
    return picked_players


def printteam():
    email=os.environ.get('EMAIL')
    password=os.environ.get('PASSWORD')
    user_id=os.environ.get('USER_ID')
    print(asyncio.run(update(email, password,user_id)))


# find predicted point for player
def find_pp(name):
    col_name = ["name", "cost", "s", "ot", "in", "BC", "xG", "G", "KP", "BCC", "xA", "A", "Pts", "predicted", "AFDR"]
    name1 = str(name)
    stat1 = "predicted"
    with open('C:/Users/ruben/Computing Coursework/static/Data/POP.csv',encoding='utf-8-sig', newline='') as csvfile:
        statsreader = csv.DictReader(csvfile, fieldnames=col_name)
        for row in statsreader:
            for name in row.items():
                if name1 == row["name"]:
                    return row[stat1]
                    break


# change name format
def change_name(row):
    x = row[0]
    if row[1] == "Goalkeeper":
        x += "(G)"
    if row[1]=="Defender":
        x += "(D)"
    if row[1]=="Midfielder":
        x += "(M)"
    if row[1]=="Forward":
        x += "(F)"
    if row[2]=="Man City":
        x += "(MCI)"
    if row[2]=="Man Utd":
        x += "(MUN)"
    if row[2]=="Leicster":
        x += "(LEI)"
    if row[2]=="Chelsea":
        x += "(CHE)"
    if row[2]=="West Ham":
        x += "(WHU)"
    if row[2]=="Everton":
        x += "(EVE)"
    if row[2]=="Spurs":
        x += "(THS)"
    if row[2]=="Liverpool":
        x += "(LIV)"
    if row[2]=="Aston Villa":
        x += "(AVL)"
    if row[2]=="Arsenal":
        x += "(ARS)"
    if row[2]=="Leeds":
        x += "(LEE)"
    if row[2]=="Wolves":
        x += "(WOL)"
    if row[2]=="Crystal Palace":
        x += "(CPL)"
    if row[2]=="Southampton":
        x += "(SOU)"
    if row[2]=="Burnley":
        x += "(BUR)"
    if row[2]=="Newcastle":
        x += "(NEW)"
    if row[2]=="Brighton":
        x += "(BHA)"
    if row[2]=="Fulham":
        x += "(FUL)"
    if row[2]=="West Brom":
        x += "(WBA)"
    if row[2]=="Sheffield":
        x += "(SHU)"
    return x

# get predicted points of team
def pp_current():
    email=os.environ.get('EMAIL')
    password=os.environ.get('PASSWORD')
    user_id=os.environ.get('USER_ID')
    df = asyncio.run(update(email, password,user_id))
    df_list = df.values.tolist()
    print(df_list)
    points_list = []
    for list in df_list:
        x = list[0]
        points = find_pp(change_name(list))
        if list[1] == "Goalkeeper":
            x += "(G)"
            points_list.append(x, points)
        if list[1] == "Defender":
            x += "(D)"
            points_list.append(x, points)
        if list[1] == "Midfielder":
            x += "(M)"
            points_list.append(x, points)
        if list[1] == "Forward":
            x += "(F)"
            points_list.append(x, points)
    return points_list


# gets the player in each postion with the highest predicted score
def get_highest():
    col_name = ["name", "cost", "s", "ot", "in", "BC", "xG", "G", "KP", "BCC", "xA", "A", "Pts", "predicted", "AFDR"]
    df = pd.read_csv('C:/Users/ruben/Computing Coursework/static/Data/POP.csv', names=col_name, encoding='utf-8-sig')
    highest_gk =0
    highest_df =0
    highest_mid=0
    highest_fwd=0
    highest = []
    for index, row in df.iterrows():
        if "(G)" in row["name"]:
            if float(row["predicted"]) > highest_gk:
                highest_gk = float(row["predicted"])
        if "(D)" in row["name"]:
            if float(row["predicted"]) > highest_df:
                highest_df = float(row["predicted"])
        if "(M)" in row["name"]:
            if float(row["predicted"]) > highest_mid:
                highest_mid = float(row["predicted"])
        if "(F)" in row["name"]:
            if float(row["predicted"]) > highest_fwd:
                highest_fwd = float(row["predicted"])
    for index, row in df.iterrows():
        if float(row["predicted"]) == highest_gk:
            highest.append(row["name"])
        if float(row["predicted"]) == highest_df:
            highest.append(row["name"])
        if float(row["predicted"]) == highest_mid:
            highest.append(row["name"])
        if float(row["predicted"]) == highest_fwd:
            highest.append(row["name"])
    return highest

def recommend():
    rec = []
    points_list = pp_current()
    highest = get_highest()
    for i in points_list:
        for j in highest:
            if i == j:
                highest.remove(j)
    return highest
