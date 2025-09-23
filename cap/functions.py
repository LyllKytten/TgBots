import json
import random


def addPlayer(chatId, playerName):
    with open('players.json', 'r') as f:
        players = json.load(f)
    f.close()
    print(type(chatId), type(playerName), chatId, playerName, players)

    if not chatId in players:
        players[chatId] = [playerName, 0]
        with open('players.json', 'w') as f:
            json.dump(players, f)
        f.close()
        return "added to players list"
    else:
        return "already in players"

def changePlayerActive(chatId, type):
    with open('players.json', 'r') as f:
        players = json.load(f)
    f.close()

    players[chatId][1] = type

    with open('players.json', 'w') as f:
        json.dump(players, f)
    f.close()

def player_list():
    with open('players.json', 'r') as f:
        players = json.load(f)
    f.close()
    return players

def changePlayerUsername(chatId, username):
    if len(username) < 5:
        return "username too short ( min length 5 )"
    else:
        with open('players.json', 'r') as f:
            players = json.load(f)
        f.close()

        players[chatId][0] = username
        with open('players.json', 'w') as f:
            json.dump(players, f)
        f.close()

        return "username changed to " + username

def pingAllInJoinedPlayers():
    with open('players.json', 'r') as f:
        players = json.load(f)
    f.close()

    activePlayers = []

    for player in players:
        if players[player][1] == 1:
            activePlayers.append(int(player))

    return activePlayers

def playersCircle():
    with open('players.json', 'r') as f:
        players = json.load(f)
    f.close()

    circleDict = {}
    circleList = []

    for player in players:
        if players[player][1] == 1:
            circleDict[player] = players[player][0]
            circleList.append(players[player])

    random.shuffle(circleList)

    return [circleDict, circleList]