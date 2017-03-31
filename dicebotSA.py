# A dice rolling bot for use on Discord servers designed for Shadowrun Anarchy
# LICENSE: This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# @category   Tools
# @copyright  Copyright (c) 2016 Robert Thayer (http://www.gamergadgets.net)
# @version    1.1
# @link       http://www.gamergadgets.net
# @author     Robert Thayer

from random import randint
import discord # Imported from https://github.com/Rapptz/discord.py
import asyncio
from discord.ext import commands

# A dice bot for use with Discord
bot = discord.Client()
bot = commands.Bot(command_prefix='!', description="A bot to handle dice rolls for Shadowrun Anarchy")

# Determines if a message is owned by the bot
def is_me(m):
    return m.author == bot.user

# Determines if the value can be converted to an integer
# Parameters: s - input string
# Returns: boolean. True if can be converted, False if it throws an error.
def is_num(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# Roll die and get a random number between 1 and 6
# Returns: int
def roll_basic():
    return randint(1, 6)

def roll_advanced(num_of_dice, glitch, edge, reroll, threshold):
    results = ""
    total, misses = 0, 0
    if (edge):
        num_of_dice += 1
        hit = 4
    else:
        hit = 5
    for x in range(0, int(num_of_dice)):
        y = roll_basic
        if (y >= int(hit)):
            results += "**{}** ".format(y)
            total += 1
        else:
            results += "{} ".format(y)
    misses = num_of_dice - total
    if (reroll > misses):
        reroll = misses
    if (reroll > 0):
        results += "Reroll: "
        for x in range(0, int(reroll)):
            y = roll_basic
            if (y >= int(hit)):
                results += "**{}** ".format(y)
                total += 1
            else:
                results += "{} ".format(y)
    results += "Total hits: {} ".format(total)
    if (threshold > 0):
        if (total >= threshold):
            net_hits = total - threshold
            results += "Success. Net hits: {} ".format(net_hits)
        else:
            results += "Failure. "
    if (glitch):
        results += "Live Dangerously: "
        y = roll_basic
        if (y == 1):
            results += "**GLITCH**"
        elif (y >= 5):
            results += "**EXPLOIT**"
        else:
            results += "No Effect"



@bot.event
@asyncio.coroutine 
def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# Parse !roll verbiage
@bot.command(pass_context=True,description='Rolls dice.\nExamples:\n12  Rolls 12d6.\nModifiers:\n> Threshold. 12>3 returns success if number of hits is greater than or equal to 33.\ne Edge. Use for pre-edge. Will add one die and count 4s as hits.\ng Glitch Die: Roll one die. If a 1, a glitch occurs. If a 5 or 6, an exploit happens.\nr Reroll. 12r2 will reroll up to 2 misses.')
@asyncio.coroutine
def roll(ctx, roll : str):
    plural, index, num_of_dice, threshold, reroll, glitch, edge = "", 0, 0, 0, 0, false, false
    # author: Writer of discord message
    author = ctx.message.author
    roll = roll.lower()
    while (roll[index].isdigit()):
        index += 1
    
    if (index > 0):
        num_of_dice = roll[:index]
    
    roll = roll[index:]
    if (roll.find('e') != -1):
        edge = true
        roll = roll.replace("e", "")
    if (roll.find('g') != -1):
        glitch = true
        roll = roll.replace("g", "")
    if (roll.find('r') != -1):
        index = roll.find('r') + 1
        while (roll[index].isdigit()):
            index += 1
        if (index > roll.find('r')):
            reroll = roll[roll.find('r'):index]
    if (roll.find('>') != -1):
        index = roll.find('>') + 1
        while (roll[index].isdigit()):
            index += 1
        if (index > roll.find('>')):
            threshold = roll[roll.find('>'):index]
        
    #Validate data
    try:
        if (num_of_dice >= 1):
            if (is_num(num_of_dice) is False):
                raise ValueError("Number of dice format error.")
                return
            else:
                num_of_dice = int(num_of_dice)
        if (num_of_dice > 200):
            raise ValueError("Too many dice. Please limit to 200 or less.")
            return
        if (threshold != 0):
            if (is_num(threshold) is False):
                raise ValueError("Error: Threshold must be a number. Proper usage 12>3")
                return
            else:
                threshold = int(threshold)
        if (num_of_dice == 1):
            plural = "die"
        else:
            plural = "dice"
        yield from bot.say("{} rolls {} {}. Results: {}".format(author, num_of_dice, plural, roll_advanced(num_of_dice, glitch, edge, reroll, threshold)))
       
    except ValueError as err:
        # Display error message to channel
        yield from bot.say(err)

#Bot command to delete all messages the bot has made.        
@bot.command(pass_context=True,description='Deletes all messages the bot has made')
@asyncio.coroutine
def purge(ctx):
    channel = ctx.message.channel
    deleted = yield from bot.purge_from(channel, limit=100, check=is_me)
    yield from bot.send_message(channel, 'Deleted {} message(s)'.format(len(deleted)))

# Follow this helpful guide on creating a bot and adding it to your server. 
# https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token
bot.run('token')
