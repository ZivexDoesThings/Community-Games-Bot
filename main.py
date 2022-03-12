import discord
from discord.ext import tasks, commands
import random
import time
import asyncio
import logging
import pickle
import itertools
import traceback
from collections import Counter
from operator import itemgetter
from emoji import UNICODE_EMOJI
from languages import *

token = ""
default_prefix = "cg."
dev_user_ids = [
    # Put your user ID(s) in int format here to run dev-only commands - more info in the README
    ]

def get_prefix(bot, msg):
    return prefixes.get(msg.guild.id, default_prefix)

# With Shards
bot = commands.AutoShardedBot(command_prefix=get_prefix, intents=discord.Intents.all())
# Without Shards
#bot = commands.Bot(command_prefix = get_prefix, intents=discord.Intents.all())


# Loads (or creates if unavailable) player statistics file
try:
    file = open('windata.pkl', 'rb')
    windata = pickle.load(file)
    file.close()

except:
    print("No win data file available. Creating new one...")
    windata = {}

# Server prefix storage file
try:
    file = open('prefixes.pkl', 'rb')
    prefixes = pickle.load(file)
    file.close()
except:
    print("No prefix file available. Creating new one...")
    prefixes = {}

# Server language storage file
try:
    file = open('lang.pkl', 'rb')
    langs = pickle.load(file)
    file.close()
except:
    print("No language file available. Creating new one...")
    langs = {}

# Premium-enabled users/servers storage file
try:
    file = open('premium.pkl', 'rb')
    premium = pickle.load(file)
    file.close()
except:
    print("No premium data save available. Creating blank template...")
    # Enables premium features for all the original contributors
    premium = {
        449433954529837056:["🌌", 0x3b2266],
        146009145290653696:[0, ""],
        317778691390439424:[0, ""],
        629082225014734851:[0, ""],
        350363572045348875:[0, ""],
        640872118107504650:[0, ""],
        387918981698289674:[0, ""],
        657394368789086218:0
        }

def flatten(x):
    return list(itertools.chain(*x))


logger = logging.getLogger()
logging.basicConfig(filename='errorlog.log', level=logging.ERROR, format='''
%(asctime)s - %(message)s''', datefmt='%d/%m/%Y %I:%M:%S %p')

bot.remove_command('help')
gamesPlayed = {}
inGame = {}
killing = []
pending_reactions = []
pending_messages = []
nextID = 1
killingBot = False

@bot.event
async def on_ready():
    global statuses
    statuses = ["games in " + str(len(bot.guilds)) + " servers.",
                'Type ' + default_prefix + 'help to get started!']


async def sendPromo(ctx): # Sends a message promoting the Patreon page, called after several games are played with the same person in a short space of time
    global langs
    if ctx.guild.id in langs: lang = langs[ctx.guild.id]
    else: lang = "English"
    colours = [0xd41608, 0x595ef7, 0xffd91c, 0x42bdbb, 0x149c14, 0xb135c4, 0xe60b92]
    embed = discord.Embed(
        title = random.choice(Language(lang).promotitles),
        description = random.choice(Language(lang).promodesc),
        colour = random.choice(colours))
    await ctx.send(content=None, embed=embed)

def check_emoji(user):
    def get_emoji(emoji):
        colon_count = 0
        id_string = ""
        for char in emoji:
            if colon_count == 2 and char != ">":         
                id_string += char
            if char == ":": colon_count += 1
        return bot.get_emoji(int(id_string))

    if user in premium:
        if premium[user][0] in UNICODE_EMOJI: return
        elif type(premium[user][0]) != int:
            if get_emoji(premium[user][0]).is_usable(): return
            else: premium[user][0] = 0

class LoopsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.index = 0
        self.change_status.start()
        self.prune_users.start()
    
    @tasks.loop(seconds=8.0)
    async def change_status(self): # Cycles through the list of statuses
        global killingBot
        global statuses
        statuses[0] = "games in " + str(len(bot.guilds)) + " servers." # Updates the number of servers shown in the status
        if not killingBot: await self.bot.change_presence(activity=discord.Game(name=statuses[(self.change_status.current_loop % len(statuses))]))
        else: await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="Heads up, I'm about to go offline for a bit."))
    
    @tasks.loop(minutes=120.0)
    async def prune_users(self):
        global gamesPlayed
        global windata
        await asyncio.sleep(20)
        gamesPlayed = {} # Clears the number of games played per person (which resets the triggers for the sendPromo function
        for user in windata:
            if not bot.get_user(user): del windata[user] # Removes the user from the stats when an attempt to find the user returns None, meaning the user no longer exists
            try:
                if bot.get_user(user).bot: del windata[user] # Will remove bot users from the stats
            except: pass

        
    
    @change_status.before_loop
    async def before_status(self):
        await self.bot.wait_until_ready()
        print("Logged in as " + str(self.bot.user))
        
    @prune_users.before_loop
    async def before_reset(self):
        await self.bot.wait_until_ready()

@bot.event
async def on_raw_reaction_add(payload):
    if not bot.get_user(payload.user_id).bot:
        for i in pending_reactions:
            try:
                if type(i.parent).__name__ == "PreGame":
                    if i.parent.game.name == "Mega Connect 4":
                        valid_user = True
                    else:
                        valid_user = False
                        for user in i.users:
                            if payload.user_id == user.id:
                                valid_user = True
                    if payload.message_id == i.msg.id and str(payload.emoji) in i.emoji and valid_user:
                        i.reaction = str(payload.emoji)
                        i.react_user = bot.get_user(payload.user_id)
                        return
            except:
                pass
            try:
                if type(i).__name__ == "Game":
                    if i.name == "Hangman":
                        valid = False
                        for player in i.players:
                            if player.id == payload.user_id:
                                valid = True
                        if valid:
                            i.votes[str(payload.emoji)] += 1
                        return
                    else:
                        valid_user = False
                        for user in i.users:
                            if payload.user_id == user.id:
                                valid_user = True
                        if payload.message_id == i.msg.id and str(payload.emoji) in i.emoji and valid_user:
                            i.reaction = str(payload.emoji)
                            i.react_user = bot.get_user(payload.user_id)
                            return
            except:
                pass
            valid_user = False
            try:
                for user in i.users:
                    if payload.user_id == user.id: valid_user = True
            except:
                try:
                    for user in i.players:
                        if payload.user_id == user.id: valid_user = True
                except: valid_user = True
            if payload.message_id == i.msg.id and str(payload.emoji) in i.emoji and valid_user:
                i.reaction = str(payload.emoji)
                i.react_user = bot.get_user(payload.user_id)

@bot.event
async def on_message(message):
    if message.guild: # Processes commands if a message is received in a server - not a DM channel
        await bot.process_commands(message)
    global pending_messages
    for i in pending_messages: # Iterates through the list of messages it's waiting on in Hangman games
        try:
            if message.channel.id == i.channel.id and message.author in i.users: i.message = message
        except:
            if message.channel.id == i.users[0].dm_channel.id and message.author in i.users: i.message = message


class Kill(Exception):
    pass

class Timer:
    def __init__(self, timeout):
        self.timed_out  = False
        self.timeout = timeout
        self.start_time = time.perf_counter()
        self.elapsed = 0

class ReactionTimeout:
    def __init__(self, parent, users, seconds, msg, emoji):
        self.parent = parent
        self.users = users
        self.time = seconds
        self.msg = msg
        self.emoji = emoji

    async def run(self):
        global pending_reactions
        self.timed_out = False
        self.reaction = ""
        self.react_user = ""
        self.timer = Timer(self.time)
        pending_reactions.append(self)
        while self.timer.elapsed < self.time:
            await asyncio.sleep(0.1)
            if type(self.parent).__name__ != "PreGame" and type(self.parent).__name__ != "Setup" and type(self.parent).__name__ != "Nothing":
                self.parent.killcheck()
            elif type(self.parent).__name__ == "Setup":
                self.parent.parent.killcheck()
            self.timer.elapsed = time.perf_counter() - self.timer.start_time
            if self.reaction:
                break
        pending_reactions.remove(self)
        if self.timer.elapsed >= self.timer.timeout:
            self.timed_out = True
        return self.reaction, self.react_user

class MessageTimeout:
    def __init__(self, parent, users, seconds, channel):
        self.parent = parent
        self.users = users
        self.time = seconds
        self.channel = channel
        self.timer = 0

    async def run(self):
        global pending_messages
        self.timed_out = False
        self.message = ""
        self.timer = Timer(self.time)
        pending_messages.append(self)
        while self.timer.elapsed < self.time:
            await asyncio.sleep(0.1)
            if type(self.parent).__name__ == "Setup": self.parent.parent.killcheck()
            else: self.parent.killcheck()
            self.timer.elapsed = time.perf_counter() - self.timer.start_time
            if self.message: break
        pending_messages.remove(self)
        if self.timer.elapsed >= self.timer.timeout:
            self.timed_out = True
        return self.message

@bot.event
async def on_command_error(ctx, error):
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id])
    else: lang = Language("English")
    if isinstance(error, commands.CommandNotFound): return
    if isinstance(error, commands.MemberNotFound):
        await ctx.send(lang.cantFindPerson)
        return
    if isinstance(error, discord.errors.Forbidden): return
    if isinstance(error, discord.errors.NotFound): return
    info = traceback.format_exception(type(error), error, error.__traceback__)
    logger.exception(("Error - Original Message: \"" + ctx.message.content + "\" - Server: " + ctx.guild.name + " - Channel: " + ctx.channel.name + "\n" + "".join(info)), exc_info=False)
    
#------------------------------------------------------------------- PRE-GAME SETUP CLASS -------------------------------------------------------------------
#############################################################################################################################################################
    
class PreGame:
    def __init__(self, ctx, game, player2, limitRange, premRange):
        self.ctx = ctx
        self.game = game
        self.player2 = player2
        self.limitRange = list(limitRange)
        self.premRange = list(premRange)
        global langs
        if self.ctx.guild.id in langs: self.lang = Language(langs[ctx.guild.id])
        else: self.lang = Language("English")

    async def checkPerms(self): # Checks that the bot has all the permissions needed to run the game, and will notify the user and cancel the game if anything is missing
        self.needed = ["Add Reactions", "Manage Messages", "Read Message History", "Use External Emojis"]
        perms = self.ctx.guild.get_member(bot.user.id).permissions_in(self.ctx.channel)
        if perms.add_reactions:
            self.needed.remove("Add Reactions")
        if perms.manage_messages:
            self.needed.remove("Manage Messages")
        if perms.read_message_history:
            self.needed.remove("Read Message History")
        if perms.external_emojis or self.game.name == "MasterMind":
            self.needed.remove("Use External Emojis")
        if len(self.needed) == 1:
            self.lang.update(permission=self.needed[0])
            await self.ctx.send(self.lang.needPerms)
        elif len(self.needed) == 0:
            if self.game.name == "Mega Connect 4": await self.startmc4() # Separate functions for MC4 and Hangman due to their multiplayer nature - MC4 needing 4 players, and Hangman having no limit on player count
            elif self.game.name == "Hangman": await self.startunlimited()
            else: await self.startup()
        else:
            self.lang.update(permission=self.needed)
            await self.ctx.send(self.lang.needPerms)


    async def startup(self):
        global killingBot
        global inGame
        self.lang.update(game=self.game.name)
        if not self.player2: # Tells the player they need to mention an opponent if none is entered in the command
            await self.ctx.send(self.lang.mentionOpponent + self.game.prefix + self.game.name.lower().replace(" ", "") + " " + bot.user.mention)
            return
        p1 = self.ctx.author
        p2 = None
        for person in self.ctx.guild.members:
            if person.id == self.player2.id:
                p2 = person
                if person.bot: # Disallows bots from being mentioned as an opponent
                    await self.ctx.send(self.lang.botsCantPlay)
                    return
        if p1.id == p2.id: # Prevents the user from playing against themself
            await self.ctx.send(self.lang.cantPlayAgainstSelf)
            return
        response = ""
        p1ingame = False
        p2ingame = False
        for game in inGame: # Iterates through the current running games and checks if either player is currently in a game
            if p1 in inGame[game].players and p2 in inGame[game].players:
                await self.ctx.send(self.lang.bothPlaying)
                return
            elif p1 in inGame[game].players:
                response = self.lang.youreAlreadyPlaying
                p1ingame = True
            elif p2 in inGame[game].players:
                self.lang.update(p2.name)
                response = self.lang.theyreAlreadyPlaying
                p2ingame = True
            if p1ingame and p2ingame:
                response = self.lang.bothPlayingElsewhere
                break
        if response != "": # Sends the appropriate response from the above for loop
            await self.ctx.send(response)
            return
        if str(p2.status) == "offline": # Prevents the user from playing with someone offline
            await self.ctx.send(self.lang.theyreOffline)
            return
        if killingBot: # Prevents the game from starting when the kill command is run by a dev
            await self.ctx.send(self.lang.downtime)
            return
        self.lang.update(p2.mention, self.game.name)
        self.msg = await self.ctx.send(self.lang.reactToStartGame)
        await self.msg.add_reaction("✅")
        timeout = ReactionTimeout(self, [p2], 180, self.msg, ["✅"])
        emoji, user = await timeout.run()
        if emoji != "": # If the opponent responded to the message in time
            await self.msg.clear_reactions()
            response = ""
            p1ingame = False
            p2ingame = False
            for game in inGame: # Checks if either player has since entered a game somewhere, and will cancel the game in that case
                if p1 and p2 in inGame[game].players:
                    await self.msg.edit(content=self.lang.goneElsewhere)
                    del inGame[self.game.gameID]
                    return
                elif p1 in inGame[game].players:
                    self.lang.update(p1.name)
                    response = self.lang.userInOtherGame
                    p1ingame = True
                elif p2 in inGame[game].players:
                    self.lang.update(p2.name)
                    response = self.lang.finishOtherGameFirst
                    p2ingame = True
                if p1ingame and p2ingame:
                    response = Language(self.lang).bothGone
                    break
            if response != "": # Sends the appropriate response from the above for loop
                await self.msg.edit(content=response)
                return
            if str(p1.status) == "offline":
                self.lang.update(p1.name)
                await self.msg.edit(content=self.lang.userWentOffline)
            else:
                await self.msg.delete()
                self.game.players = [p1, p2]
                random.shuffle(self.game.players) # Randomises the order of the players, ready for the game to start
                del self.lang
        else: # If the ReactionTimeout object timed out, the message will be edited to reflect that
            try:
                self.lang.update(p2.name)
                await self.msg.edit(content=(self.lang.noResponse))
                await self.msg.clear_reactions()
            except:
                pass

    async def startmc4(self):
        global inGame
        players = []
        p1 = self.ctx.author
        self.lang.update(p1.name)
        for game in inGame: # Checks if the player initialising the game is currently playing, and cancels if that's the case
            if self.ctx.author in inGame[game].players:
                await self.ctx.send(self.lang.finishOtherGameFirst)
                return
        msg = await self.ctx.send(content=(self.lang.whosPlaying4))
        await msg.add_reaction("✅")
        players = []
        
        # NOTE - THIS SECTION MAY NEED REPLACING WITH A REACTIONTIMEOUT OBJECT BASED SYSTEM; BOT.WAIT_FOR SOMETIMES FAILS TO RECOGNISE REACTIONS
        # Or, y'know, use buttons, since they exist now
        def check(reaction, user):
            return str(reaction.emoji) == "✅" and reaction.message.id == msg.id
        while len(players) < 3: 
            try: 
                reaction, user = await bot.wait_for('reaction_add', timeout=120, check=check) 
            except asyncio.TimeoutError: # If the reaction timeout triggers
                self.game.players = []
                try:
                    await msg.edit(content=self.lang.noOneWantsToPlay)
                    await msg.clear_reactions()
                except:
                    pass
                return
            players = await reaction.users().flatten()
            for user in players: # Checks for users that have gone offline or entered another game and removes them from the reaction list (and therefore the player list
                if str(user.status) == "offline" or user in inGame or user == p1:
                    await reaction.remove(user)
            players = await reaction.users().flatten()
            for user in players: # Removes bots and the user that ran the command from the player list (they are added at the end)
                if user.bot or user == p1: players.remove(user)
                    
        await msg.delete()
        self.game.players = [p1, players[0], players[1], players[2]]
        random.shuffle(self.game.players) # Randomises the order of the players
        del self.lang

    async def startunlimited(self):
        global inGame
        players = []
        p1 = self.ctx.author
        self.lang.update(p1.name)
        for game in inGame: # Cancels the command if the person running it is already in a different game
            if self.ctx.author in inGame[game].players:
                await self.ctx.send(self.lang.finishOtherGameFirst)
                return
        self.lang.update(p1.name, self.game.name)
        msg = await self.ctx.send(self.lang.whosPlayingUnlimited)
        await msg.add_reaction("✅")
        players = []
        self.isPremium = False
        for a in list(premium): # Checks whether the user or server has premium features enabled (which will allow a higher player count)
            if a == p1.id or a == self.ctx.guild.id: self.isPremium = True
        
        # NOTE - THIS SECTION MAY NEED REPLACING WITH A REACTIONTIMEOUT OBJECT BASED SYSTEM; BOT.WAIT_FOR SOMETIMES FAILS TO RECOGNISE REACTIONS
        # Or, y'know, use buttons, since they exist now
        def check(reaction, user):
            return str(reaction.emoji) == "✅" and reaction.message.id == msg.id
        while True:
            try: reaction, user = await bot.wait_for('reaction_add', timeout=120, check=check)
            except asyncio.TimeoutError:
                await msg.edit(content=self.lang.cancelUnlimited)
                await msg.clear_reactions()
                self.game.players = []
                return
            players = await reaction.users().flatten()
            for user in players: # Removes people that have entered another game or gone offline from the reactions, and therefore the player list
                if str(user.status) == "offline" or user in inGame: await reaction.remove(user)
            players = await reaction.users().flatten()
            for user in players:
                if user.bot: players.remove(user)
            if p1 in players: break # Starts the game if the user that ran the command reacts with the tick, regardless of player count
            elif self.isPremium and len(players) == 15: # Starts the game with the max amount of players (16)
                players.append(p1)
                await msg.clear_reactions()
                await msg.edit(content=self.lang.startMaxPlayers)
                await asyncio.sleep(4)
                break
            elif not self.isPremium and len(players) >= 3: # Starts the game with the max amount of players (4) and promotes premium features
                players.append(p1)
                self.lang.update(number=16)
                await msg.clear_reactions()
                await msg.edit(content=self.lang.startMaxPlayers + "\n" + self.lang.premiumCanHaveMore)
                await asyncio.sleep(4)
                break
        
        
        await msg.delete()
        random.shuffle(players)
        self.game.players = players
        del self.lang




# ------------------------------------------------------------------------------------------------ GAME CLASS ------------------------------------------------------------------------------------------------
#######################################################################################################################################################################################

