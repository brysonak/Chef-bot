import random

areaCodes = {
    "San Diego": "858",
    "Cleveland": "216"
    }

prefixCodes = {
    "his favorite AM station was always 930": "930",
    "his favorite AM station was always 240": "240",
    "his favorite AM station was always 580": "580",
    "his favorite AM station was always 760": "760",
    "his favorite AM station was always 420": "420",

}

lineCodes = {
    "He registered his number when the clock struck midnight": "1200",
    "He registered his number at the time the iPhone was announced": "0941",
    "He registered his number at the same time as the armistice of WWI": "1100",
    "He registered his number at the same time as when the titanic sank": "0220",
    "He registered his number at the same time his watch's hands showed a smiley face": "1010"
}

phoneNumbersToCall = [
    "212-094-1200", "212-094-0941", "212-094-1100", "212-094-0220", "212-094-1010",
"305-240-1200", "305-240-0941", "305-240-1100", "305-240-0220", "305-240-1010",
"415-580-1200", "415-580-0941", "415-580-1100", "415-580-0220", "415-580-1010",
"617-760-1200", "617-760-0941", "617-760-1100", "617-760-0220", "617-760-1010",
"702-420-1200", "702-420-0941", "702-420-1100", "702-420-0220", "702-420-1010",
"202-094-1200", "202-094-0941", "202-094-1100", "202-094-0220", "202-094-1010",
"312-240-1200", "312-240-0941", "312-240-1100", "312-240-0220", "312-240-1010",
"404-580-1200", "404-580-0941", "404-580-1100", "404-580-0220", "404-580-1010",
"503-760-1200", "503-760-0941", "503-760-1100", "503-760-0220", "503-760-1010",
"713-420-1200", "713-420-0941", "713-420-1100", "713-420-0220", "713-420-1010",
"206-094-1200", "206-094-0941", "206-094-1100", "206-094-0220", "206-094-1010",
"303-240-1200", "303-240-0941", "303-240-1100", "303-240-0220", "303-240-1010",
"801-580-1200", "801-580-0941", "801-580-1100", "801-580-0220", "801-580-1010",
"919-760-1200", "919-760-0941", "919-760-1100", "919-760-0220", "919-760-1010",
"314-420-1200", "314-420-0941", "314-420-1100", "314-420-0220", "314-420-1010"
]

wrongNumberStrings = [
     "Hello! Can I speak to G...\nWait a second...\nIs this the wrong number?\nOh, it's the wrong number!\nThe wrong number song!\nWe're very very sorry that we got it wrong!\nOh, it's the wrong number!\nThe wrong number song!\nWe're very very sorry that we got it wrong!",
     "I'm sorry, but the number you're trying to reach has a voicemail box that has not been set up yet. Goodbye",
     "Domino's Pizza. I'm sorry but we're currently closed",
     "Apple Support how may I not help you today? I'm sorry, I couldn't quite get that. Goodbye",
     "Hello? Hello hello? Uh, I wanted to record a message for you, to help you get settled in on your first nigh- (the phone call disconnects mysteriously)"
]


def initializeGame():
    location = random.choice(list(areaCodes))
    prefix = random.choice(list(prefixCodes))
    line = random.choice(list(lineCodes))
    p1, p2, p3 = random.sample(phoneNumbersToCall, 3)
    target = areaCodes[location] + "-" + prefixCodes[prefix] + "-" + lineCodes[line]
    return {"location": location, "prefix": prefix, "line": line,
            "p1": p1, "p2": p2, "p3": p3, "target": target}

def giveLocation(g):
    return f"Oh I remember him! He used to live out in {g['location']}. Try calling one of his other friends, she may be able to help you more.\nYou can reach her at {g['p2']}"

def givePrefix(g):
    return f"Everyone loved that guy! I remember {g['prefix']}. I'm sorry I couldn't tell you more, but maybe his brother can help you!\nYou can call him at {g['p3']}, just tell him I sent you!"

def giveLine(g):
    return f"Yeah I remember when he registered his number, I was right there with him! {g['line']}."

if __name__ == "__main__":
    g = initializeGame()
    inputStr = ""
    print(f"You are trying to track down a phone number. Your only lead is that you can reach one of his friends at {g['p1']}")
    while not inputStr == "exit":
        inputStr = input("What phone number would you like to dial? ")
        if inputStr == g["p1"]:
            print(giveLocation(g))
        elif inputStr == g["p2"]:
            print(givePrefix(g))
        elif inputStr == g["p3"]:
            print(giveLine(g))
        elif inputStr == g["target"]:
            print("You Win! You sucessfully called him about his car's extended warranty!")
            inputStr = "exit"
        elif inputStr != "exit":
            print(random.choice(wrongNumberStrings))
