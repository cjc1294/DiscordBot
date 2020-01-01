import discord
import asyncio
import random
import csv
import requests

async def remind(message):
        """

        """
        args = message.content[message.content.find(" ") + 1:]
        args = args.split()
        if len(args) > 1:
                outMessage = "@" + str(message.author) + " " + " ".join(args[1:])
        else:
                outMessage = "@" + str(message.author) + " " + "I'm here to remind you of a thing"
        
        if args[0].isdigit():
                await asyncio.sleep(60 * int(args[0]))
                await message.channel.send(outMessage)
        else:
                await message.channel.send("Invalid time, please input a time in minutes for the first arguement")


async def roll(message):
        if message.content.find("d") == -1:
                await message.channel.send("Rolling is done with \"!roll <# of dice>d<sides of dice>\"")
                return

        args = message.content[message.content.find(" ") + 1:]
        args = args.replace(" ", "")

        if args.startswith("d"):
                numDice = 1
                args = args[1:]
        else:
                numDice = args[:args.find("d")]
                if not numDice.isdigit():
                        await message.channel.send("Error: Invalid Number of Dice")
                        return
                numDice = int(numDice)
                if numDice > 9999:
                        numDice = 9999
                args = args[args.find("d") + 1:]
        
        sides = ""
        while args[0] not in "+-<>":
                sides += args[0]
                args = args[1:]

                if args == "":
                        break
        if sides.isdigit():
                sides = int(sides)
        else:
                await message.channel.send("Error: Invalid Dice Sides")
                return
        
        target = 0
        greaterThan = True
        modifier = 0

        if args.startswith("+") or args.startswith("-"):
                args = args.strip("+")

                modifier = ""
                while args[0] not in "<>":
                        modifier += args[0]
                        args = args[1:]

                        if args == "":
                                break
                
                if not modifier.strip("-").isdigit():
                        await message.channel.send("Error: Invalid Dice Modifier")
                        return

                modifier = int(modifier)

        if args.startswith("<") or args.startswith(">"):
                if args.startswith("<"):
                        greaterThan = False

                args = args[1:]
                if not args.isdigit():
                        await message.channel.send("Error: Invalid Dice Target")
                        return
                
                target = int(args)
        
		
        rolls = []
        total = 0
        hits = 0
        for i in range(numDice):
                roll = random.randint(1, sides) + modifier
                total += roll
                if roll > target:
                        if not greaterThan and roll == target:
                                hits += 1
                        hits += 1
                
                if numDice <= 30:
                        rolls.append(str(roll))
        
        if not greaterThan:
                hits = numDice - hits

        rollMessage = "Roll: {}d{}".format(str(numDice), str(sides))
        if modifier > 0:
                rollMessage += " + " + str(modifier)
        elif modifier < 0:
                rollMessage += " - " + str(abs(modifier))

        if target != 0:
                if greaterThan:
                        rollMessage += " > " + str(target)
                else:
                        rollMessage += " < " + str(target)

        await message.channel.send(rollMessage + "\n" + ", ".join(rolls))
        if target != 0:
                await message.channel.send("Hits: " + str(hits))
        else:
                await message.channel.send("Total: " + str(total))


async def author(message):
        await message.channel.send(message.author)


async def note(message):
        if message.content.find(" ") != -1:
                args = message.content[message.content.find(" ") + 1:]
                with open(message.guild.name + "/" + str(message.author) + ".txt", "w") as fd:
                        fd.write(str(args))
                await message.channel.send("Noted")

        else:
                with open(message.guild.name + "/" + str(message.author) + ".txt", "r") as fd:
                        await message.channel.send("Your note is: '" + fd.read() + "'")


async def blam(message):
        with open(message.guild.name + "/count.txt") as fd:
                count = int(fd.read())
        with open(message.guild.name + "/count.txt", "w") as fd:
                fd.write(str(count + 1))

        await message.channel.send(str(count + 1) + " bolter rounds have been fired")

        targetList = []
        with open(message.guild.name + "/heresyFiles.txt") as fd:
                for line in fd:
                        try: 
                                targetList.append(line.strip())
                        except discord.errors.NotFound:
                                await message.channel.send("Target not found")

        if len(targetList) > 0:
                try:
                        target = await message.channel.fetch_message(int(targetList.pop()))
                        try:
                                await target.delete()
                        except discord.errors.NotFound:
                                await message.channel.send("Target missed")
                except discord.errors.NotFound:
                        await message.channel.send("Target not found")
                

        with open(message.guild.name + "/heresyFiles.txt", "w") as fd:
                for target in targetList:
                        fd.write(target + "\n")


MANIFEST = {
        "remind":remind,
        "roll":roll,
        "author":author,
        "note":note,
        "blam":blam
        }
