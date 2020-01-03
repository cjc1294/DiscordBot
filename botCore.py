import discord
import asyncio
import random
import csv
import os
from datetime import datetime
from commands import MANIFEST

LOG_FILE_NAME = "bot.log"
SETTINGS_FILE_NAME = "settings.txt"
CLIENT_CODE = ""
HERESY_MARK = ""
PLAY_TEXT = ""
client = discord.Client()

with open(LOG_FILE_NAME, "w"):
        pass

def createErrorLog(text):
        """
        Create a log in the logs directory
        """
        fileName = str(datetime.now().date())
        fileName += " " + str(datetime.now().time()).replace(":", " ")
        with open("logs/" + fileName + ".log", "w") as fd:
                fd.write(text)

def logPrint(text, includeTime=True):
        if includeTime:
                message = str(datetime.now().date()) + " " + str(datetime.now().time()) + " " + text
        else:
                message = text
        print(message)
        with open(LOG_FILE_NAME, "a") as fd:
                fd.write(message + "\n")

@client.event
async def on_ready():
        logPrint("Logged in as " + client.user.name)
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

                if not os.path.isdir(message.guild.name):
                        os.mkdir(message.guild.name)
                        with open(message.guild.name + "/count.txt", "w") as fd:
                                fd.write("0")
                        with open(message.guild.name + "/heresyFiles.txt", "w"):
                                pass

                if message.content.startswith("!"):
                        if message.content.find(" ") != -1:
                                command = message.content[1:message.content.find(" ")]
                        else:
                                command = message.content[1:]

                        if command in MANIFEST:
                                logPrint(str(message.author) + ": " + message.content)
                                await MANIFEST[command](message)

                        if command in REFERENCES:
                                logPrint(str(message.author) + ": " + message.content)
                                await message.channel.send(REFERENCES[command])

                        await message.delete()
        except Exception as e:
                createErrorLog("[{}] Unhandled Exception: {}".format(message.guild.name, e))
                raise e


REFERENCES = {}
with open("References.csv") as refList:
        refListCSV = csv.reader(refList)
        for row in refListCSV:
                REFERENCES[row[0]] = row[1]

def main():
        global CLIENT_CODE
        global HERESY_MARK
        global PLAY_TEXT

        try:
                with open(SETTINGS_FILE_NAME, "r") as fd:
                        for line in fd:
                                tokens = line.split("=")
                                if tokens[0] == "client code":
                                        CLIENT_CODE = tokens[1].strip()
                                elif tokens[0] == "heresy mark":
                                        HERESY_MARK = tokens[1].strip()
                                elif tokens[0] == "playing text":
                                        PLAY_TEXT = discord.Game(tokens[1])
                if CLIENT_CODE == "" or HERESY_MARK == "":
                        logPrint("ERROR: Required settings are missing. Please make sure the client code and heresy mark are set", includeTime=False)
                        return
        except Exception as ex:
                logPrint("ERROR: Error in settings file, please check to ensure it is correct. If unsure, delete the settings file and it will be regenerated on next run.", includeTime=False)
                raise ex
                return

        try:
                while True:
                        try:
                                client.run(CLIENT_CODE)
                        except ConnectionResetError:
                                logPrint("Connection Reset")
                                pass
        except Exception as e:
                createErrorLog("Unhandled Exception: " + e)
                raise e

if __name__ == "__main__":
        main()
