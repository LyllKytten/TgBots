from multiprocessing.forkserver import read_signed

import telebot
import os
from dotenv import load_dotenv
import time

import functions

isRoundTime = False
words = []
guessers = []
players = []

load_dotenv()
api_key = os.getenv('API_KEY')
bot = telebot.TeleBot(api_key)

help_commands = ["DEFAULT:\n        AFTER ENTERING NAME YOU ARE NOT IN A JOINED LIST  \n DEFAULT: \n        AFTER /start YOU ARE NOT IN JOINED LIST \n\n"
                 "/change_name <name> - your name in game\n\n"
                 "/leave_game - leave game and not play in the next one\n\n"
                 "/join_game - join to the next game\n\n"
                 "/kick <player_name/player_chat_id> - kick INACTIVE player\n\n"
                 "/player_list - show ALL players that is in players_data ( also show their status [ 0 - inactive / 1 - active ])\n\n"
                 "/help - show this message\n\n"
                 ]

def send_help(message):
    for command in help_commands:
        bot.send_message(message.chat.id, command)

async def timer(roundTime, players):
    isRoundTime = True
    timeNow = 0
    while timeNow < roundTime:
        time.sleep(1)
        timeNow += 1
        if timeNow == roundTime-15:
            for player in players:
                bot.send_message(player, "15 SECOND\n\n Type /next_round to start a new round" )

    for player in players:
        bot.send_message(player, "TIME'S UP !!!")

    isRoundTime = False

@bot.message_handler(commands=['start'])
def start(message):
    send_help(message)
    result = functions.addPlayer(str(message.chat.id), message.from_user.username)
    bot.send_message(message.chat.id, result)

@bot.message_handler(commands=['help'])
def help(message):
    send_help(message)

@bot.message_handler(commands=['player_list'])
def player_list(message):
    players = functions.player_list()
    print(players)
    text = "PLAYERS : \n\n"
    for player in players:
        print(player)
        text += f"        {players[player][0]} | status : {players[player][1]} | chatid : {player}\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['change_name'])
def change_name(message):
    try:
        username = message.text.split(' ')[1]
        result = functions.changePlayerUsername(str(message.chat.id), username)
        bot.send_message(message.chat.id, f"{result}")
    except Exception as error:
        print(error)
        bot.send_message(message.chat.id, "YOUR USERNAME IS INVALID")

@bot.message_handler(commands=['leave_game'])
def leave_game(message):
    functions.changePlayerActive(str(message.chat.id), 0)
    bot.send_message(message.chat.id, "you left the game")

@bot.message_handler(commands=['join_game'])
def join_game(message):
    functions.changePlayerActive(str(message.chat.id), 1)
    bot.send_message(message.chat.id, "you joined the game")

@bot.message_handler(commands=['start_game'])
def start_game(message):
    roundTime = message.text.split(' ')[1]
    numOfWords = message.text.split(' ')[2]
    result = functions.pingAllInJoinedPlayers()
    players = result
    print(result)
    for player in result:
        print(player)
        bot.send_message(player, "Game started")

    timer(roundTime, result)

@bot.message_handler(commands=['next_round'])
def next_round(message):
    if not isRoundTime:
        print('aa')

def main():
    print("starting bot . . .")
    bot.infinity_polling()

if __name__ == '__main__':
    main()