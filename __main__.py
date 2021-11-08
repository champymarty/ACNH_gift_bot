import discord
from discord.ext import commands
import os
from random import randrange
from dotenv import load_dotenv

from TimeChecker import TimerChecker
from data import Data

# load .env variables
load_dotenv()

failedCommandTumnail = "https://cdn.discordapp.com/emojis/831963313889476648.gif?v=1"

bot = commands.Bot(command_prefix='$')
data = Data()
timeChecker = TimerChecker(data)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command(pass_context = True , aliases=["giftforwarding", "gf"])
async def _giftforwarding(ctx, *args):
    if len(args) == 0:
        if ctx.author.id not in data.usersID:
            data.usersID.add(ctx.author.id)
            data.saveUser()
            await sendMessage(ctx.message, "This is your first time using this command ! You where just added to the user list ! Do the command again if you want to get a gift budy", "Registration to gift exhanges successfull")
            return
        if len(data.usersID) <= 1:
            await sendMessage(ctx.message, "Well this is a stange place... you are the only one register in the bot ! Maybe a gift for you is a great idea !", "You are the only one register", error=True)
            return
        match = get_match(ctx.author.id)
        if match is not None:
            data.usersID_mapping[match] = ctx.author.id
            member = await ctx.guild.fetch_member(match)
            data.saveMapping()
            await sendMessage(ctx.message, "Your gift receiver is : {}\nTake good care of them !".format(member.nick), "Gift matcher")
        else:
            await sendMessage(ctx.message, "Everybody already received a gift ! You cannot give gift anymore ! Next gift reset in {}".format(timeChecker.getTimeUntilNextReset()), "Everybody as a gift", error=True)
    else:
        if len(args) > 1:
            await ctx.send("Invalid command !")
        elif args[0].lower() == "all":
            message = ""
            for receiver, giver in data.usersID_mapping.items():
                memberReceiver = await ctx.guild.fetch_member(receiver)
                memberGiver = await ctx.guild.fetch_member(giver)
                message += "**{}** is getting a gift from *{}* !\n".format(memberReceiver.nick, memberGiver.nick)
            if message == "":
                message = "*No gifts exchanges today :(*"
            await sendMessage(ctx.message, message, "Gifts exchanges of the days !")
        elif args[0].lower() == "remove" or args[0].lower() == "r":
            if ctx.author.id in data.usersID:
                data.usersID.remove(ctx.author.id)
                data.saveUser()
                await sendMessage(ctx.message, "You where just remove from the gift exchanges !", "Removed successfully !")
            else:
                await sendMessage(ctx.message, "You are not register in the gifts exchanges !", "Not register error", error=True)
        elif args[0].lower() == "help":
            message = "{}\n\n{}\n\n{}\n\n{}\n\n{}\n\n{}\n\n{}\n\n".format("**First time use:** *$giftforwarding or $gf*",
            "**Give a gift:** *$giftforwarding or $gf*",
            "**See all gift exchange of the day:** *$giftforwarding all or $gf all*",
            "**Remove yourself from gift exchange:** *$giftforwarding(gf) remove(r)*",
            "**Force reset gift exchange of the day:** *$reset_gifts or $rg*",
            "**See time remaining until next reset:** *$time*",
            "**See this help window:** *$giftforwarding help or $gf help*"
            )
            await sendMessage(ctx.message, message, "Help desk")

@bot.command(pass_context = True , aliases=["reset_gifts", "rg"])
async def _resetGifts(ctx):
    data.usersID_mapping.clear()
    data.saveMapping()
    await sendMessage(ctx.message, "The gifts were just reset !", "Reset information")

@bot.command(pass_context = True , aliases=["time"])
async def _showTime(ctx):
    await sendMessage(ctx.message, "", "gifts reset in {}".format(timeChecker.getTimeUntilNextReset()))
    

def getNumberOfGiftGiven(giverId):
    count = 0
    for giver in data.usersID_mapping.values():
        if giver == giverId:
            count += 1
    return count

def get_match(id):
    available_users = []
    for userID in data.usersID:
        if userID not in data.usersID_mapping and userID != id:
            available_users.append(userID)
    if len(available_users) == 0:
        return None
    return available_users[randrange(len(available_users))]

async def sendMessage(message, messageToDisplay, title, error=False):
    embedVar = discord.Embed(title=title, description=messageToDisplay, color=0x00FF00)
    if error:
      embedVar.set_thumbnail(url = failedCommandTumnail)
      embedVar.__setattr__("color", 0xFF0000)
    await message.channel.send(embed=embedVar)

bot.run(os.getenv('TOKEN'))