class Game: 
    def __init__(self, ctx, game, player2="", mode="", limitRange=[], premRange=[]):
        global prefixes
        self.ctx = ctx
        self.player2 = player2
        self.name = game
        self.mode = mode
        self.limitRange = list(limitRange)
        self.premRange = list(premRange)
        if self.ctx.guild.id in prefixes:
            self.prefix = prefixes[self.ctx.guild.id]
        else:
            self.prefix = default_prefix
        if self.ctx.guild.id in langs: self.lang = Language(langs[ctx.guild.id])
        else: self.lang = Language("English")

    def killcheck(self):
        global killing
        if self.gameID in killing:
            raise Kill

    async def pregame(self):
        global inGame
        global nextID
        pg = PreGame(self.ctx, self, self.player2, self.limitRange, self.premRange)
        self.players = None
        await pg.checkPerms()
        if self.players:
            self.gameID = int(nextID)
            nextID += 1
            inGame[self.gameID] = self
            random.shuffle(self.players)
            if self.name == "Connect 4":
                await self.connect4()
            elif self.name == "Tic Tac Toe":
                await self.tictactoe()
            elif self.name == "MasterMind":
                await self.mastermind()
            elif self.name == "Battleship":
                await self.battleship()
            del self.lang
        else: del self

    async def unlimitedpregame(self):
        global inGame
        global nextID
        pg = PreGame(self.ctx, self, "", [1, 2, 3, 4], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
        await pg.checkPerms()
        if len(self.players) != 0:
            self.gameID = int(nextID)
            nextID += 1
            inGame[self.gameID] = self
            random.shuffle(self.players)
            await self.hangman()
            del self.lang
        else: del self
        
    async def mc4pregame(self):
        global inGame
        global nextID
        pg = PreGame(self.ctx, self, "", [4], [3, 4, 5, 6])
        await pg.checkPerms()
        if self.players:
            self.gameID = int(nextID)
            nextID += 1
            inGame[self.gameID] = self
            await self.megaconnect4()
            del self.lang
        else: del self

    def update_stats(self):
        if self.win != "Draw" and self.name != "Hangman":
            userHasData = False
            for user in windata:
                if user == self.win.id:
                    userHasData = True
                    windata[user]["T"]["W"] += 1
                    windata[user][self.name]["W"] += 1
                    break
            if not userHasData:
                windata[self.win.id] = {"T" : {"W": 1, "P" : 0, "D" : 0},
                                        "Connect 4" : {"W": 0, "P" : 0, "D" : 0},
                                        "Tic Tac Toe" : {"W": 0, "P" : 0, "D" : 0},
                                        "Mega Connect 4" : {"W": 0, "P" : 0, "D" : 0},
                                        "MasterMind": {"W": 0, "P" : 0, "D" : 0},
                                        "Battleship" : {"W": 0, "P" : 0, "D" : 0},
                                        "Hangman" : {"Co-op": {"W":0, "P":0}, "Comp":{"W":0, "P":0}}
                                        }
                windata[self.win.id][self.name]["W"] = 1
            for player in inGame[self.gameID].players:
                userHasData= False
                for user in windata:
                    if user == player.id:
                        userHasData = True
                        windata[user]["T"]["P"] += 1
                        windata[user][self.name]["P"] += 1
                        break
                if not userHasData:
                    windata[player.id] = {"T" : {"W": 0, "P" : 1, "D" : 0},
                                        "Connect 4" : {"W": 0, "P" : 0, "D" : 0},
                                        "Tic Tac Toe" : {"W": 0, "P" : 0, "D" : 0},
                                        "Mega Connect 4" : {"W": 0, "P" : 0, "D" : 0},
                                        "MasterMind": {"W": 0, "P" : 0, "D" : 0},
                                        "Battleship" : {"W": 0, "P" : 0, "D" : 0},
                                        "Hangman" : {"Co-op": {"W":0, "P":0}, "Comp":{"W":0, "P":0, "D":0}}
                                        }
                    windata[player.id][self.name]["P"] = 1
        elif self.name != "Hangman":
            for player in inGame[self.gameID].players:
                userHasData= False
                for user in windata:
                    if user == player.id:
                        userHasData = True
                        windata[user]["T"]["D"] += 1
                        windata[user][self.name]["D"] += 1
                        break
                if not userHasData:
                    windata[player.id] = {"T" : {"W": 0, "P" : 0, "D" : 1},
                                        "Connect 4" : {"W": 0, "P" : 0, "D" : 0},
                                        "Tic Tac Toe" : {"W": 0, "P" : 0, "D" : 0},
                                        "Mega Connect 4" : {"W": 0, "P" : 0, "D" : 0},
                                        "MasterMind": {"W": 0, "P" : 0, "D" : 0},
                                        "Battleship" : {"W": 0, "P" : 0, "D" : 0},
                                        "Hangman" : {"Co-op": {"W":0, "P":0}, "Comp":{"W":0, "P":0, "D":0}}
                                        }
                    windata[player.id][self.name]["D"] += 1
        elif self.name == "Hangman":
            self.mode = self.mode.capitalize()
            if self.mode == "Co-op" and len(self.players) == 1:
                del inGame[self.gameID]
                return
            for player in [p.id for p in self.win]:
                userHasData = False
                for user in windata:
                    if user == player:
                        userHasData = True
                        windata[user]["T"]["W"] += 1
                        windata[user]["Hangman"][self.mode]["W"] += 1
                        break
                if not userHasData:
                    windata[player] = {"T" : {"W": 1, "P" : 0, "D" : 0},
                                    "Connect 4" : {"W": 0, "P" : 0, "D" : 0},
                                    "Tic Tac Toe" : {"W": 0, "P" : 0, "D" : 0},
                                    "Mega Connect 4" : {"W": 0, "P" : 0, "D" : 0},
                                    "MasterMind": {"W": 0, "P" : 0, "D" : 0},
                                    "Battleship" : {"W": 0, "P" : 0, "D" : 0},
                                    "Hangman" : {"Co-op": {"W":0, "P":0}, "Comp":{"W":0, "P":0}}
                                    }
                    windata[player]["Hangman"][self.mode]["W"] = 1
            if self.mode == "Co-op": people = [m.id for m in self.players]
            else: people = [m.id for m in self.all_players]
            for person in people:
                userHasData = False
                for user in windata:
                    if user == person:
                        userHasData = True
                        windata[user]["T"]["P"] += 1
                        windata[user]["Hangman"][self.mode]["P"] += 1
                        break
                if not userHasData:
                    windata[person] = {"T" : {"W": 0, "P" : 1, "D" : 0},
                                        "Connect 4" : {"W": 0, "P" : 0, "D" : 0},
                                        "Tic Tac Toe" : {"W": 0, "P" : 0, "D" : 0},
                                        "Mega Connect 4" : {"W": 0, "P" : 0, "D" : 0},
                                        "MasterMind": {"W": 0, "P" : 0, "D" : 0},
                                        "Battleship" : {"W": 0, "P" : 0, "D" : 0},
                                        "Hangman" : {"Co-op": {"W":0, "P":0}, "Comp":{"W":0, "P":0}}
                                        }
                    windata[person]["Hangman"][self.mode]["P"] = 1
        del inGame[self.gameID]
        file = open('windata.pkl', 'wb')
        pickle.dump(windata, file, protocol=4)
        file.close()
    



# -------------------------------------------------------------------------------------------------------   C O N N E C T   4   -------------------------------------------------------------------------------------



    async def connect4(self):
        global inGame
        global windata
        global nextID
        global gamesPlayed
        numReact = [
            "1️⃣",
            "2️⃣",
            "3️⃣",
            "4️⃣",
            "5️⃣",
            "6️⃣",
            "7️⃣",
            ]
        available = [
            "1️⃣",
            "2️⃣",
            "3️⃣",
            "4️⃣",
            "5️⃣",
            "6️⃣",
            "7️⃣",
            ]
        counters = [["\U0001F7E1", 0xffff00], ["\U0001F534", 0xff0000]]
        for p in self.players:
            if p.id in premium:
                check_emoji(p.id)
                if type(premium[p.id][0]) == str: counters[self.players.index(p)][0] = premium[p.id][0]
                if type(premium[p.id][1]) == int: counters[self.players.index(p)][1] = premium[p.id][1]
        if counters[0][0] == counters[1][0]:
            counters = [["\U0001F7E1", counters[0][1]], ["\U0001F534", counters[0][1]]]
        self.p1 = self.players[0]
        self.p2 = self.players[1]
        try:
            self.lang.update(", ".join(player.mention for player in self.players))
            self.msg = await self.ctx.send(self.lang.gameStarting)
            for i in numReact:
                await self.msg.add_reaction(i)
            autoanswer = False
            offlineanswer = False
            darken = "<:darken:722694104718508072>"
            boardlist = [[darken, darken, darken, darken, darken, darken, darken] for i in range(6)]
            def boardGen():
                board = "\n".join("".join(i) for i in boardlist)
                board += "\n1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣"
                return board
            finished = False
            self.win = ""
            content = counters[0][0] + " - " + self.players[0].name + "\n" + counters[1][0] + " - " + self.players[1].name
            turn = self.players[1]
            while not finished:
                if turn == self.players[0]:
                    turn = self.players[1]
                else:
                    turn = self.players[0]
                colour = counters[self.players.index(turn)][1]
                board = boardGen()
                self.killcheck()
                self.lang.update(turn.name)
                embed = discord.Embed(
                    title = self.lang.playersTurn,
                    description = board,
                    colour = colour,
                    )
                if autoanswer:
                    if turn == self.players[0]:
                        self.lang.update(self.players[1].name)
                        embed.set_footer(text=(self.lang.c4Timeout + "\n" + self.lang.c4HowTo))
                    else:
                        self.lang.update(self.players[0].name)
                        embed.set_footer(text=self.lang.c4Timeout + "\n" + self.lang.c4HowTo)
                elif offlineanswer:
                    if turn == self.players[0]:
                        self.lang.update(self.players[1].name)
                        embed.set_footer(text=(self.lang.c4Offline + "\n" + self.lang.c4HowTo))
                    else:
                        self.lang.update(self.players[0].name)
                        embed.set_footer(text=(self.lang.c4Offline + "\n" + self.lang.c4HowTo))
                else:
                    embed.set_footer(text=self.lang.c4HowTo)
                await self.msg.edit(content=content, embed=embed)
                for i in numReact:
                    if boardlist[0][numReact.index(i)] != darken:
                        await self.msg.remove_reaction(i, bot.user)
                        if i in available:
                            available.remove(i)
                if str(turn.status) != "offline":
                    timeout = ReactionTimeout(self, [turn], 30, self.msg, available)
                    emoji, user = await timeout.run()
                    if emoji != "":
                        response = numReact.index(emoji)
                        await self.msg.remove_reaction(emoji, turn)
                        autoanswer = False
                        offlineanswer = False
                    else:
                        response = random.randint(0, 7)
                        while (str(response + 1) + "️⃣") not in available:
                            response = random.randint(0, 7)
                        autoanswer = True
                        offlineanswer = False
                else:
                    response = random.randint(0, 7)
                    while (str(response + 1) + "️⃣") not in available:
                        response = random.randint(0, 7)
                    autoanswer = False
                    offlineanswer = True
                for row in range(6):
                    if row > 0:
                        boardlist[row-1][response] = darken
                    if turn == self.players[0]:
                        boardlist[row][response] = counters[0][0]
                    else:
                        boardlist[row][response] = counters[1][0]
                    if row < 5 and boardlist[row + 1][response] != darken:
                        break
        #----------------------------------- WIN DETECTION -----------------------------------
                # Draw
                full = True
                for char in boardlist[0]:
                    if char == darken:
                        full = False
                if full == True:
                    self.win = "Draw"
                
                # Horizontal
                index = self.players.index(turn)
                for row in boardlist:
                    for i in range(4):
                        if row[i] == row[i+1] == row[i+2] == row[i+3] == counters[index][0]:
                            self.win = turn
                
                # Vertical
                for column in range(7):
                    for row in range(3):
                        if boardlist[row][column] == boardlist[row+1][column] == boardlist[row+2][column] == boardlist[row+3][column] == counters[index][0]:
                            self.win = turn
                            break
                
                # Diagonal
                for column in range(7):
                    for row in range(6):
                        try:
                            if boardlist[row][column] == boardlist[row+1][column+1] == boardlist[row+2][column+2] == boardlist[row+3][column+3] == counters[index][0]:
                                self.win = turn
                                break
                        except:
                            pass
                        try:
                            if boardlist[row][column] == boardlist[row+1][column-1] == boardlist[row+2][column-2] == boardlist[row+3][column-3] == counters[index][0] and (column - 3) >= 0:
                                self.win = turn
                                break
                        except:
                            pass
                if self.win != "":
                    finished = True
            board = boardGen()
            sendExtra = True
            async for message in self.ctx.channel.history(limit=5):
                if self.msg.id == message.id:
                    sendExtra = False
                    break
            if self.win == "Draw":
                embed = discord.Embed(
                        title = self.lang.draw,
                        description = board,
                        colour = 0x311163,
                        )
                self.lang.update([p.name for p in self.players], "Connect 4")
                if sendExtra: await self.ctx.send(self.lang.endedInDraw)
            else:
                colour = counters[self.players.index(self.win)][1]
                lose = self.players[self.players.index(self.win)-1]
                self.lang.update(self.win.name, "Connect 4", lose.name)
                embed = discord.Embed(
                        title = self.lang.playerWon,
                        description = board,
                        colour = colour,
                        )
                if sendExtra: await self.ctx.send(self.lang.playerWonAgainst)
            await self.msg.clear_reactions()
            await self.msg.edit(content=content, embed=embed)
            self.update_stats()
        except Kill:
            killing.remove(self.gameID)
            embed = discord.Embed(
                    title = self.lang.gameWasStopped,
                    description = board,
                    colour = 0x70081d,
                )
            await self.msg.edit(content=content, embed=embed)
            del inGame[self.gameID]
            if self.p1.id not in gamesPlayed:
                gamesPlayed[self.p1.id] = 0
            if self.p2.id not in gamesPlayed:
                gamesPlayed[self.p2.id] = 0
            gamesPlayed[self.p1.id] += 1
            gamesPlayed[self.p2.id] += 1
            if gamesPlayed[self.p1.id] % 8 == 0 or gamesPlayed[self.p2.id] % 8 == 0:
                await sendPromo(self.ctx)
        except:
            logger.exception(("Error in Connect 4 - Server: " + self.ctx.guild.name + " - Channel: " + self.ctx.channel.name), exc_info=True)
            del inGame[self.gameID]
            try:
                try:
                    embed = discord.Embed(
                            title = self.lang.error,
                            description = board,
                            colour = 0x752219,
                            )
                    await self.msg.edit(content=content, embed=embed)
                except: await self.msg.edit(content=self.lang.errorStopped, embed=embed)
                await self.msg.clear_reactions()
            except: await self.ctx.send(content=self.lang.errorStopped)





# -------------------------------------------------------------------------------------------------------  M E G A   C O N N E C T   4   ----------------------------------------------------------------------------------------------------------




    async def megaconnect4(self): 
        global inGame
        global nextID
        global gamesPlayed
        numReact = [
            "0️⃣",
            "1️⃣",
            "2️⃣",
            "3️⃣",
            "4️⃣",
            "5️⃣",
            "6️⃣",
            "7️⃣",
            "8️⃣",
            "9️⃣",
            "🔟"
            ]
        available = [
            "0️⃣",
            "1️⃣",
            "2️⃣",
            "3️⃣",
            "4️⃣",
            "5️⃣",
            "6️⃣",
            "7️⃣",
            "8️⃣",
            "9️⃣",
            "🔟",
            ]
        default_counters = [["\U0001F7E1", 0xffff00], ["\U0001F534", 0xff0000], ["\U0001F7E2", 0x78b159], ["\U0001F535", 0x55acee]]
        counters = [["", 0], ["", 0], ["", 0], ["", 0]]
        for p in self.players:
            if p.id in premium:
                check_emoji(p.id)
                if type(premium[p.id][0]) == str: counters[self.players.index(p)][0] = premium[p.id][0]
                else: counters[self.players.index(p)][0] = default_counters[self.players.index(p)][0]
                if type(premium[p.id][1]) == int: counters[self.players.index(p)][1] = premium[p.id][1]
                else: counters[self.players.index(p)][1] = default_counters[self.players.index(p)][1]
            else: counters[self.players.index(p)] = default_counters[self.players.index(p)]
        for c in counters:
            for counter in counters:
                if c[0] == counter[0]:
                    counter = default_counters[counters.index(counter)]
                    c = default_counters[counters.index(c)]
        try:
            self.lang.update(", ".join(player.mention for player in self.players))
            self.msg = await self.ctx.send(self.lang.gameStarting)
            for i in numReact:
                await self.msg.add_reaction(i)
            
            autoanswer = False
            offlineanswer = False
            boardlist = ["⚫" * 11] * 10
            def boardGen():
                board = ""
                for a in boardlist: board += a + "\n"
                for b in numReact: board += b
                return board
            finished = False
            self.win = ""
            turn = -1
            content = "\n".join(counters[i][0] + " - " + self.players[i].name for i in range(len(self.players)))
            # -------------------------------   START GAME   ----------------------------------
            while not finished:
                turn += 1
                if turn == 4:
                    turn = 0
                colour = counters[turn][1]
                board = boardGen()
                self.killcheck()
                self.lang.update(self.players[turn].name)
                embed = discord.Embed(
                    title = self.lang.playersTurn,
                    description = board,
                    colour = colour,
                    )
                if autoanswer:
                    self.lang.update(self.players[turn-1].name)
                    embed.set_footer(text=(self.lang.c4Timeout + "\n" + self.lang.c4HowTo))
                elif offlineanswer:
                    self.lang.update(self.players[turn-1].name)
                    embed.set_footer(text=(self.lang.c4Offline + "\n" + self.lang.c4HowTo))
                else:
                    embed.set_footer(text=self.lang.c4HowTo)
                await self.msg.edit(content=content, embed=embed)
                for i in numReact:
                    if boardlist[0][numReact.index(i) - 1][0] != "⚫":
                        await self.msg.remove_reaction(i, bot.user)
                        if i in available:
                            available.remove(i)
                if str(self.players[turn].status) != "offline":
                    timeout = ReactionTimeout(self, [self.players[turn]], 30, self.msg, available)
                    emoji, user = await timeout.run()
                    if emoji != "":
                        response = numReact.index(emoji)
                        await self.msg.remove_reaction(emoji, self.players[turn])
                        autoanswer = False
                        offlineanswer = False
                    else:
                        response = random.randint(0, 11)
                        while (str(response + 1) + "️⃣") not in available:
                            response = random.randint(0, 11)
                        autoanswer = True
                        offlineanswer = False
                else:
                    response = random.randint(0, 11)
                    while (str(response + 1) + "️⃣") not in available:
                        response = random.randint(0, 11)
                    autoanswer = False
                    offlineanswer = True
                
                for row in range(10):
                    if row > 0: boardlist[row-1] = boardlist[row-1][:response] + "⚫" + boardlist[row-1][response+1:]
                    boardlist[row] = boardlist[row][:response] + counters[turn][0] + boardlist[row][response+1:]
                    if row < 9 and boardlist[row+1][response] != "⚫": break

        #----------------------------------- WIN DETECTION -----------------------------------
                # Draw
                full = True
                for char in boardlist[0]:
                    if char == "⚫":
                        full = False
                if full: self.win = "Draw"
                # Horizontal
                for row in boardlist:
                    for i in range(8):
                        if row[i] == row[i+1] == row[i+2] == row[i+3] == counters[turn][0]:
                            self.win = self.players[turn]
                            break
                
                # Vertical
                for column in range(11):
                    for row in range(7):
                        if boardlist[row][column] == boardlist[row+1][column] == boardlist[row+2][column] == boardlist[row+3][column] == counters[turn][0]:
                            self.win = self.players[turn]
                            break
                
                # Diagonal
                for column in range(11):
                    for row in range(10):
                        try:
                            if boardlist[row][column] == boardlist[row+1][column+1] == boardlist[row+2][column+2] == boardlist[row+3][column+3] == counters[turn][0]:
                                self.win = self.players[turn]
                                break
                        except:
                            pass
                        try:
                            if boardlist[row][column] == boardlist[row+1][column-1] == boardlist[row+2][column-2] == boardlist[row+3][column-3] == counters[turn][0] and (column - 3) >= 0:
                                self.win = self.players[turn]
                                break
                        except:
                            pass
                if self.win != "":
                    finished = True
            board = boardGen()
            colour = counters[self.players.index(self.win)][1]
            sendExtra = True
            async for message in self.ctx.channel.history(limit=5):
                if self.msg.id == message.id:
                    sendExtra = False
                    break
            if self.win == "Draw":
                embed = discord.Embed(
                        title = self.lang.draw,
                        description = board,
                        colour = 0x311163,
                        )
                self.lang.update([player.name for player in self.players], "Mega Connect 4")
                if sendExtra: await self.ctx.send(self.lang.endedInDraw)
            else:
                self.lang.update(self.win.name)
                embed = discord.Embed(
                        title = self.lang.playerWon,
                        description = board,
                        colour = colour,
                        )
                if sendExtra: await self.ctx.send(self.win.name + " won the Mega Connect Four game!")
            await self.msg.clear_reactions()
            await self.msg.edit(content=content, embed=embed)
            self.update_stats()
            for player in self.players:
                if player.id not in gamesPlayed:
                    gamesPlayed[player.id] = 0
                gamesPlayed[player.id] += 1
            if gamesPlayed[self.players[0].id] % 8 == 0 or gamesPlayed[self.players[1].id] % 8 == 0 or gamesPlayed[self.players[2].id] % 8 == 0 or gamesPlayed[self.players[3].id] % 8 == 0:
                await sendPromo(self.ctx)
        except Kill:
            killing.remove(self.gameID)
            embed = discord.Embed(
                title = self.lang.gameWasStopped,
                description = board,
                colour = 0x70081d,
                )
            await self.msg.edit(content=content, embed=embed)
            del inGame[self.gameID]
        except:
            logger.exception(("Error in Mega Connect 4 - Server: " + self.ctx.guild.name + " - Channel: " + self.ctx.channel.name), exc_info=True)
            del inGame[self.gameID]
            try:
                try:
                    embed = discord.Embed(
                        title = self.lang.error,
                        description = board,
                        colour = 0x752219,
                        )
                    await self.msg.edit(content=content, embed=embed)
                except:
                    await self.msg.edit(content=self.lang.errorStopped, embed=embed)
                await self.msg.clear_reactions()
            except:
                await self.ctx.send(content=self.lang.errorStopped)


# ------------------------------------------------------------------------------------------------------------------------------  T I C  T A C  T O E  -----------------------------------------------------------------------------------------


    async def tictactoe(self): 
        global inGame
        global nextID
        arrows = [
            "↖️",
            "⬆️",
            "↗️",
            "⬅️",
            "🔵",
            "➡️",
            "↙️",
            "⬇️",
            "↘️"
            ]
        available = [
            "↖️",
            "⬆️",
            "↗️",
            "⬅️",
            "🔵",
            "➡️",
            "↙️",
            "⬇️",
            "↘️"
            ]
        try:
            self.lang.update(", ".join(player.mention for player in self.players))
            self.msg = await self.ctx.send(self.lang.gameStarting)
            for i in arrows:
                await self.msg.add_reaction(i)
            
            turn = self.players[1]
            symbols = [["❌", 0xff9900],["⭕", 0xff9900]]
            darken = "<:darken:722694104718508072>"
            for p in self.players:
                if p.id in premium:
                    check_emoji(p.id)
                    if type(premium[p.id][0]) == str: symbols[self.players.index(p)][0] = premium[p.id][0]
                    if type(premium[p.id][1]) == int: symbols[self.players.index(p)][1] = premium[p.id][1]
            if symbols[0][0] == symbols[1][0]:
                symbols[0][0], symbols[1][0] = "❌", "⭕"
            content = "\n".join(symbols[i][0] + " - " + self.players[i].name for i in range(len(self.players)))
            boardlist = [[darken for i in range(3)] for i in range(3)]
            done = False
            count = 0
            selection = 0
            self.win = ""
            while not done:
                turn = self.players[self.players.index(turn)-1]
                board = "\n──────\n".join("|".join(i) for i in boardlist)
                self.killcheck()
                symbol = symbols[self.players.index(turn)][0]
                colour = symbols[self.players.index(turn)][1]
                self.lang.update(turn.name)
                embed = discord.Embed(
                        title = symbol + self.lang.playersTurn + symbol,
                        description = board,
                        colour = colour
                    )
                if selection == None:
                    self.lang.update(self.players[self.players.index(turn)-1].name)
                    embed.set_footer(text=(self.lang.tttTimeout + "\n\n" + self.lang.tttHowTo))
                else:
                    embed.set_footer(text=self.lang.tttHowTo)
                await self.msg.edit(content=content, embed=embed)
                timeout = ReactionTimeout(self, [turn], 30, self.msg, available)
                emoji, user = await timeout.run()
                if emoji != "":
                    await self.msg.remove_reaction(emoji, user)
                    selection = arrows.index(emoji)
                    await self.msg.remove_reaction(arrows[selection], bot.user)
                    available.remove(arrows[selection])
                    count += 1
                else: selection = None
                if selection != None: boardlist[int(selection/3)][selection % 3] = symbol
                # Win Detection
                for row in boardlist:
                    if row[0] == row[1] == row[2] != darken:
                        self.win = turn
                        done = True
                for column in range(3):
                    if boardlist[0][column] == boardlist[1][column] == boardlist[2][column] != darken:
                        self.win = turn
                        done = True
                if boardlist[0][0] == boardlist[1][1] == boardlist[2][2] != darken:
                    self.win = turn
                    done = True
                if boardlist[0][2] == boardlist[1][1] == boardlist[2][0] != darken:
                    self.win = turn
                    done = True
                if count == 9 and self.win == "":
                    self.win = "Draw"
                    done = True
            lose = self.players[self.players.index(turn)-1]
            board = "\n──────\n".join("|".join(i) for i in boardlist)
            sendExtra = True
            async for message in self.ctx.channel.history(limit=5):
                if self.msg.id == message.id:
                    sendExtra = False
                    break
            if self.win != "Draw":
                self.lang.update(self.win.name, "Tic Tac Toe", lose.name)
                embed = discord.Embed(
                        title = symbol + " " + self.lang.playerWon + " " + symbol,
                        description = board,
                        colour = colour
                    )
                if sendExtra: await self.ctx.send(self.lang.playerWonAgainst)
            else:
                self.lang.update([p.name for p in self.players], "Tic Tac Toe")
                embed = discord.Embed(
                        title = self.lang.draw,
                        description = board,
                        colour = 0xff00ff
                    )
                if sendExtra: await self.ctx.send(self.lang.endedInDraw)
            await self.msg.clear_reactions()
            await self.msg.edit(content=content, embed=embed)
            self.update_stats()
            global gamesPlayed
            for player in self.players:
                if player.id not in gamesPlayed:
                    gamesPlayed[player.id] = 0
                gamesPlayed[player.id] += 1
            if gamesPlayed[self.players[0].id] % 8 == 0 or gamesPlayed[self.players[1].id] % 8 == 0:
                await sendPromo(self.ctx)
        except Kill:
            killing.remove(self.gameID)
            embed = discord.Embed(
                    title = self.lang.gameWasStopped,
                    description = board,
                    colour = 0xff00ff
                )
            await self.msg.edit(content=content, embed=embed)
            await self.msg.clear_reactions()
            del inGame[self.gameID]
        except:
            logger.exception(("Error in Tic Tac Toe - Server: " + self.ctx.guild.name + " - Channel: " + self.ctx.channel.name), exc_info=True)
            del inGame[self.gameID]
            try:
                try:
                    embed = discord.Embed(
                        title = self.lang.error,
                        description = board,
                        colour = 0xff00ff
                    )
                    await self.msg.edit(content=content, embed=embed)
                except:
                    await self.msg.edit(content=self.lang.errorStopped, embed=embed)
                await self.msg.clear_reactions()
            except:
                await self.ctx.send(self.lang.errorStopped)





# ---------------------------------------------------------------------------------------------------------------------------   M A S T E R M I N D   --------------------------------------------------------------------------------



    async def mastermind(self): 
        global inGame
        global nextID
        global gamesPlayed
        p1finished = False
        p2finished = False
        self.p1 = self.players[0]
        self.p2 = self.players[1]
        colours = [0x3f6e34, 0x3f6e34]
        for p in self.players:
            if p.id in premium and type(premium[p.id][1]) == int:
                colours[self.players.index(p)] = premium[p.id][1]
        def results_gen(embed):
            try:
                embed.add_field(name=("**" + self.p1.name + ":**\n" + self.lang.roundNumber + "1: "), value=(prevRounds1[0][0] + "\n" + prevRounds1[0][1]), inline=False)
                for item in prevRounds1:
                    if prevRounds1.index(item) != 0:
                        embed.add_field(name=(self.lang.roundNumber + str(prevRounds1.index(item) + 1) + ": "), value=(item[0] + "\n" + item[1]), inline=False)
                embed.add_field(name="\u200b", value="\u200b", inline=False)
                try:
                    embed.add_field(name=("**" + self.p2.name + ":**\n" + self.lang.roundNumber + "1: "), value=(prevRounds2[0][0] + "\n" + prevRounds2[0][1]), inline=False)
                    for thing in prevRounds2:
                        if prevRounds2.index(thing) != 0:
                            embed.add_field(name=(self.lang.roundNumber + str(prevRounds2.index(thing) + 1) + ": "), value=(thing[0] + "\n" + thing[1]), inline=False)
                except:
                    self.lang.update(self.p2.name)
                    embed.add_field(name=self.lang.userDidNotComplete, value="\u200b", inline=False)
            except:
                embed.add_field(name=self.lang.noRounds, value="\u200b", inline=False)
        if self.mode.lower() in self.lang.modes["number"] or self.mode.lower() in ["numbers", "number", "n"]:
            self.digits = [
                "1️⃣",
                "2️⃣",
                "3️⃣",
                "4️⃣",
                "5️⃣",
                "6️⃣",
                "7️⃣",
                "8️⃣",
                "9️⃣",
                "0️⃣",
                ]
            digitType = "number"
        else:
            self.digits = [
                "🔴",
                "🟠",
                "🟡",
                "🟢",
                "🔵",
                "🟣",
                "🟤",
                "⚪",
                "⚫"
                ]
            digitType = "colour"
        self.lang.update(mode=digitType)
        class Setup:
            def __init__(self, parent, user):
                self.parent = parent
                self.user = user

            async def makeCode(self):
                self.code = list("------")
                try:
                    self.message = await self.user.send(self.parent.lang.prepareMakeCode)
                except:
                    self.parent.lang.update(self.user.mention)
                    await self.parent.msg.edit(content=self.parent.lang.needToDM)
                    self.code = ["unavailable", self.user.mention]
                    return
                for emoji in self.parent.digits:
                    await self.message.add_reaction(emoji)
                try:
                    for i in range(6):
                        embed = discord.Embed(
                            title = self.parent.lang.createCode,
                            description = " ".join(self.code),
                            colour = 0xc9c9c9
                        )
                        embed.set_footer(text=self.parent.lang.mmTimeLimit)
                        await self.message.edit(content=None, embed=embed)
                        timeout = ReactionTimeout(self, [self.user], 20, self.message, self.parent.digits)
                        emoji, person = await timeout.run()
                        if emoji != "":
                            self.code[i] = emoji
                        else:
                            self.code[i] = self.parent.digits[random.randint(0, len(self.parent.digits) - 1)]
                        self.parent.killcheck()
                    embed = discord.Embed(
                            title = self.parent.lang.codeFinished,
                            description = "".join(self.code),
                            colour = 0x00ff00
                        )
                    embed.set_footer(text=self.parent.lang.goToChannel)
                    await self.message.edit(content=None, embed=embed)
                    return
                except Kill:
                    embed = discord.Embed(
                            title = self.parent.lang.gameWasStopped,
                            description = " ".join(self.code),
                            colour = 0x401118
                        )
                    await self.message.edit(content=None, embed=embed)
                    for emoji in self.parent.digits:
                        await self.message.remove_reaction(emoji, bot.user)
                    self.code = "kill"
        
        try:
            self.msg = await self.ctx.send(self.lang.mmWaitForCodes)
            p1code = Setup(self, self.players[0])
            p2code = Setup(self, self.players[1])
            await asyncio.gather(p1code.makeCode(), p2code.makeCode())
            codes = [p1code.code, p2code.code]
            if codes[0] == "kill":
                raise Kill
            unavailable = []
            for code in codes:
                if code[0] == "unavailable":
                    unavailable.append(code[1])
                    del inGame[self.gameID]
            if len(unavailable) == 1:
                self.lang.update(unavailable[0])
                await self.msg.edit(content=self.lang.needToDM)
                return
            elif len(unavailable) == 2:
                self.lang.update(", ".join(unavailable))
                await self.msg.edit(content=self.lang.needToDM)
                return
            await self.msg.delete()
            self.killcheck()
            self.lang.update(", ".join(player.mention for player in self.players))
            self.msg = await self.ctx.send(self.lang.gameStarting)
            for i in self.digits:
                await self.msg.add_reaction(i)
            prevRounds1 = []
            prevRounds2 = []
            p1finished = False
            p2finished = False
            turn = self.players[1]
            
            while (not p1finished) or (not p2finished):
                guess = list("------")
                if turn == self.players[0]:
                    if not p2finished:
                        turn = self.players[1]
                        index = 0
                    else:
                        turn = self.players[0]
                        index = 1
                else:
                    if not p1finished:
                        turn = self.players[0]
                        index = 1
                    else:
                        turn = self.players[1]
                        index = 0
                colour = colours[self.players.index(turn)]
                for i in range(6):
                    self.lang.update(turn.name)
                    if not prevRounds2:
                        embed = discord.Embed(
                        title = self.lang.playersTurn,
                        description = " ".join(guess),
                        colour = colour
                    )
                    else:
                        embed = discord.Embed(
                        title = self.lang.playersTurn,
                        description = self.lang.previousTurns,
                        colour = colour
                    )
                        if turn == self.players[0]:
                            for item in prevRounds1:
                                embed.add_field(name=(self.lang.roundNumber + str(prevRounds1.index(item) + 1) + ": "), value=(item[0] + "\n" + item[1]), inline=False)
                        else:
                            for thing in prevRounds2:
                                embed.add_field(name=(self.lang.roundNumber + str(prevRounds2.index(thing) + 1) + ": "), value=(thing[0] + "\n" + thing[1]), inline=False)
                        embed.add_field(name=self.lang.thisTurn, value=" ".join(guess), inline=False)
                    embed.set_footer(text=self.lang.mmTimeLimit)
                    await self.msg.edit(content=None, embed=embed)
                    self.killcheck()
                    timeout = ReactionTimeout(self, [turn], 20, self.msg, self.digits)
                    emoji, user = await timeout.run()
                    if emoji != "":
                        await self.msg.remove_reaction(emoji, user)
                        guess[i] = emoji
                    else:
                        guess[i] = random.choice(self.digits)
                feedback = ""
                for num in range(6):
                    if guess[num] == codes[index][num]:
                        feedback += "✅"
                    elif guess[num] in codes[index]:
                        feedback += "❔"
                    else:
                        feedback += "❌"
                guess = "".join(guess)
                if turn == self.p1:
                    prevRounds1 += [(guess, feedback)]
                    if feedback == "✅✅✅✅✅✅":
                        p1finished = True
                elif turn == self.p2:
                    prevRounds2 += [(guess, feedback)]
                    if feedback == "✅✅✅✅✅✅":
                        p2finished = True
                self.lang.update(turn.name, mode=digitType)
                embed = discord.Embed(
                        title = self.lang.resultsFromTurn,
                        description = guess +"\n" + feedback,
                        colour = colour
                    )
                embed.set_footer(text=self.lang.mmInfo + "\n\n" + self.lang.reactWhenReady)
                await self.msg.edit(content=None, embed=embed)
                self.killcheck()
                await self.msg.add_reaction("👍") 
                timeout = ReactionTimeout(self, [turn], 30, self.msg, ["👍"])
                emoji, user = await timeout.run()
                await self.msg.clear_reaction("👍")
                self.killcheck()
                if feedback == "✅✅✅✅✅✅" and ((p1finished and not p2finished) or (p2finished and not p1finished)):
                    self.lang.update(turn.name)
                    embed = discord.Embed(
                            title = self.lang.notOverYet,
                            description = self.lang.userFinishGameCont,
                            colour = 0xf20045
                        )
                    await self.msg.edit(content=None, embed=embed)
                    await asyncio.sleep(5)
                self.killcheck()
            if len(prevRounds1) < len(prevRounds2):
                self.win = self.players[0]
                lose = self.players[1]
            elif len(prevRounds1) > len(prevRounds2):
                self.win = self.players[1]
                lose = self.players[0]
            else:
                self.win = "Draw"
            sendExtra = True
            async for message in self.ctx.channel.history(limit=5):
                if self.msg.id == message.id:
                    sendExtra = False
                    break
            
            if self.win == "Draw":
                embed = discord.Embed(
                        title = self.lang.draw,
                        colour = 0x54396e
                    )
                self.lang.update([p.name for p in self.players], "MasterMind")
                if sendExtra: await self.ctx.send(self.lang.endedInDraw)
            else:
                if colours[self.players.index(self.win)] != 0x3f6e34: colour = colours[self.players.index(self.win)]
                else: colour = 0xb242cf
                self.lang.update(self.win.name, "MasterMind", lose.name)
                embed = discord.Embed(
                        title = self.lang.playerWon,
                        colour = colour
                    )
                if sendExtra: await self.ctx.send(self.lang.playerWonAgainst)
            results_gen(embed)
            await self.msg.edit(content=None, embed=embed)
            await self.msg.clear_reactions()
            self.update_stats()
            
            if self.p1.id not in gamesPlayed:
                gamesPlayed[self.p1.id] = 0
            if self.p2.id not in gamesPlayed:
                gamesPlayed[self.p2.id] = 0
            gamesPlayed[self.p1.id] += 1
            gamesPlayed[self.p2.id] += 1
            if gamesPlayed[self.p1.id] % 8 == 0 or gamesPlayed[self.p2.id] % 8 == 0: await sendPromo(self.ctx)
        except Kill:
            killing.remove(self.gameID)
            playersInThisGame = self.players
            del inGame[self.gameID]
            if p1finished and not p2finished:
                self.win = self.players[0]
                lose = self.players[1]
            elif p2finished and not p1finished:
                self.win = self.players[1]
                lose = self.players[0]
            else:
                self.win = ""
            sendExtra = True
            async for message in self.ctx.channel.history(limit=5):
                if self.msg.id == message.id:
                    sendExtra = False
                    break
            if self.win != "":
                self.lang.update(self.win.name, "MasterMind", lose.name)
                if len(prevRounds1) == len(prevRounds2) + 1:
                    embed = discord.Embed(
                                title = self.lang.gameEndedPossibleWinner,
                                colour = 0xa3145e
                            )
                elif len(prevRounds1) <= len(prevRounds2):
                    embed = discord.Embed(
                                title = self.lang.gameEndedWinner,
                                colour = 0xa3145e
                            )
                    if sendExtra: await self.ctx.send(self.lang.playerWonAgainst)
                userHasData = False
                for user in windata:
                    if user == self.win.id:
                        userHasData = True
                        windata[user]["T"]["W"] += 1
                        windata[user]["MasterMind"]["W"] += 1
                        break
                if not userHasData:
                    windata[self.win.id] = {"T" : {"W": 1, "P" : 0, "D" : 0},
                                                        "Connect 4" : {"W": 0, "P" : 0, "D" : 0},
                                                        "Tic Tac Toe" : {"W": 0, "P" : 0, "D" : 0},
                                                        "Mega Connect 4" : {"W": 0, "P" : 0, "D" : 0},
                                                        "MasterMind": {"W": 1, "P" : 0, "D" : 0},
                                                        "Battleship" : {"W": 0, "P" : 0, "D" : 0}}
                for player in self.players:
                    userHasData= False
                    for user in windata:
                        if user == player.id:
                            userHasData = True
                            windata[user]["T"]["P"] += 1
                            windata[user]["MasterMind"]["P"] += 1
                            break
                    if not userHasData:
                        windata[self.win.id] = {"T" : {"W": 0, "P" : 1, "D" : 0},
                                                        "Connect 4" : {"W": 0, "P" : 0, "D" : 0},
                                                        "Tic Tac Toe" : {"W": 0, "P" : 0, "D" : 0},
                                                        "Mega Connect 4" : {"W": 0, "P" : 0, "D" : 0},
                                                        "MasterMind": {"W": 0, "P" : 1, "D" : 0},
                                                        "Battleship" : {"W": 0, "P" : 0, "D" : 0}}
            else:
                embed = discord.Embed(
                            title = self.lang.gameWasStopped,
                            colour = 0x70081d
                        )
            results_gen(embed)
            await self.msg.edit(content=None, embed=embed)
            await self.msg.clear_reactions()
        except:
            logger.exception(("Error in MasterMind - Server: " + self.ctx.guild.name + " - Channel: " + self.ctx.channel.name), exc_info=True)
            del inGame[self.gameID]
            try:
                await self.msg.clear_reactions()
            except:
                pass
            try:
                try:
                    if p1finished and not p2finished:
                        self.win = self.players[0]
                        lose = self.players[1]
                    elif p2finished and not p1finished:
                        self.win = self.players[1]
                        lose = self.players[0]
                    else:
                        self.win = ""
                    if self.win != "":
                        embed = discord.Embed(
                                title = "An error occured, however, " + self.win.name + " won!",
                                colour = 0xe05b4c
                            )
                        userHasData = False
                        for user in windata:
                            if user == self.win.id:
                                userHasData = True
                                windata[user]["T"]["W"] += 1
                                windata[user]["MasterMind"]["W"] += 1
                                break
                        if not userHasData:
                            windata[self.win.id] = {"T" : {"W": 1, "P" : 0, "D" : 0},
                                                                "Connect 4" : {"W": 0, "P" : 0, "D" : 0},
                                                                "Tic Tac Toe" : {"W": 0, "P" : 0, "D" : 0},
                                                                "Mega Connect 4" : {"W": 0, "P" : 0, "D" : 0},
                                                                "MasterMind": {"W": 1, "P" : 0, "D" : 0},
                                                                "Battleship" : {"W": 0, "P" : 0, "D" : 0}}
                        for player in self.players:
                            userHasData= False
                            for user in windata:
                                if user == player.id:
                                    userHasData = True
                                    windata[user]["T"]["P"] += 1
                                    windata[user]["MasterMind"]["P"] += 1
                                    break
                            if not userHasData:
                                windata[self.win.id] = {"T" : {"W": 0, "P" : 1, "D" : 0},
                                                                "Connect 4" : {"W": 0, "P" : 0, "D" : 0},
                                                                "Tic Tac Toe" : {"W": 0, "P" : 0, "D" : 0},
                                                                "Mega Connect 4" : {"W": 0, "P" : 0, "D" : 0},
                                                                "MasterMind": {"W": 0, "P" : 1, "D" : 0},
                                                                "Battleship" : {"W": 0, "P" : 0, "D" : 0}}
                    else:
                        results_gen(embed)
                        embed = discord.Embed(
                                title = self.lang.errorStopped,
                                colour = 0x752219
                            )
                    await self.msg.edit(content=None, embed=embed)
                except:
                    await self.msg.edit(content=self.lang.errorStopped, embed=embed)
            except:
                await self.ctx.send(self.lang.errorStopped)




# ------------------------------------------------------------------------------------------------------------  B A T T L E S H I P  ----------------------------------------------------------------------------




    async def battleship(self): 
        global inGame
        global nextID
        global gamesPlayed
        global premium

        try:
            self.p1, self.p2 = self.players[0], self.players[1]
            self.msg = await self.ctx.send(self.lang.waitForShips)
            
            class Setup:
                def __init__(self, parent, user):
                    self.parent = parent
                    self.user = user
                    
                async def setup(self):
                    ships = {
                        "Aircraft Carrier":5,
                        "Battleship":4,
                        "Destroyer":3,
                        "Submarine":3,
                        "Patrol Boat":2
                             }
                    directions = [
                        "⬆️",
                        "⬇️",
                        "⬅️",
                        "➡️",
                        "🔁",
                        "🎲",
                        "✅"
                        ]
                    boardlist = ["⬛"* 10]* 10
                    board = ""
                    for i in boardlist:
                        board += i + "\n"
                    try: self.message = await self.user.send(self.parent.lang.preparePlaceShips)
                    except:
                        self.parent.lang.update(self.user.mention)
                        await self.parent.msg.edit(content=self.parent.lang.needToDM)
                        self.board = ["unavailable", self.user.mention]
                        return
                    for i in directions:
                        await self.message.add_reaction(i)
                    reset = ["⬛"* 10]* 10
                    info = ["⬛"* 10]* 10
                    inforeset = ["⬛"* 10]* 10
                    row = 0
                    column = 0
                    rotation = ""
                    for ship in ships:
                        done = False
                        if ship == "Aircraft Carrier":
                            letter = "C"
                        elif ship == "Battleship":
                            letter = "B"
                        elif ship == "Destroyer":
                            letter = "D"
                        elif ship == "Submarine":
                            letter = "S"
                        elif ship == "Patrol Boat":
                            letter = "P"
                        def posCheck(r, c, rot):
                            for section in range(ships[ship]):
                                if r > 9 or c > 9: return False
                                if rot == "h":
                                    try:
                                        if boardlist[r][c + section] == "⬜": return False
                                    except: return False
                                elif rot == "v":
                                    try:
                                        if boardlist[r + section][c] == "⬜": return False
                                    except: return False
                            return True
                        firstTime = True
                        while not posCheck(row, column, rotation) or firstTime:
                            rotation = random.choice(("v", "h"))
                            if rotation == "h": row, column = random.randint(0, 9), random.randint(0, (10 - ships[ship]))
                            else: row, column = random.randint(0, (10 - ships[ship])), random.randint(0, 9)
                            firstTime = False
                        if rotation == "h":
                            boardlist[row] = (boardlist[row][:column]  + "⬜"*ships[ship] + boardlist[row][column+ships[ship]:])
                            info[row] = (info[row][:column] + letter*ships[ship] + info[row][column+ships[ship]:])
                        else:
                            for i in range(ships[ship]):
                                boardlist[row+i] = (boardlist[row+i][:column]  + "⬜" + boardlist[row+i][column+1:])
                        board = ""
                        for i in boardlist:
                            board += i + "\n"
                        while not done:
                            self.parent.lang.update(shipType=ship)
                            embed = discord.Embed(
                                title = self.parent.lang.placingShip,
                                description = board,
                                colour = 0x0000ff
                            )
                            embed.set_footer(text=self.parent.lang.positionSetTimeout)
                            await self.message.edit(content=None, embed=embed)
                            self.parent.killcheck()
                            boardlist = list(reset)
                            info = list(inforeset)
                            timeout = ReactionTimeout(self, [self.user], 15, self.message, directions)
                            emoji, user = await timeout.run()
                            if emoji != "":
                                firstTime = True
                                if emoji == directions[0]: # Up
                                    while not posCheck(row, column, rotation) or firstTime:
                                        if row == 0:
                                            if rotation == "v":
                                                row = 11 - ships[ship]
                                            else:
                                                row = 10
                                        row -= 1
                                        firstTime = False
                                elif emoji == directions[1]: # Down
                                    while not posCheck(row, column, rotation) or firstTime:
                                        if (rotation == "v" and row + ships[ship] >= 10) or (rotation == "h" and row >= 9):
                                            row = -1
                                        row += 1
                                        firstTime = False
                                elif emoji == directions[2]: # Left
                                    while not posCheck(row, column, rotation) or firstTime:
                                        if column == 0:
                                            if rotation == "h":
                                                column = 11 - ships[ship]
                                            else:
                                                column = 10
                                        column -= 1
                                        firstTime = False
                                elif emoji == directions[3]: # Right
                                    while not posCheck(row, column, rotation) or firstTime:
                                        if (rotation == "h" and column + ships[ship] >= 10) or (rotation == "v" and column >= 9):
                                            column = -1
                                        column += 1
                                        firstTime = False
                                elif emoji == directions[4]: # Rotate
                                    old_row = row
                                    old_col = column
                                    move_num = 0
                                    if rotation == "h":
                                        if row > 11 - ships[ship]:
                                            row = 11 - ships[ship]
                                        if not posCheck(row, column, "v"):
                                            for x in range(ships[ship]):
                                                column = old_col + x
                                                await asyncio.sleep(0.1)
                                                for y in range(ships[ship]):
                                                    canGoUp = True
                                                    canGoDown = True
                                                    for r in range(y):
                                                        if old_row - r < 0 or boardlist[old_row - r][x] == "⬜":
                                                            canGoUp = False
                                                        try:
                                                            if boardlist[old_row + r][x] == "⬜":
                                                                canGoDown = False
                                                        except:
                                                            canGoDown = False
                                                    if canGoUp:
                                                        row = old_row - y
                                                        if posCheck(row, column, "v"):
                                                            break
                                                    if canGoDown:
                                                        row = old_row + y
                                                        if posCheck(row, column, "v"):
                                                            break
                                                if posCheck(row, column, "v"):
                                                    break
                                        if posCheck(row, column, "v"):
                                            rotation = "v"
                                        else:
                                            row = old_row
                                            column = old_col
                                    else:
                                        if column > 11 - ships[ship]:
                                            column = 11 - ships[ship]
                                        if not posCheck(row, column, "h"):
                                            for y in range(ships[ship]):
                                                row = old_row + y
                                                await asyncio.sleep(0.1)
                                                for x in range(ships[ship]):
                                                    canGoLeft = True
                                                    canGoRight = True
                                                    for c in range(x):
                                                        if old_col - c < 0 or boardlist[y][old_col - c] == "⬜":
                                                            canGoLeft = False
                                                        try:
                                                            if boardlist[y][old_col + c] == "⬜":
                                                                canGoRight = False
                                                        except:
                                                            canGoRight = False
                                                    if canGoLeft:
                                                        column = old_col - x
                                                        if posCheck(row, column, "h"):
                                                            break
                                                    if canGoRight:
                                                        column = old_col + x
                                                        if posCheck(row, column, "h"):
                                                            break
                                                if posCheck(row, column, "h"):
                                                    break
                                        if posCheck(row, column, "h"):
                                            rotation = "h"
                                        else:
                                            row = old_row
                                            column = old_col
                                elif emoji == directions[5]: # Shuffle
                                    firstTime = True
                                    while not posCheck(row, column, rotation) or firstTime:
                                        rotation = random.choice(("v", "h"))
                                        if rotation == "h": row, column = random.randint(0, 9), random.randint(0, (10 - ships[ship]))
                                        else: row, column = random.randint(0, (10 - ships[ship])), random.randint(0, 9)
                                        firstTime = False
                                elif emoji == directions[6]: # Done
                                    done = True
                            else:
                                done = True
                            if rotation == "h":
                                boardlist[row] = (boardlist[row][:column]  + "⬜"*ships[ship] + boardlist[row][column+ships[ship]:])
                                info[row] = (info[row][:column] + letter*ships[ship] + info[row][column+ships[ship]:])
                            else:
                                originalrow = int(row)
                                while True:
                                    try:
                                        for i in range(ships[ship]):
                                            boardlist[row+i] = (boardlist[row+i][:column]  + "⬜" + boardlist[row+i][column+1:])
                                            info[row+i] = (info[row+i][:column]  + letter + info[row+i][column+1:])
                                        break
                                    except:
                                        if row >= 0:
                                            row -= 1
                                        else:
                                            column -= 1
                                            row = int(originalrow)
                            board = ""
                            for i in boardlist:
                                board += i + "\n"
                        ships[ship] = [ships[ship], row, column, rotation]
                        reset = list(boardlist)
                        inforeset = list(info)
                    embed = discord.Embed(
                            title = self.parent.lang.fleetReady,
                            description = board,
                            colour = 0x00ff00
                        )
                    embed.set_footer(text=self.parent.lang.goToChannel)
                    await self.message.edit(content=None, embed=embed)
                    self.board = info
            p1setup = Setup(self, self.players[0])
            p2setup = Setup(self, self.players[1])
            await asyncio.gather(p1setup.setup(), p2setup.setup())
            boards = [p1setup.board, p2setup.board]
            unavailable = []
            for board in boards:
                if board[0] == "unavailable":
                    unavailable.append(board[1])
            if len(unavailable) == 1:
                del inGame[self.gameID]
                self.lang.update(unavailable[0])
                await self.msg.edit(content=self.lang.needToDM)
                return
            elif len(unavailable) == 2:
                del inGame[self.gameID]
                self.lang.update(", ".join(unavailable))
                await self.msg.edit(content=self.lang.needToDM)
                return
            await self.msg.delete()
            self.killcheck()
            letters = [
                    "🇦",
                    "<:letter_b:675874970945191939>",
                    "<:letter_c:675874970642939944>",
                    "<:letter_d:675874970643202059>",
                    "<:letter_e:675874970592739338>",
                    "<:letter_f:675874970508853270>",
                    "<:letter_g:675874970643202098>",
                    "<:letter_h:675874970659848243>",
                    "<:letter_i:675874970714374144>",
                    "<:letter_j:675874970324303893>"
                ]
            numbers = [
                    "1️⃣",
                    "2️⃣",
                    "3️⃣",
                    "4️⃣",
                    "5️⃣",
                    "6️⃣",
                    "7️⃣",
                    "8️⃣",
                    "9️⃣",
                    "🔟"
                ]
            def set_display(board_list):
                display = ("⬛" + "".join(letters) + "\n" + numbers[0] + board_list[0] + "\n" + numbers[1] + board_list[1] + "\n" + numbers[2] + board_list[2] + "\n" +
                        numbers[3] + board_list[3] + "\n" + numbers[4] + board_list[4] + "\n" + numbers[5] + board_list[5] + "\n" + numbers[6] + board_list[6] + "\n" +
                        numbers[7] + board_list[7] + "\n" + numbers[8] + board_list[8] + "\n" + numbers[9] + board_list[9]
                           )
                return display
            self.lang.update(", ".join(player.mention for player in self.players))
            self.msg = await self.ctx.send(self.lang.gameStarting)
            sunk = [[], []]
            turn = self.players[1]
            for emoji in letters:
                await self.msg.add_reaction(emoji)
            for emoji in numbers:
                try: await self.msg.add_reaction(emoji)
                except:
                    for r in self.msg.reactions:
                        if not r.me: await r.clear()
            finished = False
            guesses = [["⬛"* 10] * 10] * 2
            self.win = ""
            colours = [0xffff00, 0xffff00]
            for p in self.players:
                if p.id in premium:
                    colours[self.players.index(p)] = premium[p.id][1]
            while not finished:
                self.killcheck()
                if turn == self.players[0]: turn, other, index = self.players[1], self.players[0], 0
                else: turn, other, index = self.players[0], self.players[1], 1
                
                colour = colours[self.players.index(turn)]
                boardlist = list(guesses[index-1])
                display = set_display(boardlist)
                board = ""
                for i in boardlist:
                    board += i + "\n"
                valid = False
                self.lang.update(turn.name)
                heading = self.lang.userAiming
                while not valid:
                    coordsdisp = "__"
                    coords = []
                    embed = discord.Embed(
                        title = heading,
                        description = display + "\n\n" + coordsdisp,
                        colour = colour
                        )
                    embed.set_footer(text=self.lang.selectX)
                    await self.msg.edit(content=None, embed=embed)
                    timeout = ReactionTimeout(self, [turn], 20, self.msg, letters)
                    emoji, user = await timeout.run()
                    if emoji != "":
                        await self.msg.remove_reaction(emoji, user)
                        coords = [letters.index(emoji)]
                    else:
                        coords = [random.randint(0, 9)]
                    coordsdisp = letters[coords[0]] + "_"
                    embed.description = display + "\n\n" + coordsdisp
                    embed.set_footer(text=self.lang.selectY)
                    await self.msg.edit(content=None, embed=embed)
                    self.killcheck()
                    timeout = ReactionTimeout(self, [turn], 20, self.msg, numbers)
                    emoji, user = await timeout.run()
                    if emoji != "":
                        await self.msg.remove_reaction(emoji, user)
                        coords.append(numbers.index(emoji))
                    else:
                        coords.append(random.randint(0, 9))
                    coordsdisp = letters[coords[0]] + numbers[coords[1]]
                    embed.description = display + "\n\n" + coordsdisp
                    await self.msg.edit(content=None, embed=embed)
                    self.killcheck()
                    if boardlist[coords[1]][coords[0]] != "⬛":
                        heading = self.lang.alreadyFiredThere
                    else:
                        valid = True
                boardlist[coords[1]] = list(boardlist[coords[1]])
                boardlist[coords[1]][coords[0]] = "🟧"
                boardlist[coords[1]] = "".join(boardlist[coords[1]])
                display = set_display(boardlist)
                embed = discord.Embed(
                        title = self.lang.firing,
                        description = display,
                        colour = 0xffffff
                        )
                await self.msg.edit(content=None, embed=embed)
                self.killcheck()
                await asyncio.sleep(1)
                if boards[index][coords[1]][coords[0]] != "⬛":
                    result = self.lang.hit
                    symbol = "💥"
                    colour = 0xff0000
                    boards[index][coords[1]] = list(boards[index][coords[1]])
                    boards[index][coords[1]][coords[0]] = "X"
                    boards[index][coords[1]] = "".join(boards[index][coords[1]])
                    c_count, b_count, d_count, s_count, p_count = 0, 0, 0, 0, 0
                    
                    for row in boards[index]:
                        if "C" in row:
                            c_count += Counter(row)["C"]
                        if "B" in row:
                            b_count += Counter(row)["B"]
                        if "D" in row:
                            d_count += Counter(row)["D"]
                        if "S" in row:
                            s_count += Counter(row)["S"]
                        if "P" in row:
                            p_count += Counter(row)["P"]
                    if "C" not in sunk[index] and c_count == 0:
                        sunk[index].append("C")
                        self.lang.update(turn.name, user2=other.name, shipType="Aircraft Carrier")
                        result = self.lang.sunkShip
                    elif "B" not in sunk[index] and b_count == 0:
                        sunk[index].append("B")
                        self.lang.update(turn.name, user2=other.name, shipType="Battleship")
                        result = self.lang.sunkShip
                    elif "D" not in sunk[index] and d_count == 0:
                        sunk[index].append("D")
                        self.lang.update(turn.name, user2=other.name, shipType="Destroyer")
                        result = self.lang.sunkShip
                    elif "S" not in sunk[index] and s_count == 0:
                        sunk[index].append("S")
                        self.lang.update(turn.name, user2=other.name, shipType="Submarine")
                        result = self.lang.sunkShip
                    elif "P" not in sunk[index] and p_count == 0:
                        sunk[index].append("P")
                        self.lang.update(turn.name, user2=other.name, shipType="Patrol Boat")
                        result = self.lang.sunkShip
                
                else:
                    result = self.lang.missed
                    symbol = "⚪"
                    embed.colour = 0x093291
                boardlist[coords[1]] = list(boardlist[coords[1]])
                boardlist[coords[1]][coords[0]] = str(symbol)
                boardlist[coords[1]] = "".join(boardlist[coords[1]])
                guesses[index-1] = list(boardlist)
                display = set_display(boardlist)
                embed = discord.Embed(
                        title = result,
                        description = display,
                        colour = colour
                        )
                if len(sunk[index-1]) == 5 and turn == self.players[1]:
                    self.win = self.players[0]
                    lose = self.players[1]
                    finished = True
                if len(sunk[index]) == 5 and turn == self.players[1]:
                    if self.win != self.players[0]:
                        self.win = self.players[1]
                        lose = self.players[0]
                    else:
                        self.win = "Draw"
                    finished = True
                await self.msg.edit(content=None, embed=embed)
                self.killcheck()
                await asyncio.sleep(3)
            sendExtra = True
            async for message in self.ctx.channel.history(limit=5):
                if self.msg.id == message.id:
                    sendExtra = False
                    break
            if self.win == "Draw":
                title = self.lang.draw
                self.lang.update([p.name for p in self.players], "Battleship")
                if sendExtra: await self.ctx.send(self.lang.endedInDraw)
            else:
                self.lang.update(self.win.name, "Battleship", lose.name)
                title = self.lang.playerWon
                if sendExtra: await self.ctx.send(self.lang.playerWonAgainst)
            p1shots = "\n".join(guesses[0])
            p2shots = "\n".join(guesses[1])
            self.lang.update(self.players[0].name)
            embed = discord.Embed(
                    title = title,
                    description = self.lang.usersShots + p1shots + "\n\n",
                    colour = 0x5a0266
                    )
            self.lang.update(self.players[1].name)
            embed.description += self.lang.usersShots + p2shots
            await self.msg.edit(content=None, embed=embed)
            await self.msg.clear_reactions()
            self.update_stats()
            if self.p1.id not in gamesPlayed:
                gamesPlayed[self.p1.id] = 0
            if self.p2.id not in gamesPlayed:
                gamesPlayed[self.p2.id] = 0
            gamesPlayed[self.p1.id] += 1
            gamesPlayed[self.p2.id] += 1
            if gamesPlayed[self.p1.id] % 8 == 0 or gamesPlayed[self.p2.id] % 8 == 0:
                await sendPromo(self.ctx)
        except Kill:
            killing.remove(self.gameID)
            try:
                p1remaining = 0
                p2remaining = 0
                for row in boards[1]:
                    p1remaining += Counter(row)["C"] + Counter(row)["B"] + Counter(row)["D"] + Counter(row)["S"] + Counter(row)["P"]
                for row in boards[0]:
                    p2remaining += Counter(row)["C"] + Counter(row)["B"] + Counter(row)["D"] + Counter(row)["S"] + Counter(row)["P"]
                if p1remaining > p2remaining: self.win = self.p2
                elif p1remaining < p2remaining: self.win = self.p1
                else: self.win = "Draw"
                p1shots = "\n".join(guesses[0])
                p2shots = "\n".join(guesses[1])
                if self.win == "Draw":
                    desc = self.lang.possibleDraw + "\n\n"
                    embed = discord.Embed(
                            title = self.lang.gameWasStopped,
                            colour = 0x70081d
                            )
                else:
                    self.lang.update(self.win.name)
                    desc = self.lang.gameEndedPossibleWinner + "\n\n"
                    embed = discord.Embed(
                            title = self.lang.gameWasStopped,
                            colour = 0x70081d
                            )

                self.lang.update(self.players[0].name)
                desc += self.lang.usersShots + p1shots + "\n\n"
                self.lang.update(self.players[1].name)
                desc += self.lang.usersShots + p2shots

                embed.description = desc

                del inGame[self.gameID]
                await self.msg.edit(content=None, embed=embed)
            except:
                embed = discord.Embed(
                        title = self.lang.gameWasStopped,
                        colour = 0x70081d
                        )
                del inGame[self.gameID]
                await self.msg.edit(content=None, embed=embed)
            await self.msg.clear_reactions()
        except:
            logger.exception(("Error in Battleship - Server: " + self.ctx.guild.name + " - Channel: " + self.ctx.channel.name), exc_info=True)
            del inGame[self.gameID]
            try:
                await self.msg.clear_reactions()
            except:
                pass
            try:
                try:
                    self.lang.update(self.players[0])
                    embed = discord.Embed(
                        title = self.lang.errorStopped,
                        description = self.lang.usersShots + "\n".join(guesses[0]) + "\n\n",
                        colour = 0x70081d
                        )
                    self.lang.update(self.players[1])
                    embed.description += self.lang.usersShots + "\n".join(guesses[1])
                    await self.msg.edit(content=None, embed=embed)
                except:
                    await self.msg.edit(content=self.lang.errorStopped, embed=embed)
            except:
                await self.ctx.send(self.lang.errorStopped)


# ------------------------------------------------------------------------------------------------------------  H A N G M A N  ----------------------------------------------------------------------------

    async def hangman(self): 
        global inGame
        global nextID
        global gamesPlayed

        blank = "<:blank:718734451785465977>"
        hungman = [('\u200B\n\u200B\n\u200B\n\u200B\n\u200B\n\u200B\n\u200B\n=========', 0x4d77f7, "\U0001F61B"),
                ('\u200B\n|\n|\n|\n|\n|\n|\n=========', 0x4db6f7, "\U0001F601"),
                ('+----+\n| {} |\n|\n|\n|\n|\n|\n========='.format(blank), 0x38c0c2, "\U0001F642"),
                ('+----+\n| {} |\n|{}\U0001F644\n|\n|\n|\n|\n========='.format(blank, blank), 0x21cc7f, "\U0001F644"),
                ('+----+\n| {} |\n|{}\U0001F620\n| {} |\n|\n|\n|\n========='.format(blank, blank, blank), 0xcfe339, "\U0001F620"),
                ('+----+\n| {} |\n|{}\U0001F97A\n|{}/|\n|\n|\n|\n========='.format(blank, blank, blank), 0xf0ca32, "\U0001F97A"),
                ('+----+\n| {} |\n|{}\U0001F62D\n|{}/|\\\n|\n|\n|\n========='.format(blank, blank, blank), 0xf57e16, "\U0001F62D"),
                ('+----+\n| {} |\n|{}\U0001F614\n|{}/|\\\n|{}/\n|\n|\n========='.format(blank, blank, blank, blank), 0xe3180e, "\U0001F614"),
                ('+----+\n| {} |\n|{}\U0001F635\n|{}/|\\\n|{}/\\\n|\n|\n========='.format(blank, blank, blank, blank), 0x360a0a, "\U0001F635")]
        
        def check_validity(string, word=None):
            if len(string) > 100: return False
            alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
            alpha_symbols = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " ", ",", ".", "\"", "'", "!", "?", "/", "-", ":", "(", ")", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
            letters_only = ""
            for c in string.lower():
                if c in alphabet: letters_only += c
                elif c not in alphabet and len(string) == 1: return False
            if 1 < len(letters_only) < 4: return False
            for char in string.lower():
                if not word and char not in alpha_symbols: return False
                elif word:
                    if char not in word and char not in alphabet: return False
            if word and len(string) > 1 and string.count(" ") != word.count(" "): return False
            return True

        try:
            if not self.mode.lower() in ["co-op", "coop", "co-operation", "cooperation", "co-operate", "cooperate", "comp", "competitive", "compete", "competition", self.lang.modes["comp"].lower(), self.lang.modes["co-op"].lower()] and len(self.players) > 1:
                self.msg = await self.ctx.send(self.lang.hmModeVote)
                await self.msg.add_reaction("🤼")
                await self.msg.add_reaction("🤝")
                self.votes = {"🤼":0, "🤝":0}
                global pending_reactions
                pending_reactions.append(self)
                for i in range(20):
                    await asyncio.sleep(0.5)
                    self.killcheck()
                pending_reactions.remove(self)
                await self.msg.clear_reactions()
                await self.msg.edit(content=self.lang.calculateResult)
                if self.votes["🤝"] > self.votes["🤼"]: self.mode = "co-op"
                elif self.votes["🤝"] < self.votes["🤼"]: self.mode = "comp"
                else:
                    await self.msg.edit(content=self.lang.voteDraw)
                    await asyncio.sleep(2)
                    self.mode = random.choice(["comp", "co-op"])
                mentions = ""
                for player in self.players:
                    mentions += player.mention + " "
                await self.msg.delete()
                self.lang.update(mode=self.mode)
                self.msg = await self.ctx.send(content=self.lang.gameModeSelected + "\n" + mentions)
                await asyncio.sleep(5)
            elif len(self.players) == 1:
                self.mode = "co-op"
                self.msg = await self.ctx.send(self.lang.hmOnePlayer)
                await asyncio.sleep(2)
            elif self.mode:
                mentions = ""
                if self.mode == "co-op":
                    mentions = ", ".join(player.mention for player in self.players)
                    self.msg = await self.ctx.send(mentions + self.lang.gameStarting)
                await asyncio.sleep(3)
        except Kill:
            await self.msg.clear_reactions()
            await self.msg.edit(content=None, embed=discord.Embed(title=self.lang.gameWasStopped, colour=0x70081d))
        except:
            await self.msg.clear_reactions()
            await self.msg.edit(content=None, embed=discord.Embed(title=self.lang.errorStopped, colour=0x752219))


        if self.mode.lower() in ["co-op", "coop", "co-operation", "cooperation", "co-operate", "cooperate"]:
            self.mode = "co-op"
            try:
                file = open('words.pkl', 'rb')
                word_list = pickle.load(file)
                word = random.choice(word_list)
                file.close()
                if word.count(" ") == 0: term = "word"
                else: term = "phrase"
                chars = []
                for i in range(len(word)):
                    if word[i].isalpha():
                        chars.append("\_")
                    elif word[i] == " ":
                        chars.append(blank)
                    else:
                        chars.append(word[i])
                incorrect = []
                wrong_count = 0
                attempt_count = 0
                turn = self.players[-1]
                while "".join(chars).replace(blank, " ") != word.upper() and wrong_count < len(hungman) - 1:
                    if self.players.index(turn) == len(self.players) - 1: turn = self.players[0]
                    else: turn = self.players[self.players.index(turn) + 1]
                    if len(incorrect) > 0: strincorrect = "**" + self.lang.incorrectGuesses + "**\n" + ", ".join(incorrect)
                    else: strincorrect = ""
                    self.lang.update(user=turn.name, number=30, wordPhrase=term)
                    embed = discord.Embed(
                            title = self.lang.takeAGuess,
                            description = hungman[wrong_count][0] + "\n\n" + " ".join(chars) + "\n\n" + strincorrect,
                            colour = hungman[wrong_count][1]
                        )
                    embed.set_footer(text=self.lang.hmHowTo)
                    await self.msg.edit(content=None, embed=embed)
                    guess = ""
                    mainTimeout = MessageTimeout(self, [turn], 30, self.ctx.channel)
                    userinput = await mainTimeout.run()
                    if userinput != "":
                        guess = userinput.content.lower()
                        valid = check_validity(guess, word)
                        while (not valid or guess in incorrect or guess.upper() in chars) and (time.perf_counter() - mainTimeout.timer.start_time) <= 25:
                            letters_only = ""
                            for c in guess:
                                if c in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]: letters_only += c
                            if guess in incorrect or guess.upper() in chars:
                                embed.title = self.lang.alreadyGuessed
                                await userinput.delete()
                            elif len(guess) == 1: embed.title = self.lang.invalidLetter
                            elif len(letters_only) < 4: embed.title = self.lang.hmTooShort
                            elif len(guess) > 100: embed.title = self.lang.hmTooLong
                            else: embed.title = self.lang.invalidWord
                            self.lang.update(wordPhrase=term, number=int(29-(time.perf_counter()-mainTimeout.timer.start_time)))
                            embed.set_footer(text=self.lang.hmHowTo)
                            await self.msg.edit(embed=embed)
                            guess = ""
                            timeout = MessageTimeout(self, [turn], 30-(time.perf_counter()-mainTimeout.timer.start_time), self.ctx.channel)
                            userinput = await timeout.run()
                            if userinput == "":
                                break
                            guess = userinput.content.lower()
                            valid = check_validity(guess, word)
                        if userinput: await userinput.delete()
                        if guess == word.lower():
                            attempt_count += 1
                            break
                        if guess != "":
                            count = 0
                            for i in range(len(word)):
                                if word[i].lower() == guess:
                                    chars[i] = guess.upper()
                                    count += 1
                            self.lang.update(wordPhrase=term, other=guess.upper(), other2=str(count))
                            if count == 0 and len(guess) == 1:
                                incorrect.append(guess)
                                wrong_count += 1
                                embed = discord.Embed(
                                        title = self.lang.letterNotInWord,
                                        description = hungman[wrong_count][0] + "\n\n" + " ".join(chars) + "\n\n" + strincorrect,
                                        colour = hungman[wrong_count][1]
                                    )
                            elif count == 0:
                                incorrect.append(guess)
                                wrong_count += 1
                                embed = discord.Embed(
                                        title = self.lang.incorrectWord,
                                        description = hungman[wrong_count][0] + "\n\n" + " ".join(chars) + "\n\n" + strincorrect,
                                        colour = hungman[wrong_count][1]
                                    )
                            elif count == 1:
                                embed.title = self.lang.letterAppearsOnce
                                embed.description = hungman[wrong_count][0] + "\n\n" + " ".join(chars) + "\n\n" + strincorrect
                            elif count == 2:
                                embed.title = self.lang.letterAppearsTwice
                                embed.description = hungman[wrong_count][0] + "\n\n" + " ".join(chars) + "\n\n" + strincorrect
                            else:
                                embed.title = self.lang.letterAppears
                                embed.description = hungman[wrong_count][0] + "\n\n" + " ".join(chars) + "\n\n" + strincorrect
                            await self.msg.edit(embed=embed)
                            await asyncio.sleep(2)
                        else:
                            embed.title = self.lang.hmTimeout
                            wrong_count += 1
                    else:
                        embed.title = self.lang.hmTimeout
                        wrong_count += 1
                    attempt_count += 1
                if wrong_count == len(hungman) - 1:
                    embed.title = self.lang.failedToGuess
                    embed.set_footer(text=self.lang.wordWas + word)
                    await self.msg.edit(embed=embed)
                    self.win = []
                if "".join(chars).replace(blank, " ") == word.upper() or guess == word.lower():
                    chars = []
                    for i in range(len(word)):
                        if word[i] == " ": chars.append(blank)
                        else: chars.append(word[i].upper())
                    embed.title = self.lang.youWin
                    embed.description = hungman[wrong_count][0] + "\n\n" + " ".join(chars) + "\n\n" + strincorrect
                    embed.colour = 0x34c23b
                    self.lang.update(wordPhrase=term, other=str(attempt_count), other2=str((len(hungman) - 1 - wrong_count)))
                    embed.set_footer(text=self.lang.coOpWinStats)
                    await self.msg.edit(embed=embed)
                    self.win = self.players
            
                sendExtra = True
                async for message in self.ctx.channel.history(limit=5):
                    if self.msg.id == message.id:
                        sendExtra = False
                        break
                if sendExtra and wrong_count < len(hungman) - 1:
                    if len(self.players) == 1:
                        self.lang.update(user=self.players[0].name, wordPhrase=term, other=word, other2=str(attempt_count))
                        await self.ctx.send(self.lang.hmCoOpEnd)
                    else:
                        self.lang.update(user=[person.name for person in self.players], wordPhrase=term, other=word, other2=str(attempt_count))
                        await self.ctx.send(self.lang.hmCoOpEnd)

                self.update_stats()
            except Kill:
                killing.remove(self.gameID)
                embed.title = self.lang.gameWasStopped
                embed.colour = 0x70081d
                embed.set_footer(text=self.lang.wordWas + word)
                await self.msg.edit(embed=embed)
                del inGame[self.gameID]
                sentPromo = False
                for p in self.players:
                    if p.id not in gamesPlayed: gamesPlayed[p.id] = 0
                    gamesPlayed[p.id] += 1
                    if gamesPlayed[p.id] % 8 == 0 and not sentPromo:
                        await sendPromo(self.ctx)
                        sentPromo = True
            except:
                logger.exception(("Error in Hangman (Co-op) - Server: " + self.ctx.guild.name + " - Channel: " + self.ctx.channel.name), exc_info=True)
                del inGame[self.gameID]
                embed.title = self.lang.errorStopped
                embed.colour = 0x752219
                embed.set_footer(text=self.lang.wordWas + word)
                try: await self.msg.edit(embed=embed)
                except:
                    try: await self.msg.edit(content=self.lang.errorStopped, embed=embed)
                    except: await self.ctx.send(content=self.lang.errorStopped)
        else:
            self.mode = "comp"
            letter_scores = {
                **dict.fromkeys(['e', 'a', 'i', 'o', 'n', 'r', 't', 'l', 's', 'u'], 10), 
                **dict.fromkeys(['d', 'g'], 20),
                **dict.fromkeys(['b', 'c', 'm', 'p'], 30),
                **dict.fromkeys(['f', 'h', 'v', 'w', 'y'], 40),
                **dict.fromkeys(['k'], 50),
                **dict.fromkeys(['j', 'x'], 80),
                **dict.fromkeys(['q', 'z'], 100),
                }
            class Setup:
                def __init__(self, parent, user):
                    self.user = user
                    self.parent = parent
                
                async def setup(self):
                    try:
                        if len(self.parent.unavailable) > 0:
                            return
                        try:
                            await self.user.send(self.parent.lang.hmSetup)
                        except:
                            self.parent.lang.update(self.user.mention)
                            await self.parent.msg.edit(content=self.parent.lang.needToDM)
                            self.parent.unavailable.append(self.user.mention)
                            return
                        await asyncio.sleep(0.1)
                        if len(self.parent.unavailable) > 0:
                            await self.user.send(self.parent.lang.hmSetupCancel)
                            return
                        self.mainTimeout = MessageTimeout(self, [self.user], 60, self.user.dm_channel)
                        self.message = await self.mainTimeout.run()
                        if self.message == "":
                            await self.user.send(self.parent.lang.hmSetupTimeout)
                            file = open('words.pkl', 'rb')
                            word_list = pickle.load(file)
                            self.word = random.choice(word_list)
                            file.close()
                            return
                        else:
                            valid = check_validity(self.message.content)
                            while not valid and (time.perf_counter() - self.mainTimeout.timer.start_time) <= 57:
                                self.word = self.message.content
                                to_send = ""
                                if self.word.count(" ") == 0: self.parent.lang.update(wordPhrase="word")
                                else: self.parent.lang.update(wordPhrase="phrase")
                                letters_only = ""
                                to_send = ""
                                for c in self.word.lower():
                                    if c in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]: letters_only += c
                                    if c not in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " ", ",", ".", "\"", "'", "!", "?", "/", "-", ":", "(", ")", "$", "%", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]: to_send = self.parent.lang.hmSetupInvalid
                                if not to_send:
                                    if len(letters_only) < 4: to_send = self.parent.lang.hmTooShort
                                    elif len(self.word) > 100: to_send = self.parent.lang.hmTooLong
                                    else: to_send = self.parent.lang.hmSetupInvalid
                                await self.user.send(to_send)
                                self.timeout = MessageTimeout(self, [self.user], 60-(time.perf_counter() - self.mainTimeout.timer.start_time), self.user.dm_channel)
                                self.message = await self.timeout.run()
                                if self.message == "":
                                    await self.user.send(self.parent.lang.hmSetupTimeout)
                                    file = open('words.pkl', 'rb')
                                    word_list = pickle.load(file)
                                    self.word = random.choice(word_list)
                                    file.close()
                                    return
                                valid = check_validity(self.message.content)
                            self.word = self.message.content
                            class Confirm():
                                def __init__(self):
                                    self.content = ""
                            self.confirm = Confirm()
                            self.start_time = time.perf_counter()
                            while self.confirm.content.lower() != self.parent.lang.yes and (time.perf_counter() - self.start_time) <= 15:
                                self.parent.lang.update(other=self.word)
                                await self.user.send(self.parent.lang.hmSetupConfirm)
                                self.timeout = MessageTimeout(self, [self.user], 20-(time.perf_counter() - self.start_time), self.user.dm_channel)
                                self.confirm = await self.timeout.run()
                                if self.confirm == "":
                                    await self.user.send(self.parent.lang.hmSetupConfirmTimeout)
                                    return
                                elif self.confirm.content.lower() != self.parent.lang.yes:
                                    self.word = self.confirm.content
                            await self.user.send(self.parent.lang.hmSetupComplete)
                    except Kill:
                        self.word = "^($@) cancelled"
                        await self.user.send(self.parent.lang.hmSetupCancel)
                    except:
                        logger.exception(("Error in Hangman Setup - Server: " + self.parent.ctx.guild.name + " - Channel: " + self.parent.ctx.channel.name), exc_info=True)
                        self.word = "^($@) error"
                        await self.user.send(self.parent.lang.hmSetupCancel)

            
            try:
                self.num_players = len(self.players)
                self.all_players = list(self.players)
                try: await self.msg.edit(content=self.lang.waitForWords)
                except: self.msg = await self.ctx.send(self.lang.waitForWords)
                self.unavailable = []
                self.objs = [Setup(self, user) for user in self.players]
                self.setups = [s.setup() for s in self.objs]
                await asyncio.gather(*self.setups)
                if len(self.unavailable) > 0:
                    self.lang.update(", ".join(self.unavailable))
                    await self.msg.edit(content=self.lang.needToDM)
                    del inGame[self.gameID]
                    return
                
                self.words = [s.word for s in self.objs]
                if "^($@) cancelled" in self.words: raise Kill
                if "^($@) error" in self.words: raise Exception("Error in Setup")
                self.moved = self.words.pop(0)
                self.words.append(self.moved)
                await self.msg.delete()
                self.msg = await self.ctx.send(self.lang.hmAllSetupsComplete + "\n" + " ".join(player.mention for player in self.players))
                await asyncio.sleep(5)
                for word in self.words:
                    if word.count(" ") == 0: term = "word"
                    else: term = "phrase"
                    chars = []
                    for i in range(len(word)):
                        if word[i].isalpha():
                            chars.append("\_")
                        elif word[i] == " ":
                            chars.append(blank)
                        else:
                            chars.append(word[i])
                    self.words[self.words.index(word)] = (word, term, chars)
                self.info = [[player, [], 0, 0, 0] for player in self.players]
                self.finished = []
                while len(self.finished) < self.num_players:
                    for index in range(self.num_players):
                        if self.all_players[index] in self.players:
                            turn = self.all_players[index]
                            incorrect = self.info[index][1]
                            wrong_count = self.info[index][2]
                            attempt_count = self.info[index][3]
                            word = self.words[index][0]
                            term = self.words[index][1]
                            chars = self.words[index][2]

                            if len(incorrect) > 0: strincorrect = "**" + self.lang.incorrectGuesses + "**\n" + ", ".join(incorrect)
                            else: strincorrect = ""
                            self.lang.update(user=turn.name, number=30, wordPhrase=term)
                            embed = discord.Embed(
                                    title = self.lang.yourTurn,
                                    description = hungman[wrong_count][0] + "\n\n" + " ".join(chars) + "\n\n" + strincorrect,
                                    colour = hungman[wrong_count][1]
                                )
                            embed.set_footer(text=self.lang.hmHowTo)
                            await self.msg.edit(content=None, embed=embed)
                            guess = ""
                            mainTimeout = MessageTimeout(self, [turn], 30, self.ctx.channel)
                            userinput = await mainTimeout.run()
                            if userinput != "":
                                guess = userinput.content.lower()
                                valid = check_validity(guess, word)
                                while (not valid or guess in incorrect or guess.upper() in chars) and (time.perf_counter() - mainTimeout.timer.start_time) <= 27:
                                    if guess.count(" ") == 0: self.lang.update(wordPhrase="word")
                                    else: self.lang.update(wordPhrase="phrase")
                                    letters_only = ""
                                    for c in guess:
                                        if c in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]: letters_only += c
                                    if guess in incorrect or guess.upper() in chars:
                                        embed.title = self.lang.alreadyGuessed
                                        await userinput.delete()
                                    elif len(guess) == 1: embed.title = self.lang.invalidLetter
                                    elif len(letters_only) < 4: embed.title = self.lang.hmTooShort
                                    elif len(guess) > 100: embed.title = self.lang.hmTooLong
                                    else: embed.title = self.lang.invalidWord
                                    self.lang.update(wordPhrase=term, number=int(29-(time.perf_counter()-mainTimeout.timer.start_time)))
                                    embed.set_footer(text=self.lang.hmHowTo)
                                    await self.msg.edit(embed=embed)
                                    guess = ""
                                    timeout = MessageTimeout(self, [turn], 30-(time.perf_counter()-mainTimeout.timer.start_time), self.ctx.channel)
                                    userinput = await timeout.run()
                                    if userinput == "":
                                        break
                                    guess = userinput.content.lower()
                                    valid = check_validity(guess, word)
                                try: await userinput.delete()
                                except:
                                    embed.title = self.lang.hmTimeout
                                    wrong_count += 1
                                    await self.msg.edit(embed=embed)
                                    await asyncio.sleep(1.5)
                                if guess == word.lower():
                                    chars = []
                                    for i in range(len(word)):
                                        if word[i] == " ": chars.append(blank)
                                        else: chars.append(word[i].upper())
                                    embed.title = self.lang.wordFinished
                                    embed.description = hungman[wrong_count][0] + "\n\n" + " ".join(chars) + "\n\n" + strincorrect
                                    embed.colour = 0x34c23b
                                elif guess != "":
                                    count = 0
                                    for i in range(len(word)):
                                        if word[i].lower() == guess:
                                            chars[i] = guess.upper()
                                            count += 1
                                    self.lang.update(wordPhrase=term, other=guess.upper())
                                    if count == 0 and len(guess) == 1:
                                        incorrect.append(guess)
                                        wrong_count += 1
                                        embed = discord.Embed(
                                                title = self.lang.letterNotInWord,
                                                colour = hungman[wrong_count][1]
                                            )
                                    elif count == 0:
                                        incorrect.append(guess)
                                        wrong_count += 1
                                        embed = discord.Embed(
                                                title = self.lang.incorrectWord,
                                                colour = hungman[wrong_count][1]
                                            )
                                    elif count == 1:
                                        embed.title = self.lang.letterAppearsOnce
                                    elif count == 2:
                                        embed.title = self.lang.letterAppearsTwice
                                    else:
                                        self.lang.update(wordPhrase=term, other=guess.upper(), other2=count)
                                        embed.title = self.lang.letterAppears
                                    embed.description = hungman[wrong_count][0] + "\n\n" + " ".join(chars) + "\n\n" + strincorrect
                                    await self.msg.edit(embed=embed)
                                    await asyncio.sleep(2)
                                else:
                                    embed.title = self.lang.hmTimeout
                                    wrong_count += 1
                                    await self.msg.edit(embed=embed)
                                    await asyncio.sleep(1.5)
                            else:
                                embed.title = self.lang.hmTimeout
                                wrong_count += 1
                                await self.msg.edit(embed=embed)
                                await asyncio.sleep(1.5)

                            attempt_count += 1
                            self.info[index] = [turn, incorrect, wrong_count, attempt_count, 0]
                            self.words[index] = [word, term, chars]

                            wordSoFar = []
                            for i in chars:
                                wordSoFar.append(i.replace(blank, " "))
                            if "".join(wordSoFar).lower() == word.lower() or guess.lower() == word.lower():
                                chars = []
                                for i in range(len(word)):
                                    if word[i] == " ": chars.append(blank)
                                    else: chars.append(word[i].upper())
                                embed.title = self.lang.wordFinished
                                embed.description = hungman[wrong_count][0] + "\n\n" + " ".join(chars) + "\n\n" + strincorrect
                                embed.colour = 0x34c23b
                                self.lang.update(wordPhrase=term, other=attempt_count, other2=(len(hungman) - 1 - wrong_count))
                                embed.set_footer(text=self.lang.personFinished)
                                await self.msg.edit(embed=embed)
                                self.finished.append(turn)
                                self.players.remove(turn)
                                await asyncio.sleep(5)
                            
                            elif wrong_count == len(hungman) - 1:
                                self.lang.update(wordPhrase=term)
                                embed.title = self.lang.hmeliminated
                                embed.set_footer(text=self.lang.wordWas + word)
                                await self.msg.edit(embed=embed)
                                self.finished.append(turn)
                                self.players.remove(turn)
                                await asyncio.sleep(5)

                # End of game
                await self.msg.edit(content=self.lang.everyoneFinished, embed=None)
                index = 0
                while index < len(self.all_players):
                    chars = list(self.words[index][2])
                    word = str(self.words[index][0])
                    incorrect = list(self.info[index][1])
                    attempts = int(self.info[index][3])
                    score = 0
                    for char in chars:
                        try: score += letter_scores[char.lower()]
                        except: pass
                    for c in chars:
                        if c.lower() == "_":
                            try: score -= letter_scores[word[chars.index(c)].lower()]
                            except: pass
                    for x in incorrect:
                        if len(x) == 1:
                            try: score -= letter_scores[x.lower()]
                            except: pass
                        else: score -= 150
                    if attempts < len(Counter(word.lower())):
                        score += (len(Counter(word.lower())) - attempts) * 20
                    self.info[index][4] = int(score)
                    index += 1

                self.info, self.words = zip(*sorted(zip(self.info, self.words), key=lambda x: x[0][4], reverse=True))
                
                embed = discord.Embed(colour = 0x8456e8)
                self.lang.update(user=self.info[0][0].name)
                embed.set_author(name=self.lang.playerWon)
                self.win = []
                for i in self.info:
                    word = self.words[self.info.index(i)][0]
                    if word.count(" ") > 0: self.lang.update(wordPhrase="phrase")
                    else: self.lang.update(wordPhrase="word")
                    if i[4] == self.info[0][4]:
                        emoji = "👑"
                        self.win.append(i[0])
                    elif i[2] == 8: emoji = "💀"
                    else: emoji = ""
                    player = i[0].name
                    embed.add_field(name="**" + player + "** " + emoji,
                        value=self.lang.wordPhrase.capitalize() + ": " + word + "\n" + self.lang.totalAttempts + str(i[3]) + "\n" + self.lang.correctAttempts + str(i[3]-i[2]) + "\n" + self.lang.incorrectAttempts + str(i[2]) + "\n" + "Score: " + str(i[4]))
                await self.msg.edit(content=None, embed=embed)
                self.update_stats()
            except Kill:
                killing.remove(self.gameID)
                try:
                    index = 0
                    while index < len(self.all_players):
                        chars = list(self.words[index][2])
                        word = str(self.words[index][0])
                        incorrect = list(self.info[index][1])
                        attempts = int(self.info[index][3])
                        score = 0
                        for char in chars:
                            try: score += letter_scores[char.lower()]
                            except: pass
                        for c in chars:
                            if c.lower() == "_":
                                try: score -= letter_scores[word[chars.index(c)].lower()]
                                except: pass
                        for x in incorrect:
                            if len(x) == 1:
                                try: score -= letter_scores[x.lower()]
                                except: pass
                            else: score -= 150
                        if attempts < len(Counter(word.lower())):
                            score += (len(Counter(word.lower())) - attempts) * 20
                        self.info[index][4] = int(score)
                        index += 1

                    self.info, self.words = zip(*sorted(zip(self.info, self.words), key=lambda x: x[0][4], reverse=True))
                    embed = discord.Embed(colour=0x752219)
                    embed.set_author(name=self.lang.gameWasStopped)
                    for i in self.info:
                        showScore = True
                        word = self.words[self.info.index(i)]
                        if word[0].count(" ") > 0: self.lang.update(wordPhrase="phrase")
                        else: self.lang.update(wordPhrase="word")
                        if i[2] == 8: emoji = "💀"
                        else:
                            emoji = ""
                            for l in word[2]:
                                if l == "\\_": emoji = "(DNF)"
                        player = i[0].name
                        embed.add_field(name="**" + player + "** " + emoji,
                            value=(self.lang.wordPhrase.capitalize() + ": "
                            + word[0].upper() + "\n"
                            + self.lang.totalAttempts + str(i[3]) + "\n" +
                            self.lang.correctAttempts + str(i[3]-i[2]) + "\n" +
                            self.lang.incorrectAttempts + str(i[2])))
                        if emoji != "(DNF)": embed.fields[-1].value += "\nScore: " + str(i[4])
                        else: embed.fields[-1].value += "\n" + self.lang.scoreUnavailable
                    await self.msg.edit(content=None, embed=embed)
                    sentPromo = False
                    for p in self.all_players:
                        if p.id not in gamesPlayed: gamesPlayed[p.id] = 0
                        gamesPlayed[p.id] += 1
                        if gamesPlayed[p.id] % 8 == 0:
                            try:
                                await sendPromo(self.ctx)
                                sentPromo = True
                            except: pass
                except:
                    await self.msg.edit(content=None, embed=discord.Embed(title=self.lang.gameWasStopped, colour=0x70081d))
                del inGame[self.gameID]
            except Exception as e:
                if e != "Error in Setup": logger.exception(("Error in Hangman (Competitive) - Server: " + self.ctx.guild.name + " - Channel: " + self.ctx.channel.name), exc_info=True)
                del inGame[self.gameID]
                try:
                    i = 0
                    while i < len(self.all_players):
                        chars = list(self.words[i][2])
                        word = str(self.words[i][0])
                        incorrect = list(self.info[i][1])
                        attempts = int(self.info[i][3])
                        score = 0
                        for char in chars:
                            try: score += letter_scores[char.lower()]
                            except: pass
                        for c in chars:
                            if c.lower() == "_":
                                try: score -= letter_scores[word[chars.index(c)].lower()]
                                except: pass
                        for x in incorrect:
                            if len(x) == 1:
                                try: score -= letter_scores[x.lower()]
                                except: pass
                            else: score -= 150
                        if attempts < len(Counter(word.lower())):
                            score += (len(Counter(word.lower())) - attempts) * 20
                        self.info[i][4] = int(score)
                        i += 1

                    self.info, self.words = zip(*sorted(zip(self.info, self.words), key=lambda x: x[0][4], reverse=True))
                    
                    embed = discord.Embed(colour=0x752219)
                    embed.set_author(name=self.lang.errorStopped)
                    for i in self.info:
                        showScore = True
                        word = self.words[self.info.index(i)]
                        if word[0].count(" ") > 0: self.lang.update(wordPhrase="phrase")
                        else: self.lang.update(wordPhrase="word")
                        if i[2] == 8: emoji = "💀"
                        elif "_" in word[2]: emoji = "(DNF)"
                        else: emoji = ""
                        player = i[0].name
                        embed.add_field(name="**" + player + "** " + emoji,
                            value=self.lang.wordPhrase.capitalize() + ": " + word[0].upper + "\n" + self.lang.totalAttempts + str(i[3]) + "\n" + self.lang.correctAttempts + str(i[3]-i[2]) + "\n" + self.lang.incorrectAttempts + str(i[2]))
                        if emoji != "(DNF)": embed.fields[-1].value += "\nScore: " + str(i[4])
                        else: embed.fields[-1].value += "\n" + self.lang.scoreUnavailable
                    await self.msg.edit(content=None, embed=embed)
                except: 
                    try:
                        await self.msg.edit(content=None, embed=discord.Embed(title=self.lang.errorStopped, colour=0x752219))
                    except: await self.ctx.send(content=None, embed=discord.Embed(title=self.lang.errorStopped, colour=0x752219))






                



