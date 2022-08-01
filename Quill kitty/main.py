import discord
from discord.ext import commands
import asyncio
import random
import ast
import os

bot = commands.Bot(command_prefix = "-", case_insensitive=True)

@bot.event
async def on_ready():
    print("Bot ready")

def tk_safe(string: str):
    characters = []
    for i in string:
        if 0 < ord(i) < 65536:
            characters.append(i)
        else:
            characters.append(f"[U+{ord(i):02X}]")
    return "".join(characters)

def Main():
    with open('important.txt', "r") as f:
        token =  ast.literal_eval(f.read())
    bot.run(token)


async def xembed(title, desc):
    return discord.Embed(title=title, description=desc, color=0xb40a78)

global timeID
with open('messageID.txt',"r") as f:
    timeID = ast.literal_eval(f.read())
#insert the message ID in the file
#timeID is the main message



def load():
    global bank
    global messig
    with open('bank.json', "r") as f:
        bank =  ast.literal_eval(f.read())
        messig = bank['message']

def save():
    with open('bank.json', 'w') as f:
        f.write(repr(bank))

@bot.command()
async def roll(ctx, *, side:int=20):
        """
        Rolls a die, randomly picking a number between 1 and the number of sides
        -roll (sides)
        """
        message = await ctx.send(embed = await xembed("{},".format(ctx.author.display_name), f"You rolled a {side}-sided die and got {random.randint(1,side)}"))



@bot.command()
async def newmessage(ctx):
    """
    Command used to send a new message. Used for the addtime. Don't use this please
    """
    await ctx.send("** **")



async def getmsg(ctx, msgID:int):
    msg = await ctx.fetch_message(msgID)
    return msg

@bot.command()
async def calendar(ctx):
    """
    Information about the Issellian Calendar
    """
    await ctx.send(""" The Issellian Calendar has 140 days per year split up into 10 months. \nA week has 7 days and each month has 2 weeks.\nEvery month in order:
                    Peinín
                    Listir
                    Mort
                    Finet
                    Aust
                    Erat
                    Lúsifer
                    Syw
                    Osk'r
                    Noariic
                   """)



global months
months = [["Peinín",14],["Listir",14], ["Mort",14], ["Finet",14], ["Aust",14],["Erat",14], ["Lúsifer",14], ["Syw",14], ["Osk'r",14],["Noariic",14],]
weekdays = {1:"Sol",2:"Lune",3:"Ós",4:"Far'l",5:"Dronder",6:"Heimill",7:"Frind"}
spicynum = {1:"1st",2:"2nd",3:"3rd",4:"4th",5:"5th",6:"6th",7:"7th",8:"8th",9:"9th",10:"10th",11:"11th",12:"12th",13:"13th",14:"14th"}
@bot.command()
async def addtime(ctx,*, addedTime:int=1):
    """
    Advances time in the world. Admin command only
    Cycles through the year
    """
    load()

    def newMonth():
        if messig['month'] < 9:
            messig['month'] = messig['month']+1
        else:
            messig['month'] = 0
            messig['year']= messig['year']+1

    def newWeek():
        if messig['week'] < 19:
            messig['week'] = messig['week']+1
        else:
            messig['week'] = 0

    def newDay():
        messig['hour']=0
        if messig['day'] < months[messig['month']][1]:
            messig['day']= messig['day']+1
        else:
            messig['day'] = 1
            newMonth()
        if messig['weekday'] <7:
            messig['weekday'] = messig['weekday'] +1
        else:
             messig['weekday'] = messig['weekday'] = 1
             newWeek()

    #insert the userID of the bot master here
    yourID = 139102588762193920
    if False:
        await ctx.send("bruh you're not allowed to do that")
    else:
        for i in range(addedTime):
            if messig['hour']+1 < 24:
               messig['hour'] = messig['hour']+1
            else:
                newDay()
        monthnum = messig['month']
        weekday = weekdays[messig['weekday']]

        embed = discord.Embed(title="Time and Date", description="Current time and date according to the Issellian Calendar", colour=0xb40a78)
        embed.add_field(name="Time", value=f"{messig['hour']}:00")
        embed.add_field(name="Date", value=f"{weekday} the {spicynum[messig['day']]}")
        embed.add_field(name="Month", value=f"{months[monthnum][0]}")
        embed.add_field(name="Week", value=f"{messig['week']}")
        embed.add_field(name="Year", value=f"{messig['year']}")
        #embed.add_field(name="Debug", value=f"{messig}")
        #await ctx.send(embed = embed)
        bleh = await getmsg(ctx, timeID)
        await bleh.edit(content="", embed=embed)
        await ctx.message.delete()
        save()




if __name__ == "__main__":
    Main()
