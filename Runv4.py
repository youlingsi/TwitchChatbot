import string
import csv
import time
import operator
from Readv3 import getUser, getMessage, getChannelname, getBannedUser, getBannedChannelname
from Readv3 import getslowmode, getr9k, getsubmode, getroomstatechannelname
from Readv3 import getOwner, getTurbo, getSub, getMod
from Socketv2 import openSocket, sendMessage
from Settingsv2 import HOST, PORT, PASS, IDENT
from datetime import datetime
from BotActivities import numGen, numCheck, emChat


# Actually joins the rooms
s = openSocket()

### joinRoom(s)
readbuffer = ""


id = 0

# Sets how long the scraper will run for (in seconds)
starttime = time.time() + 7200

# Define the number to guess:
numGuess = ""

# Runs until time is up
while time.time() < starttime:
    
        # Pulls a chunk off the buffer, puts it in "temp"
        readbuffer = readbuffer + s.recv(1024).decode('utf-8')
        temp = readbuffer.split("\n")
        readbuffer = temp.pop()
    
        # Iterates through the chunk
        for line in temp:
            print(line)
            id = id + 1

        
            # Parses lines and writes them to the file
            if "PRIVMSG" in line:
                try:

                    # Gets user, message, and channel from a line
                    user = getUser(line)
                    message = getMessage(line)
                    channelname = getChannelname(line)
                    owner = getOwner(line)
                    mod = getMod(line)
                    sub = getSub(line)
                    turbo = getTurbo(line)
                    
                    
                    if owner == 1:
                        mod = 1
        
                    # Writes Message ID, channel, user, date/time, and cleaned message to file
                    with open('outputlog.csv', 'a') as fp:
                        ab = csv.writer(fp, delimiter=',')
                        data = [id, channelname, user, datetime.now(), message.strip(), owner, mod, sub, turbo];
                        ab.writerow(data)
                                
                # Survives if there's a message problem
                except Exception as e:
                    print("MESSAGE PROBLEM")
                    print(line)
                    print(e)
        
            # Responds to PINGs from twitch so it doesn't get disconnected
            elif "PING" in line:
                try:
                    separate = line.split(":", 2)
                    s.send(("PONG %s\r\n" % separate[1]).encode('utf-8'))
                    print(("PONG %s\r\n" % separate[1]))
                    print("I PONGED BACK")
                
                # Survives if there's a ping problem
                except:
                    print("PING problem PING problem PING problem")
                    print(line)
        
            # Parses ban messages and writes them to the file
            elif "CLEARCHAT" in line:
                try:
            
                    # Gets banned user's name and channel name from a line
                    user = getBannedUser(line)
                    channelname = getBannedChannelname(line)
                
                    # Writes Message ID, channel, user, date/time, and an indicator that it was a ban message.
                    #   I use "oghma.ban" because the bot's name is oghma, and I figure it's not a phrase that's
                    #   likely to show up in a message so it's easy to search for.
                    with open('outputlog.csv', 'a') as fp:
                        ab = csv.writer(fp, delimiter=',');
                        data = [id, channelname, user, datetime.now(), "oghma.ban"];
                        ab.writerow(data);
            
                # Survives if there's a ban message problem
                except Exception as e:
                    print("BAN PROBLEM")
                    print(line)
                    print(e)



       ###### The activities for the assignment########
            #1. Guessing Number
            if "#numGuessStart" in line:
                if numGuess == "":
                    message = getMessage(line).split("numGuessStart")[1].strip()
                    numGuess = numGen(message)
                    sendMessage(s, "Guess a number with " + str(len(numGuess)) + " Digits" , 0)
                else:
                    sendMessage(s, "The game is already started", 0)
                    sendMessage(s, "Guess a number with " + str(len(numGuess)) + " Digits" , 0)

            if "#numGuessInput" in line:
                if numGuess == "":
                    sendMessage(s, "Type #numGuessStart to start the game.", 0)
                else:
                    message = getMessage(line).split("#numGuessInput")[1].strip()
                    result = numCheck(numGuess, message)
                    if result == "error":
                        sendMessage(s, "Error! Please input a number with " + str(len(numGuess)) + " Digits" , 0)
                    elif result == "win":
                        usr = getUser(line)
                        sendMessage(s, numGuess + "! Correct! " + usr + " wins!", 0)
                        numGuess = ""
                    else:
                        sendMessage(s, result, 0)
                        sendMessage(s, "Y -- Matching Digit; N -- Wrong Digit; O -- Correct digit by wrong position", 0)
                        
            # reveal the secret number and ends the game.
            if "#numGuessPrint" in line:
                    sendMessage(s, "number: " + numGuess, 0)
                    numGuess = ""

            #2. Chat with the bot using emojis
            if "#emChat" in line:
                msg = ""
                message = getMessage(line).split("#emChat")[1].strip()
                #print ("Message is" + message + " end")
                if message == "":
                    msg = emChat("Default")
                else:
                    emo = message.split(" ")
                    print(emo)
                    for em in emo:
                        msg += emChat(em) + " "
                sendMessage(s, msg, 0)

            if "#emSmile" in line:
                sendMessage(s, ";)", 0)











