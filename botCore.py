import discord
import asyncio
import random
import csv
import requests
from datetime import datetime
from commands import MANIFEST

client = discord.Client()

TARGET = 'test'
if TARGET == 'test':
	HERESY_MARK = '💯'
	CLIENT_CODE = 'MzU0Mzk4NDMyMTI0OTkzNTM2.DI9svQ.-S6HcYiht7GPLvvijLv4U_Y_nGs'
	PLAY_TEXT = discord.Game('with some code')
elif TARGET == 'main':
	HERESY_MARK = '<:Heresy:268495139876372480>'
	CLIENT_CODE = 'MzUxMDcyMzI5MzIyNzI1Mzkw.DINRIQ.JQCN2YE7kffKHP76BXI_O0y7GqU'
	PLAY_TEXT = discord.Game('with promethum')

def log(text):
        fileName = str(datetime.now().date())
        fileName += " " + str(datetime.now().time()).replace(":", " ")
        with open("logs/" + fileName + ".log", "w") as fd:
                fd.write(text)

@client.event
async def on_ready():
        print("Logged in as", client.user.name)
        await client.change_presence(activity = PLAY_TEXT)

@client.event
async def on_reaction_add(reaction, user):
        if str(reaction.emoji) == HERESY_MARK:
                heresyMessage = str(reaction.message.id)
                with open(reaction.message.guild.name + "/heresyFiles.txt", "a") as fd:
                        fd.write(heresyMessage + "\n")


@client.event
async def on_message(message):
        try:
                if message.author == client.user:
                        return

                if message.content.startswith("!"):
                        if message.content.find(" ") != -1:
                                command = message.content[1:message.content.find(" ")]
                        else:
                                command = message.content[1:]

                        if command in MANIFEST:
                                await MANIFEST[command](message)

                        if command in REFERENCES:
                                await message.channel.send(REFERENCES[command])

                        await message.delete()
        except Exception as e:
                log("[{}] Unhandled Exception: {}".format(message.guild.name, e))
                raise e


REFERENCES = {}
with open("References.csv") as refList:
        refListCSV = csv.reader(refList)
        for row in refListCSV:
                REFERENCES[row[0]] = row[1]


if __name__ == "__main__":
        try:
                while True:
                        try:
                                client.run(CLIENT_CODE)
                        except ConnectionResetError:
                                log("Connection reset, retrying")
                                pass
        except Exception as e:
                log("Unhandled Exception: " + e)
                raise e