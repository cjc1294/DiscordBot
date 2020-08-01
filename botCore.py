import discord
import asyncio
import random
import csv
import os
import time
import socket
import aiohttp
import logging
from datetime import datetime
from commands import MANIFEST

FAILS = 0

LOG_FILE_NAME = "bot.log"
SETTINGS_FILE_NAME = "settings.txt"
CLIENT_CODE = ""
HERESY_MARK = ""
PLAY_TEXT = ""
REFERENCES = {}
client = discord.Client()

with open(LOG_FILE_NAME, "w"):
        pass


def logException(text):
        filename = str(datetime.now().date())
        filename += " " + str(datetime.now().time()).replace(":", " ")
        filename += ".log"
        logging.basicConfig(filename="logs/" + filename, filemode='w', format="%(message)s")
        logger = logging.getLogger(__name__)
        logger.exception(text)


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
        FAILS = 0
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
                logException("[{}] Unhandled Exception:".format(message.guild.name))
                raise e


def main():
        global CLIENT_CODE
        global HERESY_MARK
        global PLAY_TEXT
        global FAILS

        if not os.path.exists("References.csv"):
                with open("References.csv", "w") as fd:
                        pass
                logPrint("References.csv file created. Add references with the format \"command,text\" where command is the command trigger and text is the text for the bot to respond with.")
        
        if not os.path.exists("settings.txt"):
                with open("settings.txt", "w") as fd:
                        fd.write("client code=\nheresy mark=<:100:>\nplaying text=with promethium")
                logPrint("Settings.txt file created. Fill all fields and then rerun the bot.")
                return

        try:
                with open("References.csv") as refList:
                        refListCSV = csv.reader(refList)
                        for row in refListCSV:
                                REFERENCES[row[0]] = row[1]

                with open(SETTINGS_FILE_NAME, "r") as fd:
                        for line in fd:
                                tokens = line.split("=")
                                if tokens[0] == "client code":
                                        CLIENT_CODE = tokens[1].strip()
                                elif tokens[0] == "heresy mark":
                                        HERESY_MARK = tokens[1].strip()
                                        if HERESY_MARK == "<:100:>":
                                                HERESY_MARK = "💯"
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
                        if FAILS >= 5:
                                logPrint("Number of fails exceeded, shutting down")
                                return
                        try:
                                client.run(CLIENT_CODE)
                        except ConnectionResetError:
                                logPrint("Connection Reset")
                                FAILS += 1
                        except RuntimeError as re:
                                if re.args[0] == "Event loop stopped before Future completed":
                                        logPrint("Bot shutting down")
                                        return
                                else:
                                        raise re
                        except (socket.gaierror, aiohttp.client_exceptions.ClientConnectorError):
                                FAILS += 1
                                time.sleep(2)

        except Exception as e:
                logException("Unhandled Exception:")
                raise e

if __name__ == "__main__":
        main()