################################################################################################   COMMANDS   ############################################################################


@bot.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["c4", "connectfour", "conecta4", "connetti4", "puissance4", "четыревряд", "czwórki"]), ["连接4", "CONNECT4"]]))
async def connect4(ctx, *, player2:discord.Member=None):
    game = Game(ctx, "Connect 4", player2)
    await game.pregame()
    del game

@bot.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["mc4", "megaconnectfour", "megaconecta4", "megaconnetti4", "mégapuissance4", "мегачетыревряд", "megaczwórki"]), ["巨型连接4", "MEGACONNECT4"]]))
async def megaconnect4(ctx):
    game = Game(ctx, "Mega Connect 4", limitRange=range(3,4), premRange=range(3,8))
    await game.mc4pregame()
    del game

@bot.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["xo", "ttt", "noughtsandcrosses", "nc", "tresenlínea", "tris", "morpion", "крестики-нолики", "kółkoikrzyżyk"]), ["井字游戏", "TICTACTOE"]]))
async def tictactoe(ctx, *, player2:discord.Member=None):
    game = Game(ctx, "Tic Tac Toe", player2)
    await game.pregame()
    del game

@bot.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["mm", "codecrack", "codecracker", "cc", "mentemaestra", "быкиикоровы"]), ["策划者", "MASTERMIND"]]))
async def mastermind(ctx, player2:discord.Member=None, mode="colour"):
    game = Game(ctx, "MasterMind", player2, mode)
    await game.pregame()
    del game

