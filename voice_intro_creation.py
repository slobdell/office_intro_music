# THIS FILE WILL ONLY WORK ON MAC OS X

import pyttsx
import Foundation
import random
from engineer_list import ENGINEER_TO_MP3

Foundation.NSURL
engine = pyttsx.Engine()
voices = engine.getProperty("voices")

for voice in voices:
    print voice.id
    if "Alex" in str(voice.id):  # cannot arbitrarily create objc strings
        engine.setProperty("voice", voice.id)
#    engine.setProperty("voice", voice.id)
#    engine.say("this is a test")
#    engine.runAndWait()

engine.setProperty("rate", 150)
engine.proxy._driver._proxy.setBusy(False)  # must set to False in order for above properties to take effect

GREETING = [
    "hello",
    "good morning",
    "top of the morning",
    "welcome",
    "all hail",
    "behold",
    "in the red corner hailing from San Francisco",
    "in the blue corner hailing from far east in Canada"
    "all rise for",

]


NICKNAMES = [
    "Iceman",
    "Maverick",
    "Crazy Fingers",
    "Deepwoods",
    "The Blizzard",
    "Smoke",
    "Ice Box",
    "Spike",
    "Whack Attack",
    "Tee Bone"
]

RANDOM_OUTROS = [
    "destroyer of all the universe",
    "first of his name and protector of product",
    "lord commander of Hearsay Social",
    "senior compliance engineer and marketing blocker",
    "senior underling to the lord commander of Hearsay Social",
    "assistant to the chief technical officer",
    "heavy weight software engineering champion",
    "the one whom the prophecies fortold",
    "the one man wolf pack",
    "the legendary coder who allegedly doesn't even use vim"
]


def to_filename(name):
    filename = name.lower().replace(" ", "_") + ".wav"
    return filename

for engineer in ENGINEER_TO_MP3.keys():
    file = Foundation.NSURL.fileURLWithPath_(to_filename(engineer))
    intro = random.choice(GREETING)
    outro = random.choice(RANDOM_OUTROS)
    nickname = random.choice(NICKNAMES)
    first = engineer.split(" ")[0]
    last = engineer.split(" ")[1]
    thing_to_say = " ".join((intro, first, nickname, last, outro))
    engine.proxy._driver._tts.startSpeakingString_toURL_(thing_to_say, file)
    print thing_to_say
    # USE MP3-CONVERTER TO CONVERT TO MP3 AFTERWARD
