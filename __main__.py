import discord
from discord.ext import commands
import os
from random import randrange
from dotenv import load_dotenv
import pickle

# load .env variables
load_dotenv()

failedCommandTumnail = "https://cdn.discordapp.com/emojis/831963313889476648.gif?v=1"
USER_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "user_file.bin")
USER_MAPPING_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "user_mapping_file.bin")

bot = commands.Bot(command_prefix='$')

usersID = set()
usersID_mapping = {} # match -> giver
delay = 1

@bot.event
async def on_ready():
    loadData()
    print('We have logged in as {0.user}'.format(bot))

@bot.command(pass_context = True , aliases=["giftforwarding", "gf"])
async def _giftforwarding(ctx, *args):
    if ctx.author.id not in usersID:
        usersID.add(ctx.author.id)
        saveData()
        await ctx.send("This is your first time using this command ! You where just added to the user list ! Do the command again if you want to be match with someone")
        return
    if len(usersID) <= 1:
        await ctx.send("Not enought people are register in the bot to match you")
        return

    match = get_match(ctx.author.id)
    if match is not None:
        usersID_mapping[match] = ctx.author.id
        member = await ctx.guild.fetch_member(match)
        await ctx.send("You where just match with: {}".format(member.nick))
    else:
        await ctx.send("There is no one left to match you with :(")

def get_match(id):
    available_users = []
    for userID in usersID:
        if userID not in usersID_mapping and userID != id:
            available_users.append(userID)
    if len(available_users) == 0:
        return None
    return available_users[randrange(len(available_users))]
    

def saveData():
    with open(USER_FILE,'wb') as f:
        pickle.dump(usersID, f)
    with open(USER_MAPPING_FILE,'wb') as f:
        pickle.dump(usersID_mapping, f)

def loadData():
    global usersID
    global usersID_mapping
    if os.path.isfile(USER_FILE):
        with open(USER_FILE,'rb') as f:
            usersID = pickle.load(f)
    if os.path.isfile(USER_MAPPING_FILE):
        with open(USER_MAPPING_FILE,'rb') as f:
            usersID_mapping = pickle.load(f)

bot.run(os.getenv('TOKEN'))