@bot.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["b", "bs", "seabattle", "sb", "batallanaval", "battaglianavale", "bataillenavale", "морскойбой", "statki"]), ["战舰", "BATTLESHIP"]]))
async def battleship(ctx, player2:discord.Member=None):
    game = Game(ctx, "Battleship", player2)
    await game.pregame()
    del game

@bot.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["hm", "elahorcado", "impiccato", "man子手", "виселица", "wisielec"]), ["HANGMAN"]]))
async def hangman(ctx, mode=""):
    global inGame
    game = Game(ctx, "Hangman", "", mode, range(1, 4), range(1, 16))
    await game.unlimitedpregame()
    del game

@bot.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["statistics", "estadísticas", "statistiche", "statistiques", "статистика", "statystyki"]), ["统计", "STATS"]]))
async def stats(ctx, *, targetUser=""):
    global windata
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id])
    else: lang = Language("English")

    user = ""
    if targetUser != "":
        for person in bot.users:
            if "!" in person.mention:
                mention = ""
                for char in range(len(person.mention)):
                    if char != 2:
                        mention += person.mention[char]
            else:
                mention = person.mention
            if targetUser[0] == "<" and targetUser[1] == "@" and targetUser[2] == "!":
                usermention = ""
                for char in range(len(targetUser)):
                    if char != 2:
                        usermention += targetUser[char]
            else:
                usermention = targetUser
            if usermention == mention or targetUser.lower() == person.name.lower() or targetUser.lower == str(person).lower() or targetUser == str(person.id):
                user = person
                break
        if user == "":
            for person in ctx.guild.members:
                if "!" in person.mention:
                    mention = ""
                    for char in range(len(person.mention)):
                        if char != 2:
                            mention += person.mention[char]
                else:
                    mention = person.mention
                if targetUser[0] == "<" and targetUser[1] == "@" and targetUser[2] == "!":
                    usermention = ""
                    for char in range(len(targetUser)):
                        if char != 2:
                            usermention += targetUser[char]
                else:
                    usermention = targetUser
                if usermention == mention or targetUser.lower() == person.name.lower() or targetUser.lower() == person.display_name.lower() or targetUser.lower == str(person).lower() or targetUser == str(person.id):
                    user = person
                    break
        if user == "":
            await ctx.send(lang.cantFindPerson)
            return
    else:
        user = ctx.author
    hasData = False
    for data in windata:
        if data == user.id:
            hasData = True
            userData = windata[user.id]
            break
    
    lang.update(user.name)
    if not hasData:
        if user == ctx.author:
            await ctx.send(lang.youHaveNoStats)
        else:
            await ctx.send(lang.theyHaveNoStats)
        return

    if user.id in premium:
        if type(premium[user.id][1]) == int: colour = premium[user.id][1]
        else: colour = 0x4014de
    else: colour = 0x4014de

    embed = discord.Embed(
            title = lang.personsStats,
            colour = colour
        )
    def getValue(game):
        value = ""
        if game not in ["Hangman (Competitive)", "Hangman (Co-op)"]:
            try: value += "**" + lang.wins + ":** " + str(userData[game]["W"]) + "\n"
            except: pass
            try: value += "**" + lang.losses + ":** " + str(userData[game]["P"] - userData[game]["W"]) + "\n"
            except: pass
            try: value += "**" + lang.draws + ":** " + str(userData[game]["D"]) + "\n"
            except: pass
            try: value += "**" + lang.played + ":** " + str(userData[game]["P"] + userData[game]["D"]) + "\n"
            except: pass
            try: value += "**" + lang.winRate + ":** " + str(round((userData[game]["W"]/userData[game]["P"])*100, 2)) + "%"
            except: pass
        else:
            if game == "Hangman (Co-op)": mode = "Co-op"
            elif game == "Hangman (Competitive)": mode = "Comp"
            try: value += "**" + lang.wins + ":** " + str(userData["Hangman"][mode]["W"]) + "\n"
            except: pass
            try: value += "**" + lang.losses + ":** " + str(userData["Hangman"][mode]["P"] - userData["Hangman"][mode]["W"]) + "\n"
            except: pass
            try: value += "**" + lang.played + ":** " + str(userData["Hangman"][mode]["P"]) + "\n"
            except: pass
            try: value += "**" + lang.winRate + ":** " + str(round((userData["Hangman"][mode]["W"]/userData["Hangman"][mode]["P"])*100,2)) + "%"
            except: pass
        return value
    embed.add_field(
            name=lang.total,
            value=getValue("T"),
            inline=False)
    for game in ["Connect 4", "Mega Connect 4", "MasterMind", "Tic Tac Toe", "Battleship"]:
        if userData[game]["P"] > 0 or userData[game]["D"] > 0:
            embed.add_field(
                    name="**" + lang.games[game] + "**",
                    value=getValue(game),
                    inline=True)
    if userData["Hangman"]["Comp"]["P"] > 0:
        embed.add_field(
            name="**" + lang.hm + " (" + lang.modes["comp"].capitalize() + ")**",
            value=getValue("Hangman (Competitive)"),
            inline=True)
    if userData["Hangman"]["Co-op"]["P"] > 0:
        embed.add_field(
            name="**" + lang.hm + " (" + lang.modes["co-op"].capitalize() + ")**",
            value=getValue("Hangman (Co-op)"),
            inline=True)
    await ctx.send(content=None, embed=embed)


