import csv
import pandas as pd

# function that returns a requested stat for a specific player by turning CSV rows into a searchable dictionary
def find_stat(name, stat):
    col_name = ["name", "cost", "s", "ot", "in", "BC", "xG", "G", "KP", "BCC", "xA", "A", "Pts", "predicted", "AFDR"]
    name1 = str(name)
    stat1 = str(stat)
    with open('C:/Users/ruben/Computing Coursework/static/Data/POP.csv',encoding='utf-8-sig', newline='') as csvfile:
        statsreader = csv.DictReader(csvfile, fieldnames=col_name)
        for row in statsreader:
            for name, stat in row.items():
                if name1 == row["name"]:
                    return row[stat1]
                    break


# same but for team stats
def find_teamstat(team, stat):
    col_name = ["team", "sc", "cin", "cot", "csp", "chd", "cbc", "xGC", "xCS", "DFDR"]
    team1 = str(team)
    stat1 = str(stat)
    with open('C:/Users/ruben/Computing Coursework/static/Data/Team-stats.csv',encoding='utf-8-sig', newline='') as csvfile:
        statsreader = csv.DictReader(csvfile, fieldnames=col_name)
        for row in statsreader:
            for team, stat in row.items():
                if team1 == row["team"]:
                    return row[stat1]
                    break

# uses attacking stats and FDR to determine goal threat for a player i.e. number of goals/total goals by team
def threat(name):
    name = str(name)
    percentage = 0
    percentage += float(find_stat(name, "s"))*0.8
    percentage += float(find_stat(name, "ot")) * 1
    percentage += float(find_stat(name, "in")) * 1.05
    percentage += float(find_stat(name, "BC")) * 1.2
    percentage += float(find_stat(name, "xG")) * 1.4
    goals = (float(find_stat(name, "AFDR"))*5)*(percentage/100)
    return goals


# uses creative stats and FDR to determine assist threat i.e. number of assists/total goals by team
def creativity(name):
    name = str(name)
    percentage = 0
    percentage += float(find_stat(name, "KP"))*1
    percentage += float(find_stat(name, "BCC"))*1.2
    percentage += float(find_stat(name, "xA"))*1.4
    assists = (float(find_stat(name, "AFDR"))*5)*(percentage/100)
    return assists


# number of cleansheets for GKs (4), DEFs (4) and MIDs (1) based on team defensive stats
def cleansheet(name):
    name = str(name)
    string = str(find_stat(name, "name"))
    nameList = string.split("(")
    team = nameList[2]
    percentage = 0
    percentage += float(find_teamstat(team, "sc"))*0.8
    percentage += float(find_teamstat(team, "cin")) * 1.05
    percentage += float(find_teamstat(team, "cot")) * 1
    percentage += float(find_teamstat(team, "csp")) * 1
    percentage += float(find_teamstat(team, "chd")) * 1
    percentage += float(find_teamstat(team, "cbc")) * 1.2
    percentage += float(find_teamstat(team, "xGC")) * 1.4
    percentage += float(find_teamstat(team, "DFDR")) * 1.4
    cleansheets = (float(find_teamstat(team, "xCS"))-(percentage/100))*5
    return cleansheets


# puts it all together by multiplying the above values by the fpl points they are worth
def pointsprediction(name):
    name = str(name)
    string = str(find_stat(name, "name"))
    nameList = string.split("(")
    position = nameList[1]
    points = 0
    if position == "M)":
        points += threat(name)*5
        points += creativity(name)*3
        points += cleansheet(name)*1
        points += 10
        return points
    if position == "D)":
        points += threat(name)*6
        points += creativity(name)*3
        points += cleansheet(name)*4
        points += 10
        return points
    if position == "F)":
        points += threat(name)*4
        points += creativity(name)*3
        points += cleansheet(name)*1
        points += 10
        return points
    if position == "G)":
        points += threat(name)*6
        points += creativity(name)*3
        points += cleansheet(name)*4
        points += 10
        return points


# write predicted points to CSV file to be used to make reccomendations
def update_csv():
    col_name = ["name", "cost", "s", "ot", "in", "BC", "xG", "G", "KP", "BCC", "xA", "A", "Pts", "predicted", "AFDR"]
    df = pd.read_csv('C:/Users/ruben/Computing Coursework/static/Data/POP.csv', names=col_name, encoding='utf-8-sig')
    for index, row in df.iterrows():
        points = pointsprediction(row["name"])
        points = round(points, 1)
        df.loc[index, "predicted"] = points
        df.to_csv(path_or_buf='C:/Users/ruben/Computing Coursework/static/Data/POP.csv', index=False, header=False, encoding='utf-8-sig')
        print(find_stat(row["name"], "predicted"))















