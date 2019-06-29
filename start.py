import discord
import asyncio
import random
import csv
import requests
from datetime import datetime
from commands import MANIFEST

client = discord.Client()

target='test'
if target=='test':
	heresyMark = '💯'
	clientCode = 'MzU0Mzk4NDMyMTI0OTkzNTM2.DI9svQ.-S6HcYiht7GPLvvijLv4U_Y_nGs'
	playText = discord.Game('with some code')
elif target=='main':
	heresyMark = '<:Heresy:268495139876372480>'
	clientCode = 'MzUxMDcyMzI5MzIyNzI1Mzkw.DINRIQ.JQCN2YE7kffKHP76BXI_O0y7GqU'
	playText = discord.Game('with promethum')

def log(text):
        fileName = str(datetime.now().date())
        fileName += " " + str(datetime.now().time()).replace(":", " ")
        with open("logs/" + fileName + ".log", "w") as fd:
                fd.write(text)

@client.event
async def on_ready():
        print("Logged in as", client.user.name)
        await client.change_presence(activity=playText)

@client.event
async def on_reaction_add(reaction, user):
        if str(reaction.emoji) == heresyMark:
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
                client.run(clientCode)
        except Exception as e:
                log("Unhandled Exception: " + e)
                raise e