async def makeLeaderboard(ctx, state, game, calculateRate, mode, lang):
    global windata
    lboard = []
    if state == "This Server":
        for user in windata:
            userData = windata[user]
            if game != "Hangman":
                if ctx.guild.get_member(user) and userData[game]["P"] != 0:
                    name = str(ctx.guild.get_member(user))
                    if calculateRate:
                        if userData[game]["P"] > 5:
                            lboard.append((name, (userData[game]["W"] / userData[game]["P"])*100))
                    else:
                        lboard.append((name, userData[game]["W"]))
            else:
                if ctx.guild.get_member(user) and userData["Hangman"][mode]["P"] != 0:
                    name = str(ctx.guild.get_member(user))
                    if calculateRate:
                        if userData["Hangman"][mode]["P"] > 5:
                            lboard.append((name, (userData["Hangman"][mode]["W"] / userData["Hangman"][mode]["P"])*100))
                    else:
                        lboard.append((name, userData["Hangman"][mode]["W"]))

    else:
        mode = mode.capitalize()
        for user in windata:
            userData = windata[user]
            if game != "Hangman":
                if bot.get_user(user) and userData[game]["P"] > 0:
                    name = str(bot.get_user(user))
                    if calculateRate:
                        if userData[game]["P"] > 5:
                            lboard.append((name, (userData[game]["W"] / userData[game]["P"])*100))
                    else:
                        lboard.append((name, userData[game]["W"]))
            else:
                if bot.get_user(user) and userData["Hangman"][mode]["P"] > 0:
                    name = str(bot.get_user(user))
                    if calculateRate:
                        if userData["Hangman"][mode]["P"] > 5:
                            lboard.append((name, (userData["Hangman"][mode]["W"] / userData["Hangman"][mode]["P"])*100))
                    else:
                        lboard.append((name, userData["Hangman"][mode]["W"]))
    lboard = sorted(lboard, key=itemgetter(1))
    lboard.reverse()
    placing = None
    for user in lboard:
        if user[0] == ctx.author.name:
            if lboard.index(user) >= 10:
                placing = lboard.index(user) + 1
            break
    popval = 10
    while len(lboard) > popval:
        if placing and lboard[5][0] == ctx.author.name:
            popval = 11
        lboard.pop(popval)
    if game == "T": game = lang.allGames
    else: game = lang.games[game]
    if game != lang.hm:
        embed = discord.Embed(
                title = lang.lb,
                description = lang.lbstates[state] + " - " + game,
                colour = 0x19d1e6
            )
    else:
        mode = mode.lower()
        embed = discord.Embed(
                title = lang.lb,
                description = lang.lbstates[state] + " - " + game + " - " + lang.modes[mode].capitalize(),
                colour = 0x19d1e6
            )

    string = ""
    def numberchange(i):
        if i + 1 == 1:
            number = ":first_place:"
        elif i + 1 == 2:
            number = ":second_place:"
        elif i + 1 == 3:
            number = ":third_place:"
        else:
            number = lang.placings[i]
        return number
    if len(lboard) > 0:
        if placing:
            for i in range(len(lboard) - 1):
                number = numberchange(i)
                if calculateRate:
                    string += (number) + " - " + lboard[i][0] + " - " + str(lboard[i][1]) + "% \n"
                else:
                    string += (number) + " - " + lboard[i][0] + " - " + str(lboard[i][1]) + "\n"
            embed.add_field(name="\u200b", value=string, inline=False)
            if calculateRate:
                embed.add_field(name="\u200b", value=("**" + (str(placing)) + " - " + lboard[5][0] + " - " + str(round(lboard[5][1], 2)) + "%**"), inline=False)
            else:
                embed.add_field(name="\u200b", value=("**" + (str(placing)) + " - " + lboard[5][0] + " - " + str(lboard[5][1]) + "**"), inline=False)
        else:
            for i in range(len(lboard)):
                number = numberchange(i)
                if lboard[i][0] == str(ctx.author):
                    if calculateRate:
                        string += "**" + str(number) + " - " + lboard[i][0] + " - " + str(round(lboard[i][1], 2)) + "%** \n"
                    else:
                        string += "**" + str(number) + " - " + lboard[i][0] + " - " + str(lboard[i][1]) + "** \n"
                else:
                    if calculateRate:
                        string += str(number) + " - " + lboard[i][0] + " - " + str(round(lboard[i][1], 2)) + "% \n"
                    else:
                        string += str(number) + " - " + lboard[i][0] + " - " + str(lboard[i][1]) + "\n"
            embed.add_field(name="\u200b", value=string, inline=False)
    else:
        embed.add_field(name=lang.emptylb, value=lang.emptylb2, inline=False)
    await ctx.send(content=None, embed=embed)

