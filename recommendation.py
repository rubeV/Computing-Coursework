import datetime
import csv
import pandas as pd
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
    async with aiohttp.ClientSession(trust_env=True) as session:
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
            k = str(p["web_name"])+" "+str(p["element_type"])+" "+str(p["team"])
            picked_players.append(k)
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


# change name format to access data on current team from pop csv
def change_name(player):
    num_list = [int(i) for i in player.split() if i.isdigit()]
    player1 = ''.join([i for i in player if not i.isdigit()])
    if num_list[0] == 1:
        player1 += "(G)"
    if num_list[0] == 2:
        player1 += "(D)"
    if num_list[0] == 3:
        player1 += "(M)"
    if num_list[0] == 4:
        player1 += "(F)"
    if num_list[1] == 12:
        player1 += "(MCI)"
    if num_list[1] == 13:
        player1 += "(MUN)"
    if num_list[1] == 9:
        player1 += "(LEI)"
    if num_list[1] == 5:
        player1 += "(CHE)"
    if num_list[1] == 19:
        player1 += "(WHU)"
    if num_list[1] == 7:
        player1 += "(EVE)"
    if num_list[1] == 17:
        player1 += "(THS)"
    if num_list[1] == 11:
        player1 += "(LIV)"
    if num_list[1] == 2:
        player1 += "(AVL)"
    if num_list[1] == 1:
        player1 += "(ARS)"
    if num_list[1] == 10:
        player1 += "(LEE)"
    if num_list[1] == 20:
        player1 += "(WOL)"
    if num_list[1] == 6:
        player1 += "(CPL)"
    if num_list[1] == 16:
        player1 += "(SOU)"
    if num_list[1] == 4:
        player1 += "(BUR)"
    if num_list[1] == 14:
        player1 += "(NEW)"
    if num_list[1] == 3:
        player1 += "(BHA)"
    if num_list[1] == 8:
        player1 += "(FUL)"
    if num_list[1] == 18:
        player1 += "(WBA)"
    if num_list[1] == 15:
        player1 += "(SHU)"
    player1 = player1.replace(" ", "")
    return player1


# get predicted points of team
def pp_current():
    email=os.environ.get('EMAIL')
    password=os.environ.get('PASSWORD')
    user_id=os.environ.get('USER_ID')
    player_list = asyncio.run(update(email, password,user_id))
    points_list = []
    for player in player_list:
        player1 = change_name(player)
        points = find_pp(player1)
        points_list.append((player1, points))
    return points_list


# gets the player in each position in the user's team with the lowest predicted score
def get_lowest(points_list):
    lowest_gk = 0
    lowest_df = 0
    lowest_mid = 0
    lowest_fwd = 0
    lowest_gk_name = ""
    lowest_df_name = ""
    lowest_mid_name = ""
    lowest_fwd_name = ""
    lowest = []
    for player in points_list:
        if player[1] is None:
            continue
        if "(G)" in player[0]:
            if lowest_gk == 0:
                lowest_gk = player[1]
                lowest_gk_name = player[0]
            if player[1] < lowest_gk:
                lowest_gk = player[1]
                lowest_gk_name = player[0]
        if "(D)" in player[0]:
            if lowest_df == 0:
                lowest_df = player[1]
                lowest_df_name = player[0]
            if player[1] < lowest_df:
                lowest_df = player[0]
                lowest_df_name = player[0]
        if "(M)" in player[0]:
            if lowest_mid == 0:
                lowest_mid = player[1]
                lowest_mid_name = player[0]
            if player[1] < lowest_mid:
                lowest_mid = player[0]
                lowest_mid_name = player[0]
        if "(F)" in player[0]:
            if lowest_fwd == 0:
                lowest_fwd = player[1]
                lowest_fwd_name = player[0]
            if player[1] > lowest_fwd:
                lowest_fwd = player[0]
                lowest_fwd_name = player[0]
    lowest.append(lowest_gk_name)
    lowest.append(lowest_df_name)
    lowest.append(lowest_mid_name)
    lowest.append(lowest_fwd_name)
    return lowest

# gets the player in each position with the highest predicted score
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


# compares team to highest predicted points players
def recommend():
    rec = []
    points_list = pp_current()
    print(points_list)
    low_list = get_lowest(points_list)
    print(get_lowest(points_list))
    highest = get_highest()
    for p1 in points_list:
        for p2 in highest:
            if p1[0] == p2:
                highest.remove(p2)
    print(highest)
    for low in low_list:
        for player in highest:
            if "(G)" in low:
                if "G" in player:
                    rec.append((low, player))
            if "(D)" in low:
                if "(D)" in player:
                    rec.append((low, player))
            if "(M)" in low:
                if "(M)" in player:
                    rec.append((low, player))
            if "(F)" in low:
                if "(F)" in player:
                    rec.append((low, player))
    print(rec)
    return rec
