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

@bot.event
async def on_ready():
    TimerChecker(data.usersID_mapping)
    print('We have logged in as {0.user}'.format(bot))
    print(data.usersID, data.usersID_mapping)

@bot.command(pass_context = True , aliases=["giftforwarding", "gf"])
async def _giftforwarding(ctx, *args):
    if ctx.author.id not in data.usersID:
        data.usersID.add(ctx.author.id)
        data.saveData()
        await ctx.send("This is your first time using this command ! You where just added to the user list ! Do the command again if you want to get a gift budy")
        return
    if len(data.usersID) <= 1:
        await ctx.send("Well this is a stange place... you are the only one register in the bot ! Maybe a gift for you is a great idea !")
        return

    match = get_match(ctx.author.id)
    if match is not None:
        data.usersID_mapping[match] = ctx.author.id
        member = await ctx.guild.fetch_member(match)
        data.saveData()
        await ctx.send("You gift special person is : {}\nTake good care of him/her !".format(member.nick))
    else:
        await ctx.send("Everybody already received a gift ! You cannot give gift anymore !")

def get_match(id):
    available_users = []
    for userID in data.usersID:
        if userID not in data.usersID_mapping and userID != id:
            available_users.append(userID)
    if len(available_users) == 0:
        return None
    return available_users[randrange(len(available_users))]

bot.run(os.getenv('TOKEN'))