@bot.group(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["lb", "clasificación", "classifica", "classement", "доскалидеров", "tabelawyników"]), ["排行榜", "LEADERBOARD"]]))
async def leaderboard(ctx, arg1="", arg2="", arg3="", arg4=""):
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id])
    else: lang = Language("English")
    arg1 = arg1.lower()
    arg2 = arg2.lower()
    arg3 = arg3.lower()
    arg4 = arg4.lower()
    mode = ""
    if arg1 == "":
        local_global = "All Servers"
        game = "T"
        index = 1
        winrate = False
    aliases = ["server", "l", "s", "local", lang.local]
    if arg1 in aliases or arg2 in aliases or arg3 in aliases or arg4 in aliases: local_global = "This Server"
    else: local_global = "All Servers"
    aliases = ["rate", "winrate", "percent", "percentage"]
    if arg1 in aliases or arg2 in aliases or arg3 in aliases or arg4 in aliases: winrate = True
    else: winrate = False
    c4aliases = ["c4", "connect4", "connectfour", lang.c4.lower().replace(" ", "")]
    mc4aliases = ["mc4", "megaconnect4", "megaconnectfour", lang.mc4.lower().replace(" ", "")]
    tttaliases = ["ttt", "tictactoe", "xo", lang.ttt.lower().replace(" ", "")]
    mmaliases = ["mastermind", "mm", "codebreaker", "cb", lang.mm.lower().replace(" ", "")]
    battleshipaliases = ["b", "battleship", "bs", "seabattle", "sb", lang.bs.lower().replace(" ", "")]
    hmaliases = ["hangman", "hm", lang.hm.lower().replace(" ", "")]
    if arg1 in c4aliases or arg2 in c4aliases or arg3 in c4aliases: game = "Connect 4"
    elif arg1 in mc4aliases or arg2 in mc4aliases or arg3 in mc4aliases: game = "Mega Connect 4"
    elif arg1 in tttaliases or arg2 in tttaliases or arg3 in tttaliases: game = "Tic Tac Toe"
    elif arg1 in mmaliases or arg2 in mmaliases or arg3 in mmaliases: game = "MasterMind"
    elif arg1 in battleshipaliases or arg2 in battleshipaliases or arg3 in battleshipaliases: game = "Battleship"
    elif arg1 in hmaliases or arg2 in hmaliases or arg3 in hmaliases:
        game = "Hangman"
        coopaliases = ["co-op", "coop", "co-operation", "cooperation", "co-operate", "cooperate", lang.modes["co-op"].lower().replace(" ", "")]
        if arg1 in coopaliases or arg2 in coopaliases or arg3 in coopaliases or arg4 in coopaliases: mode = "Co-op"
        else: mode = "Comp"
    else: game = "T"
    await makeLeaderboard(ctx, local_global, game, winrate, mode, lang)

