import random
import string

###### Guess number Game ######
DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
#Generate the number to guess
def numGen(message):

    num = ""
    if message in DIGITS:
        n = int(message)
        if n < 4:
            n = 4
    else:
        n = 4
    i = 0
    while i < n:
        numRand = str(random.randrange(10))
        if numRand not in num:
            num += numRand
            i += 1
    return num


#Check if the nuber is correct
def numCheck(numGuess, message):
    if len(numGuess) != len(message):
        return "error"
    else:
        result = ""
        countCorrect = 0
        for i in range(len(numGuess)):
            if message[i] not in DIGITS:
                return "error"
            else:
                if message[i] == numGuess[i]:
                    result += "Y"
                    countCorrect += 1
                else:
                    if message[i] in numGuess:
                        result += "O"
                    else:
                        result += "N"
        if countCorrect == len(numGuess):
            return "win"
        else:
            return result


####### the emoji chat activities ######
# Generate a random emoji in the list
def emRandom(lst):
    i = random.randrange(len(lst))
    return lst[i]

# Return emoji based on the input
def emChat(emo):
    emoAll = [":)", ":(", ":D", ">(", ":|", "O_o", "B)", ":O", "<3", ":/", ";)", ":P", ";P", "R)",  "MrDestructoid", "Squid1 Squid2 Squid3 Squid4", "TwitchUnity", "PowerUpR", "PowerUpL"]
    emoPositive = [":D", "B)", ";)", ";P", "R)"]
    emoNeutual = [":)", ":O", ":P", ":|"]
    emoNagative = [":(", ">(", ":/"]
    if "MrDestructoid" in emo:
        return "B)"
    elif "Squid" in emo:
        return "Squid1 Squid2 Squid3 Squid4"
    elif "PowerUpR" in emo:
        return "PowerUpL"
    elif "PowerUpL" in emo:
        return "PowerUpR"
    elif "<3" in emo:
        return "TwitchUnity"
    elif "TwitchUnity" in emo:
        return "<3"
    elif emo in emoPositive:
        return emRandom(emoPositive)
    elif emo in emoNeutual:
        return emRandom(emoNeutual)
    elif emo in emoNagative:
        return emRandom(emoNagative)
    elif emo == "Default":
        return emRandom(emoAll)
    else:
        return "O_o"

    
    




