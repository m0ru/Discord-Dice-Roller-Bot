# Discord-Dice-Roller-Bot
A bot that handles rolls for Shadowrun Anarchy

# Dependencies
This bot is extended from [Discord.py] (https://github.com/Rapptz/discord.py/). Install Discord.py prior to running this bot.

#Python Version
This requires Python 3.4.1+. If you are using Python 3.5:

Replace `async def` instead of `@asyncio.corouting` and `await` instead of `yield from`

# Usage
1. Follow the directions [here] (https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token) to create a bot token.
2. Add the bot to the servers you want.
3. Place the token in the last line of the script.
4. Launch script.

# Commands
`!purge`
Deletes all messages made from the bot. Used to clean up after a session.

`!roll`
Supported rolls are:
- !roll # - Rolls # of d6 (max 200), returns number of hits.

#Modifiers
- `>` Success marker. !roll 12>3 will say "Success" if number of hits is 3 or higher or "Failure" if not. Will also show net hits.
- `r` Reroll. Rerolls number of misses. !roll 12r3 will reroll up to 3 missed dice.
- 'e' Pre-Edge. Adds one die to the total and counts 4s as hits. !roll 12e
- 'g' Live Dangerously. Adds an exploit/glitch die to the roll. !roll 12g

You can string these together:
- `!roll 10>4r3eg` would roll 11d6, give a count of how many are 4 or higher, reroll up to 3 misses, advise if the roll got more than 4 hits, and roll a glitch/exploit die.