@bot.group(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["h", "help", "ayuda", "aiuto", "aide", "помощь", "pomoc"]), ["帮助"]])) # -------------------------------------------------------------------------------------------------   H E L P  C O M M A N D   ------------------------------------------------------------------------------------
async def helpcommand(ctx):
    if ctx.guild.id in prefixes:
        prefix = prefixes[ctx.guild.id]
    else:
        prefix = default_prefix
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id], prefix=prefix)
    else: lang = Language("English", prefix=str(prefix))
    if ctx.invoked_subcommand == None:
        games = discord.Embed(
                    colour = 0x00ffff
                )
        games.set_author(name=lang.gamecommands)
        games.add_field(name=("**" + prefix + lang.c4.lower().replace(' ', '') + "**"), value=lang.c4shortdesc, inline=False)
        games.add_field(name=("**" + prefix + lang.mc4.lower().replace(' ', '') + "**"), value=lang.mc4shortdesc, inline=False)
        games.add_field(name=("**" + prefix + lang.ttt.lower().replace(' ', '') + "**"), value=lang.tttshortdesc, inline=False)
        games.add_field(name=("**" + prefix + lang.bs.lower().replace(' ', '') + "**"), value=lang.bsshortdesc, inline=False)
        games.add_field(name=("**" + prefix + lang.mm.lower().replace(' ', '') + "**"), value=lang.mmshortdesc, inline=False)
        games.add_field(name=("**" + prefix + lang.hm.lower().replace(' ', '') + "**"), value=lang.hmshortdesc, inline=False)
        games.set_footer(text=lang.moreinfo)
        
        misc = discord.Embed(
                colour = 0x0000ff
            )
        misc.set_author(name=lang.misccommands)
        misc.add_field(name=("**" + prefix + lang.stop.lower().replace(' ', '') + "**"), value=lang.stopshortdesc, inline=False)
        misc.add_field(name=("**" + prefix + lang.lb.lower().replace(' ', '') + "**"), value=lang.lbshortdesc, inline=False)
        misc.add_field(name=("**" + prefix + lang.stats.lower().replace(' ', '') + "**"), value=lang.statsshortdesc, inline=False)
        misc.add_field(name=("**" + prefix + lang.prefix.lower().replace(' ', '') + "**"), value=lang.prefixshortdesc, inline=False)
        misc.add_field(name=("**" + prefix + lang.ping.lower().replace(' ', '') + "**"), value=lang.pingshortdesc, inline=False)
        misc.add_field(name=("**" + prefix + lang.disp.lower().replace(' ', '') + "**"), value=lang.dispshortdesc, inline = False)
        misc.add_field(name=("**" + prefix + lang.colour.lower().replace(' ', '') + "**"), value=lang.colourshortdesc, inline = False)
        misc.add_field(name=("**" + prefix + lang.help.lower().replace(' ', '') + "**"), value=lang.helpshortdesc, inline=False)
        misc.set_footer(text=lang.moreinfo)

        links = discord.Embed(
                title = lang.links,
                description = """[{}](https://patreon.com/CommunityGamesBot)
[{}](https://top.gg/bot/656058788020879370/vote)
[{}](https://forms.gle/G19i5t7cpdQHk72w9)
[{}](https://discordapp.com/api/oauth2/authorize?client_id=656058788020879370&permissions=387136&scope=bot)
[{}](https://discord.gg/dVHsMRK)""".format(lang.patreon, lang.vote, lang.suggest, lang.invite, lang.support),
                colour = 0xb32d7d
            )
        await ctx.send(embed=games)
        await ctx.send(embed=misc)
        await ctx.send(embed=links)

@helpcommand.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["b", "bs", "seabattle", "sb", "batallanaval", "battaglianavale", "bataillenavale", "морскойбой", "statki"]), ["战舰", "BATTLESHIP"]]))
async def battleship(ctx):
    if ctx.guild.id in prefixes: prefix = prefixes[ctx.guild.id]
    else: prefix = default_prefix
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id], prefix=prefix, commands=['battleship', 'battleships', 'seabattle', 'sb'])
    else: lang = Language("English", prefix=prefix, commands=['battleships', 'seabattle', 'sb'])
    if lang.bs == "Battleship" and lang.lang != "English": lang.update(commands=['battleships', 'seabattle', 'sb'])
    embed = discord.Embed(
            title=(prefix + lang.bs.lower().replace(" ", "") + " [{}]".format(lang.opponent)),
            description=lang.bslongdesc,
            colour=0xff0000
        )
    embed.set_footer(text=lang.canBeTriggeredWith)
    await ctx.send(embed=embed)

@helpcommand.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["mm", "codecrack", "codecracker", "cc", "mentemaestra", "быкиикоровы"]), ["策划者", "MASTERMIND"]]))
async def mastermind(ctx):
    if ctx.guild.id in prefixes: prefix = prefixes[ctx.guild.id]
    else: prefix = default_prefix
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id], prefix=prefix, commands=['mastermind', 'mm', 'codecracker', 'cc'])
    else: lang = Language("English", prefix=prefix, commands=['mm', 'codecracker', 'cc'])
    if lang.mm.lower() == "mastermind" and lang.lang != "English": lang.update(commands=['mm', 'codecracker', 'cc'])
    embed = discord.Embed(
            title=(prefix + lang.mm.lower().replace(" ", "") + " [{}] ({})".format(lang.opponent, lang.gamemode)),
            description=lang.mmlongdesc,
            colour=0xff0000
        )
    embed.set_footer(text=lang.canBeTriggeredWith)
    await ctx.send(embed=embed)

@helpcommand.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["c4", "connectfour", "conecta4", "connetti4", "puissance4", "четыревряд", "czwórki"]), ["连接4", "CONNECT4"]]))
async def connect4(ctx):
    if ctx.guild.id in prefixes: prefix = prefixes[ctx.guild.id]
    else: prefix = default_prefix
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id], prefix=prefix, commands=['connect4', 'connectfour', 'c4'])
    else: lang = Language("English", prefix=prefix, commands=['connectfour', 'c4'])
    embed = discord.Embed(
            title=(prefix + lang.c4.lower().replace(' ', '') + " [{}]".format(lang.opponent)),
            description=lang.c4longdesc,
            colour=0xff0000
        )
    embed.set_footer(text=lang.canBeTriggeredWith)
    await ctx.send(embed=embed)

@helpcommand.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["mc4", "megaconnectfour", "megaconecta4", "megaconnetti4", "mégapuissance4", "мегачетыревряд", "megaczwórki"]), ["巨型连接4", "MEGACONNECT4"]]))
async def megaconnect4(ctx):
    if ctx.guild.id in prefixes: prefix = prefixes[ctx.guild.id]
    else: prefix = default_prefix
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id], prefix=prefix, commands=['megaconnect4', 'megaconnectfour', 'mc4'])
    else: lang = Language("English", prefix=prefix, commands=['megaconnectfour', 'mc4'])
    embed = discord.Embed(
            title=(prefix + lang.mc4.lower().replace(' ', '')),
            description=lang.mc4longdesc,
            colour=0xff0000
        )
    embed.set_footer(text=lang.canBeTriggeredWith)
    await ctx.send(embed=embed)

@helpcommand.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["xo", "ttt", "noughtsandcrosses", "nc", "tresenlínea", "tris", "morpion", "крестики-нолики", "kółkoikrzyżyk"]), ["井字游戏", "TICTACTOE"]]))
async def tictactoe(ctx):
    if ctx.guild.id in prefixes: prefix = prefixes[ctx.guild.id]
    else: prefix = default_prefix
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id], prefix=prefix, commands=['tictactoe', 'ttt', 'xo'])
    else: lang = Language("English", prefix=prefix, commands=['ttt', 'xo'])
    embed = discord.Embed(
            title=(prefix + lang.ttt.lower().replace(' ', '') + " [{}]".format(lang.opponent)),
            description=lang.tttlongdesc,
            colour=0xff0000
        )
    embed.set_footer(text=lang.canBeTriggeredWith)
    await ctx.send(embed=embed)
    
@helpcommand.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["hm", "elahorcado", "impiccato", "man子手", "виселица", "wisielec"]), ["HANGMAN"]]))
async def hangman(ctx):
    if ctx.guild.id in prefixes: prefix = prefixes[ctx.guild.id]
    else: prefix = default_prefix
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id], prefix=prefix, commands=['hangman', 'hm'])
    else: lang = Language("English", prefix=prefix, commands='hm')
    embed = discord.Embed(
            title=(prefix + lang.hm.lower().replace(' ', '') + " (" + lang.gamemode + ")"),
            description=lang.hmlongdesc,
            colour=0xff0000
        )
    if lang.lang != "English": embed.description += "\n" + lang.hmEnglishWords
    embed.set_footer(text=lang.canBeTriggeredWith)
    await ctx.send(embed=embed)
    
@helpcommand.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["h", "ayuda", "aiuto", "aide", "помощь", "pomoc"]), ["帮助"]]))
async def help(ctx):
    if ctx.guild.id in prefixes: prefix = prefixes[ctx.guild.id]
    else: prefix = default_prefix
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id], prefix=prefix, commands=['help', 'h'])
    else: lang = Language("English", prefix=prefix, commands='h')
    embed = discord.Embed(
            title=(prefix + lang.help.lower().replace(' ', '') + " ({})".format(lang.command)),
            description=lang.helplongdesc,
            colour=0xff0000
        )
    embed.set_footer(text=lang.canBeTriggeredWith)
    await ctx.send(embed=embed)

@helpcommand.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["p", "пинг"]), ["呯", "PING"]]))
async def ping(ctx):
    if ctx.guild.id in prefixes: prefix = prefixes[ctx.guild.id]
    else: prefix = default_prefix
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id], prefix=prefix, commands=['ping', 'p'])
    else: lang = Language("English", prefix=prefix, commands='p')
    embed = discord.Embed(
            title=(prefix + lang.ping.lower()),
            description=lang.pinglongdesc,
            colour=0xff0000
        )
    embed.set_footer(text=lang.canBeTriggeredWith)
    await ctx.send(embed=embed)

@helpcommand.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["customprefix", "setprefix", "prefijo", "prefisso", "префикс", "prefiks"]), ["前缀", "PREFIX"]]))
async def prefix(ctx):
    if ctx.guild.id in prefixes: prefix = prefixes[ctx.guild.id]
    else: prefix = default_prefix
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id], prefix=prefix, commands=['prefix', 'customprefix', 'setprefix'])
    else: lang = Language("English", prefix=prefix, commands=['customprefix', 'setprefix'])
    embed = discord.Embed(
            title=(prefix + lang.prefix.lower() + " [{}]".format(lang.newprefix)),
            description=lang.prefixlongdesc,
            colour=0xff0000
        )
    embed.set_footer(text=lang.canBeTriggeredWith)
    await ctx.send(embed=embed)

@helpcommand.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["emoji", "avi", "avatar", "disp", "дисплей", "widok"]), ["显示", "DISPLAY"]]))
async def display(ctx):
    if ctx.guild.id in prefixes:
        prefix = prefixes[ctx.guild.id]
    else:
        prefix = default_prefix
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id], prefix=prefix, commands=['display', 'disp', 'emoji', 'avatar', 'avi'])
    else: lang = Language("English", prefix=prefix, commands=['disp', 'emoji', 'avatar', 'avi'])
    embed = discord.Embed(
            title=(prefix + lang.disp.lower() + " [{}]".format(lang.emoji)),
            description=lang.displongdesc,
            colour=0xff0000
        )
    embed.set_footer(text=lang.canBeTriggeredWith)
    await ctx.send(embed=embed)
    
@helpcommand.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["color", "c", "colore", "цвет", "kolor"]), ["颜色", "COLOUR"]]))
async def colour(ctx):
    if ctx.guild.id in prefixes:
        prefix = prefixes[ctx.guild.id]
    else:
        prefix = default_prefix
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id], prefix=prefix, commands=['colour', 'color', 'c'])
    else: lang = Language("English", prefix=prefix, commands=['color', 'c'])
    embed = discord.Embed(
            title=(prefix + lang.colour.lower() + " [{}]".format(lang.value)),
            description=lang.colourlongdesc,
            colour=0xff0000
        )
    embed.set_footer(text=lang.canBeTriggeredWith)
    await ctx.send(embed=embed)

@helpcommand.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["end", "kill", "quit", "parar", "стоп", "zakończgrę"]), ["停", "STOP"]]))
async def stop(ctx):
    if ctx.guild.id in prefixes: prefix = prefixes[ctx.guild.id]
    else: prefix = default_prefix
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id], prefix=prefix, commands=['stop', 'end', 'quit', 'kill'])
    else: lang = Language("English", prefix=prefix, commands=['end', 'quit', 'kill'])
    embed = discord.Embed(
            title=(prefix + lang.stop.lower().replace(' ', '')),
            description=lang.stoplongdesc,
            colour=0xff0000
        )
    embed.set_footer(text=lang.canBeTriggeredWith)
    await ctx.send(embed=embed)

@helpcommand.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["lang", "lenguaje", "lingua", "Язык", "język"]), ["语言", "LANGUAGE"]]))
async def language(ctx):
    if ctx.guild.id in prefixes: prefix = prefixes[ctx.guild.id]
    else: prefix = default_prefix
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id], prefix=prefix, commands=['language', 'lang'])
    else: lang = Language("English", prefix=prefix, commands='lang')
    embed = discord.Embed(
            title=(prefix + lang.language.lower() + " (" + lang.language.lower + ")"),
            description=lang.langlongdesc,
            colour=0xff0000
        )
    embed.set_footer(text=lang.canBeTriggeredWith)
    await ctx.send(embed=embed)

@helpcommand.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["lb", "clasificación", "classifica", "classement", "доскалидеров", "tabelawyników"]), ["排行榜", "LEADERBOARD"]]))
async def leaderboard(ctx):
    if ctx.guild.id in prefixes: prefix = prefixes[ctx.guild.id]
    else: prefix = default_prefix
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id], prefix=prefix, commands=['leaderboard', 'lb'])
    else: lang = Language("English", prefix=prefix, commands='lb')
    embed = discord.Embed(
            title=(prefix + lang.lb.lower() + " ({}) ({}) ({})".format(lang.game, lang.winrateoption, lang.globallocal)),
            description=lang.lblongdesc,
            colour=0xff0000
        )
    embed.set_footer(text=lang.canBeTriggeredWith)
    await ctx.send(embed=embed)

@helpcommand.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["statistics", "estadísticas", "statistiche", "statistiques", "статистика", "statystyki"]), ["统计", "STATS"]]))
async def stats(ctx):
    if ctx.guild.id in prefixes:
        prefix = prefixes[ctx.guild.id]
    else:
        prefix = default_prefix
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id], prefix=prefix, commands=["statistics", "stats"])
    else: lang = Language("English", prefix=prefix, commands="stats")
    embed = discord.Embed(
            title=(prefix + lang.stats.lower() + " [@{}]".format(lang.person)),
            description=lang.statslongdesc,
            colour=0xff0000
        )
    embed.set_footer(text=lang.canBeTriggeredWith)
    await ctx.send(embed=embed)

@bot.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["end", "kill", "quit", "parar", "стоп", "zakończgrę"]), ["停", "STOP"]])) # --------------------------------------------------------------------------------   S T O P  C O M M A N D   ----------------------------------------------------------------------------------
async def stop(ctx):
    global inGame
    global killing
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id], prefix=prefix)
    else: lang = Language("English", prefix=prefix)
    async def just_straight_up_end_the_game():
        msg = await ctx.send(lang.ending)
        while gameID in killing:
            await asyncio.sleep(0.5)
        await msg.edit(content=lang.stopped)
        return
    valid = False
    people = []
    for game in inGame:
        if ctx.author in inGame[game].players:
            valid = True
            gameID = inGame[game]
            playerindex = inGame[game].players.index(ctx.author)
            break
    if not valid:
        await ctx.send(lang.mustBeInGame)
        return
    valid = False
    if len(gameID.players) == 4:
        online = []
        for user in gameID.players:
            if str(user.status) != "offline" and user != ctx.author:
                online.append(user)
        if len(online) > 0:
            lang.update(", ".join(person.mention for person in online))
            msg = await ctx.send(lang.okayToStop)
        else:
            killing.append(gameID.gameID)
            await just_straight_up_end_the_game()
            return
        await msg.add_reaction("✅")
    elif len(gameID.players) == 1:
        killing.append(gameID.gameID)
        await just_straight_up_end_the_game()
        return
    else:
        if str(gameID.players[playerindex-1].status) != "offline":
            lang.update(gameID.players[playerindex-1].mention)
            msg = await ctx.send(lang.okayToStop)
            online = [gameID.players[playerindex-1]]
        else:
            killing.append(gameID)
            await just_straight_up_end_the_game()
            return
        await msg.add_reaction("✅")
    
    class Nothing:
        def __init__(self):
            self.nothing = ""
    
    timeout = ReactionTimeout(Nothing(), online, 120, msg, ["✅"])
    reacted = []
    while len(reacted) < len(online):
        emoji, user = await timeout.run()
        if emoji == "":
            await msg.delete()
            await ctx.message.delete()
            return
        for person in online:
            if person.id == user.id and person.id not in reacted:
                reacted.append(person.id)
    try:
        await msg.clear_reactions()
    except: pass
    killing.append(gameID.gameID)
    await msg.edit(content=lang.ending)
    while gameID.gameID in killing:
        await asyncio.sleep(1)
    await msg.edit(content=lang.stopped)


@bot.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["p", "пинг"]), ["呯", "PING"]])) # ----------------------------------------------------------------------------------- UTILITY/SETTINGS -----------------------------------------------------------------------------------
async def ping(ctx):
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id], prefix=prefix)
    else: lang = Language("English", prefix=prefix)
    before = time.monotonic()
    msg = await ctx.send("***{}***".format(lang.pong))
    ping = (time.monotonic() - before) * 1000
    diff = ping - bot.latency * 1000
    await msg.edit(content="***{}***\n{}".format(lang.pong, lang.connection) + str(round(bot.latency*1000)) + "ms\n{}".format(lang.processDelay) + str(round(diff)) + "ms\n{}".format(lang.latency) + str(round(ping)) + "ms")

@bot.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["customprefix", "setprefix", "prefijo", "prefisso", "префикс", "prefiks"]), ["前缀", "PREFIX"]]))
async def prefix(ctx, *, new_prefix=""):
    global prefixes
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id], prefix=prefix)
    else: lang = Language("English", prefix=prefix)
    if 0 < len(new_prefix) <= 8 and ctx.author.guild_permissions.manage_guild:
        lang.update(prefix=new_prefix)
        await ctx.send(lang.prefixSet)
        if new_prefix == default_prefix:
            if ctx.guild.id in prefixes: del prefixes[ctx.guild.id]
            else: pass
        else: prefixes[ctx.guild.id] = new_prefix
        file = open("prefixes.pkl", "wb")
        pickle.dump(prefixes, file, protocol=4)
        file.close()
    elif not ctx.author.guild_permissions.manage_guild:
        await ctx.send(lang.askAdminPrefix)
    elif len(new_prefix) > 8:
        await ctx.send(lang.prefixTooLong)
    elif len(new_prefix) == 0:
        try: prfx = prefixes[ctx.guild.id]
        except: prfx = default_prefix
        await ctx.send(lang.enterPrefix + "\n`" + prfx + lang.prefix.lower() + " cg.`")

@bot.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["lang", "lenguaje", "lingua", "Язык", "język"]), ["语言", "LANGUAGE"]]))
async def language(ctx, *, language=""):
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id], prefix=prefix)
    else: lang = Language("English", prefix=prefix)
    if ctx.author.guild_permissions.manage_guild:
        if language.lower() in ["english", "french", "francais", "français", "italian", "italiano", "spanish", "español", "espanol", "chinese", "中文", "russian", "русский язык", "русский", "polish", "polski", "język polski"]:
            if language.lower() == "english":
                if ctx.guild.id in langs:
                    del langs[ctx.guild.id]
                embed = discord.Embed(
                    title = "Language set to English",
                    colour = 0xb8c2d4
                )
                await ctx.send(content=None, embed=embed)
                file = open('lang.pkl', 'wb')
                pickle.dump(langs, file, protocol=4)
                file.close()
                return
            if language.lower() in ["french", "francais", "français"]: langs[ctx.guild.id] = "French"
            elif language.lower() in ["italian", "italiano"]: langs[ctx.guild.id] = "Italian"
            elif language.lower() in ["spanish", "español", "espanol"]: langs[ctx.guild.id] = "Spanish"
            elif language.lower() in ["chinese", "中文"]: langs[ctx.guild.id] = "Chinese"
            elif language.lower() in ["russian", "русский язык", "русский"]: langs[ctx.guild.id] = "Russian"
            elif language.lower() in ["polish", "polski", "język polski"]: langs[ctx.guild.id] = "Polish"
            lang = Language(langs[ctx.guild.id])
            lang.update(other=str(bot.get_user(lang.translatorID)))
            embed = discord.Embed(
                title = lang.setlang,
                description = lang.setlangdesc,
                colour = 0xb8c2d4)
            file = open('lang.pkl', 'wb')
            pickle.dump(langs, file, protocol=4)
            file.close()
            await ctx.send(content=None, embed=embed)
        else:
            flags = {"🇬🇧":("English", "English"), "🇪🇸":("Spanish", "Español"), "🇫🇷":("French", "Français"), "🇮🇹":("Italian", "Italiano"), "🇨🇳":("Chinese", "中文"), "🇷🇺":("Russian", "Русский язык"), "🇵🇱":("Polish", "Polski")}
            embed = discord.Embed(
                    title = lang.setLanguageHeader,
                    description = "\n".join(flag + " - " + flags[flag][1] for flag in flags),
                    colour = 0xb8c2d4
                )
            msg = await ctx.send(content=None, embed=embed)
            for flag in flags:
                await msg.add_reaction(flag)
            class Nothing:
                def __init__(self):
                    self.nothing = None
            timeout = ReactionTimeout(Nothing(), ctx.author, 120, msg, flags)
            emoji, user = await timeout.run()
            try: await msg.clear_reactions()
            except: pass
            if emoji != "" and user == ctx.author:
                if emoji == "🇬🇧":
                    if ctx.guild.id in langs:
                        del langs[ctx.guild.id]
                        embed = discord.Embed(
                            title = "Language set to English",
                            colour = 0xb8c2d4
                        )
                        await msg.edit(content=None, embed=embed)
                        file = open('lang.pkl', 'wb')
                        pickle.dump(langs, file, protocol=4)
                        file.close()
                        return
                else:
                    langs[ctx.guild.id] = flags[emoji][0]
                    lang = Language(langs[ctx.guild.id])
                    lang.update(other=str(bot.get_user(lang.translatorID)))
                    embed = discord.Embed(
                            title = lang.setlang,
                            description = lang.setlangdesc,
                            colour = 0xb8c2d4)
                    file = open('lang.pkl', 'wb')
                    pickle.dump(langs, file, protocol=4)
                    file.close()
                    await msg.edit(content=None, embed=embed)

    else:
        await ctx.send(lang.askAdminLanguage)

# ---------------------------------------------------------------------------------------- PREMIUM FEATURES----------------------------------------------------------------------------------------
@bot.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["emoji", "avi", "avatar", "disp", "дисплей", "widok"]), ["显示", "DISPLAY"]]))
async def display(ctx, emoji=""):
    global premium
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id], prefix=prefix)
    else: lang = Language("English", prefix=prefix)
    colour = 0x04b551
    found = False
    if ctx.author.id in premium:
        if emoji in ["⚫", "⬛", "<:darken:722694104718508072>", "<:blank:718734451785465977>"]:
            await ctx.send(content=None, embed=discord.Embed(title=lang.invalidEmoji, colour=0xcc2106))
            return

        if emoji == "":
            try: prfx = prefixes[ctx.guild.id]
            except: prfx = default_prefix
            await ctx.send(lang.enterEmoji + "\n`" + prfx + lang.disp.lower() + " " + random.choice(list(UNICODE_EMOJI)) +"`")
            return

        if type(premium[ctx.author.id][1]) == int: colour = premium[ctx.author.id][1]
        if emoji.lower() == lang.colours["reset"] or emoji.lower() == lang.colours["clear"] or emoji.lower() == "clear" or emoji.lower() == "reset":
            premium[ctx.author.id][0] = 0
            lang.update(user=str(ctx.author))
            await ctx.send(content=None, embed=discord.Embed(title=lang.displayDefault, colour=0xcccad9))
            file = open('premium.pkl', 'wb')
            pickle.dump(premium, file, protocol=4)
            file.close()
            return
        if emoji in UNICODE_EMOJI:
            premium[ctx.author.id][0] = emoji
            lang.update(user=str(ctx.author), other=emoji)
            await ctx.send(content=None, embed=discord.Embed(title=lang.displaySet, description=lang.displaySetDesc, colour=colour))
            file = open('premium.pkl', 'wb')
            pickle.dump(premium, file, protocol=4)
            file.close()
            return
        else:
            for x in ctx.guild.emojis:
                if str(x) == emoji or x.name == emoji.replace(":", ""):
                    premium[ctx.author.id][0] = str(x)
                    lang.update(user=str(ctx.author), other=x)
                    await ctx.send(content=None, embed=discord.Embed(title=lang.displaySet, description=lang.displaySetDesc, colour=colour))
                    file = open('premium.pkl', 'wb')
                    pickle.dump(premium, file, protocol=4)
                    file.close()
                    return

            await ctx.send(content=None, embed=discord.Embed(title=lang.noEmojiFound, colour=0x05759e))
            return
        await ctx.send(lang.noEmojiFound)
    else: await ctx.send(content=None, embed=discord.Embed(title=lang.onlyPremium, description=lang.becomePremium, colour=0x206996))


@bot.command(aliases=flatten([flatten((i.lower(), i.upper()) for i in ["color", "c", "colore", "цвет", "kolor"]), ["颜色", "COLOUR"]]))
async def colour(ctx, r="", g="", b=""):
    global premium
    global langs
    if ctx.guild.id in langs: lang = Language(langs[ctx.guild.id])
    else: lang = Language("English")

    if ctx.author.id in premium:
        def update(code=None):
            if code: premium[ctx.author.id][1] = code
            else: code = ""
            lang.update(user=str(ctx.author), other=strcode)
            file = open('premium.pkl', 'wb')
            pickle.dump(premium, file, protocol=4)
            file.close()
        if r.lower() in [lang.colours["reset"], lang.colours["clear"], "reset", "clear"]:
            lang.update(user=str(ctx.author))
            embed = discord.Embed(title=lang.colourDefault, colour=0xcccad9)
            await ctx.send(content=None, embed=embed)
            update()
            return
        elif r.lower() in lang.colours or r.lower() in [lang.colours[colour] for colour in lang.colours]:
            colours = {"red":0xff0000, "orange":0xff7f00, "gold":0xd99904, "yellow":0xffff00, "green":0x03ad03, "aqua":0x00ffff, "blue":0x0000ff, "purple":0xaa00ff, "violet":0xe36ffc, "magenta":0xff00ff, "pink":0xff5978, "white":0xfefefe, "gray":0x696969, "grey":0x696969, "black":0x000000}
            code = None
            for colour in lang.colours:
                if colour == r.lower():
                    code = colours[colour]
                elif lang.colours[colour].lower() == r.lower():
                    code = colours[colour]
                if code:
                    lstcode = list(str(hex(code)))[2:]
                    while len(lstcode) < 6: 
                        lstcode.insert(0, "0")
                    strcode = "".join(lstcode)
        elif b != "":
            try:
                r = int(r.replace(",", "").replace("(", ""))
                g = int(g.replace(",", ""))
                b = int(b.replace(")", ""))
                rgb = (r, g, b)
                for i in rgb:
                    if i < 0 or i > 255:
                        raise Exception
                strcode = "%02x%02x%02x" % rgb
                code = int(strcode, base=16)
            except:
                await ctx.send(content=None, embed=discord.Embed(title=lang.invalidRGB, description=lang.invalidRGBDesc, colour=0xe00d0d))
                return
        elif g == "" and r != "":
            strcode = r.replace("#", "")
            try: code = int(strcode, base=16)
            except:
                await ctx.send(content=None, embed=discord.Embed(title=lang.invalidHex, description=lang.invalidHexDesc, colour=0xe00d0d))
                return
        elif r == "":
            try: prfx = prefixes[ctx.guild.id]
            except: prfx = default_prefix
            await ctx.send(lang.enterColour + "\n`" + prfx + lang.colour.lower() + random.choice([
                (" " + random.choice([lang.colours[key] for key in list(lang.colours)[:-2]]) + "`"),
                (" #" + "%02x%02x%02x" % tuple([random.randint(0, 255) for i in range(3)]) + "`"),
                (" " + ", ".join([str(random.randint(0, 255)) for i in range(3)]) + "`")
                ]))
            return
        else:
            await ctx.send(content=None, embed=discord.Embed(title=lang.invalidInput, description=lang.invalidDesc, colour=0xe00d0d))
            return
        lang.update(user=ctx.author.name, other=("#" + strcode))
        embed = discord.Embed(title=lang.colourSet, colour=code)
        if strcode == "ffffff": embed.description = lang.notWhite
        else: embed.description = lang.colourSetDesc
        await ctx.send(content=None, embed=embed)
        update(code)
    else: await ctx.send(content=None, embed=discord.Embed(title=lang.onlyPremium, description=lang.becomePremium, colour=0x206996))
            



# ------------------------------------------------------------------------------------------ DEV STUFF ----------------------------------------------------------------------------------------

@bot.command()
async def shard(ctx):
    if ctx.author.id == 449433954529837056:
        await ctx.send("This guild is in shard #{} out of {}".format(str(ctx.guild.shard_id), str(bot.shard_count)))

@bot.command()
async def save(ctx):
    global windata
    if ctx.author.id == 449433954529837056:
        file = open('windata.pkl', 'wb')
        pickle.dump(windata, file, protocol=4)
        file.close()
        await ctx.send("Data saved")

@bot.command()
async def killbot(ctx):
    global windata
    global killingBot
    if ctx.author.id == 449433954529837056:
        currentGames = {"MasterMind" : 0, "Tic Tac Toe" : 0, "Connect 4" : 0, "Mega Connect 4" : 0, "Battleship" : 0, "Hangman" : 0}
        for g in inGame:
            currentGames[inGame[g].name] += 1
        killingBot = True
        await ctx.send(currentGames)
        string = ""
        count = 0
        for game in inGame:
            string += (str(game) + " - " + inGame[game].name + " - " + ", ".join(str(player) for player in inGame[game].players) + " - " + inGame[game].ctx.guild.name + " - #" + inGame[game].ctx.channel.name + "\n")
            count += 1
            if count == 30:
                await ctx.send(string)
                count = 0
                string = ""
        if string:
            lst = list(string)
            i = 0
            while i < len(lst):
                if lst[i] in ["*", "|", "`", "~"]:
                    lst.insert(i, "\\")
                    i += 1
                i += 1
            await ctx.send("".join(lst))
        clear = False
        while not clear:
            await asyncio.sleep(5)
            if not inGame:
                clear = True
        await ctx.send("All current games complete. Killing bot...")
        await bot.change_presence(status=discord.Status.offline)
        with open('windata.pkl', 'wb') as handle:
            pickle.dump(windata, handle, protocol=4)
        exit()

@bot.command()
async def running(ctx):
    if ctx.author.id == 449433954529837056:
        currentGames = {"MasterMind" : 0, "Tic Tac Toe" : 0, "Connect 4" : 0, "Mega Connect 4" : 0, "Battleship" : 0, "Hangman" : 0}
        for game in inGame:
            currentGames[inGame[game].name] += 1
        await ctx.send(currentGames)
        string = ""
        count = 0
        for game in inGame:
            string += (str(game) + " - " + inGame[game].name + " - " + ", ".join(str(player) for player in inGame[game].players) + " - " + inGame[game].ctx.guild.name + " - #" + inGame[game].ctx.channel.name + "\n")
            count += 1
            if count == 30:
                await ctx.send(string)
                count = 0
                string = ""
        if string:
            lst = list(string)
            i = 0
            while i < len(lst):
                if lst[i] in ["*", "|", "`", "~"]:
                    lst.insert(i, "\\")
                    i += 1
                i += 1
            await ctx.send("".join(lst))
            

@bot.command()
async def servers(ctx):
    if ctx.author.id == 449433954529837056:
        string = ""
        count = 0
        member_count = 0
        for server in bot.guilds:
            string += server.name + " - " + str(server.owner) + " - " + str(server.id) + "\n"
            count += 1
            member_count += len(server.members)
            if count == 30:
                await ctx.send(string)
                count = 0
                string = ""
        await ctx.send(string + "\n\nTotal members: " + str(member_count))

@bot.command(aliases=["fr", "forcestop", "fs"])
async def forceremove(ctx, game=None):
    if ctx.author.id == 449433954529837056:
        try:
            gameName = inGame[int(game)].name
            gamectx = inGame[int(game)].ctx
            players = inGame[int(game)].players
            del inGame[int(game)]
            await ctx.send("Successfully removed " + gameName + " game from list of ongoing games\n\nServer: '" + gamectx.guild.name + "'\nChannel: '#" + gamectx.channel.name + "'\nPlayers: " + ", ".join([str(p) for p in players]))
        except: await ctx.send("Invalid Game ID")

@bot.command(aliases=["vp"])
async def viewpremium(ctx):
    global premium
    if ctx.author.id == 449433954529837056:
        string = ""
        for i in premium:
            if bot.get_user(i): string += str(i) + " - " + str(bot.get_user(i)) + "\n"
            elif bot.get_guild(i): string += str(i) + " - " + bot.get_guild(i).name + "\n"
            else: string += str(i) + " - **Does not exist/Cannot be seen**\n"
        await ctx.send(string)


@bot.command()
async def padd(ctx, uid):
    if ctx.author.id != 449433954529837056:
        return
    try:
        uid = int(uid)
    except:
        await ctx.send("Invalid ID")
        return
    user = bot.get_user(uid)
    if not user:
        guild = bot.get_guild(uid)
        if not guild:
            await ctx.send("Could not find user/guild with that ID")
            return
        else:
            premium[uid] = 0
            await ctx.send(guild.name + " added to premium guilds")
    else:
        premium[uid] = [0, ""]
        await ctx.send(str(user) + " added to premium users")
    file = open('premium.pkl', 'wb')
    pickle.dump(premium, file, protocol=4)
    file.close()

@bot.command()
async def premove(ctx, uid):
    if ctx.author.id != 449433954529837056:
        return
    try:
        uid = int(uid)
    except:
        await ctx.send("Invalid ID")
        return
    if uid not in premium:
        await ctx.send("No such user/guild in premium list")
        return
    del premium[uid]
    user = bot.get_user(uid)
    if not user:
        guild = bot.get_guild(uid)
        await ctx.send(guild.name + " removed from premium guilds")
    else:
        await ctx.send(str(user) + " removed from premium users")
    file = open('premium.pkl', 'wb')
    pickle.dump(premium, file, protocol=4)
    file.close()

@bot.command()
async def toggle(ctx):
    if ctx.author.id != 449433954529837056:
        return
    if not ctx.guild.id in premium:
        premium[ctx.guild.id] = 0
        await ctx.send("Added this guild to premium guilds")
    else:
        del premium[ctx.guild.id]
        await ctx.send("Removed this guild from premium guilds")

@bot.command(aliases=["as"])
async def addstatus(ctx, *, status):
    if ctx.author.id != 449433954529837056:
        return
    global statuses
    statuses.append(status)
    await ctx.send("Successfully added to status loop\n" + status)

@bot.command(aliases=["vs", "viewstatuses"])
async def viewstatus(ctx):
    if ctx.author.id != 449433954529837056:
        return
    global statuses
    string = ""
    for i in statuses: string += i + "\n"
    await ctx.send(string)

@bot.command(aliases=["rs", "remstatus"])
async def removestatus(ctx, *, status):
    if ctx.author.id != 449433954529837056:
        return
    global statuses
    try: statuses.pop(int(status))
    except: statuses.remove(status)
    await ctx.send("Successfully removed from status loop\n" + status)


bot.add_cog(LoopsCog(bot)) 
bot.run(token)