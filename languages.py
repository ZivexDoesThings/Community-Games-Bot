import random

class Language:
    def  __init__(self, lang, user="", game="", user2="", permission="", mode="", shipType="", prefix="", commands="", number=0, wordPhrase="word", other="", other2=""):
        self.lang = lang
        self.user = user
        self.game_ = game
        self.user2 = user2
        self.permission = permission
        self.mode = mode
        self.shipType = shipType
        self.prfx = prefix
        self.commands = commands
        self.number = number
        self.wordPhrase = wordPhrase
        self.other = other
        self.other2 = other2
        if self.lang == "English":
            # Command Names
            self.c4 = "Connect 4"
            self.mc4 = "Mega Connect 4"
            self.ttt = "Tic Tac Toe"
            self.bs = "Battleship"
            self.mm = "MasterMind"
            self.hm = "Hangman"
            self.games = {"Connect 4":self.c4, "Mega Connect 4":self.mc4, "Tic Tac Toe":self.ttt, "Battleship":self.bs, "MasterMind":self.mm, "Hangman":self.hm, "":""}
            self.stop = "Stop"
            self.lb = "Leaderboard"
            self.stats = "Statistics"
            self.ping = "Ping"
            self.prefix = "Prefix"
            self.language = "Language"
            self.disp = "Display"
            self.colour = "Colour"
            self.help = "Help"

            # Utility Commands
            self.ending = "Alright then. Ending the game momentarily..."
            self.stopped = "The game has been stopped."
            self.mustBeInGame = "You need to be *in* a game before you can stop it!"
            self.okayToStop = "{}, is it okay if the game is stopped?".format(self.user)
            self.pong = "Pong!"
            self.connection = "Connection to Discord: "
            self.processDelay = "Process Delay: "
            self.latency = "Total Latency: "
            self.enterPrefix = "Please enter a prefix, like so:"
            self.prefixSet = "Prefix set to `{}`".format(self.prfx)
            self.prefixTooLong = "Prefix is too long! Must be 8 characters or less"
            self.askAdminPrefix = "You must have the 'Manage Server' permission to use this command. Ask an admin to change the prefix."
            self.askAdminLanguage = "You must have the 'Manage Server' permission to use this command. Ask an admin to change the language."
            self.setLanguageHeader = "Set language"

            # Help
            self.gamecommands = "Game Commands"
            self.c4shortdesc = "Get 4 in a row to win!"
            self.mc4shortdesc = "Connect 4, for 4 players!"
            self.bsshortdesc = "Sink your opponent's ships!"
            self.tttshortdesc = "Get 3 in a row to win!"
            self.mmshortdesc = "Solve your opponent's code!"
            self.hmshortdesc = "Figure out the word to avoid getting hung!"
            self.moreinfo = "Type {}help [command] to view more information on a command".format(self.prefix)

            self.misccommands = "Miscellaneous/Utility Commands"
            self.stopshortdesc = "Ends the game you're currently in"
            self.lbshortdesc = "Shows you the leaderboard(s)"
            self.statsshortdesc = "Shows you the stats of a selected person"
            self.pingshortdesc = "Checks the latency of the bot"
            self.prefixshortdesc = "Sets the bot's prefix"
            self.langshortdesc = "Sets the bot's language"
            self.dispshortdesc = "**(Premium users only)** Change your look in Connect 4 and Tic Tac Toe"
            self.colourshortdesc = "**(Premium users only)** Change your display colour for all games"
            self.helpshortdesc = "Does this, duh"

            self.links = "Links"
            self.patreon = "Patreon"
            self.vote = "Give a vote on the Discord Bot List"
            self.suggest = "Suggest a Game"
            self.invite = "Invite Me to Your Server"
            self.support = "Support Server"

            self.opponent = "@opponent"
            self.gamemode = "gamemode"
            self.game = "game"
            self.command = "command"
            self.winrateoption = "wins/rate"
            self.globallocal = "global/local"
            self.local = "local"
            self.person = "person"
            self.newprefix = "new prefix"
            self.emoji= "emoji"
            self.value = "value"
            if type(self.commands) == list: self.canBeTriggeredWith = "This command can also be triggered with '{}' and '{}'".format("', '".join(self.commands[:-1]), self.commands[-1])
            else: self.canBeTriggeredWith = "This command can also be triggered with '{}'".format(self.commands)
            self.bslongdesc = "The two players will place their ships on a 10x10 grid secretly. The players take turns at guessing the locations of said ships, using results from previous turns as reference. They will then be shown whether they hit a ship or missed entirely. Play continues until someone has sunk all of the other player's ships."
            self.mmlongdesc= "The two players will create a code for each other to figure out. The players take turns at guessing the codes, using results from previous turns as reference. They will then be shown whether each digit was in the correct position, elsewhere in the code or not in the code at all. Play continues until both players have completely solved their codes.\n\nThe 'gamemode' argument is optional. It will default to colours if left empty, but you can enter \"numbers\", \"n\" or \"number\" to enter number mode, or put in \"colours\", \"colors\", \"colour\", \"color\" or \"c\" because you can."
            self.c4longdesc = "Select a row to drop your checker into. Stack them on top of each other to get 4 in a row - horizontally, vertically or diagonally - before your opponent does to win."
            self.mc4longdesc = "The same rules as connect four, but here there are 4 players.\nSelect a row to drop your checker into. Stack them on top of each other to get 4 in a row - horizontally, vertically or diagonally - before anyone else does to win."
            self.tttlongdesc = "Take turns to claim squares on a 3x3 grid. The first player to get 3 in a row - horizontally, vertically or diagonally - wins."
            self.hmlongdesc = "Figure out the word to avoid being hung. For 1-4 players, but **premium games can have up to 16 players.**\nIf the gamemode argument is left empty, all players will vote for the game mode they wish to play in.\nCo-op mode: All players take turns to help solve the same word.\nCompetitive mode: All players secretly choose a word, which is given to another player to solve. The winner is the first to solve their word with the least number of incorrect attempts."
            self.helplongdesc = "Shows you all the commands, or the details of a specific command."
            self.pinglongdesc = "Returns the current latency of the bot."
            self.stoplongdesc = "After asking the other player/s if they're okay with it, the game you're in will end prematurely. The game will end instantly if all the other players are offline. Useful if someone needs to leave in a hurry."
            self.lblongdesc = "Displays the leaderboard for the requested game of the same command, in all servers, or just the server you're in. You can sort the leaderboard by most amount of wins, or highest win rate. All arguments are optional, and order does not matter."
            self.statslongdesc = "Displays the statistics of the selected person. If no person is selected, it will show your own."
            self.prefixlongdesc = "Changes the bot's prefix for the server.\nPrefix must be 8 characters or less, and set by someone with the 'Manage Server' permission."
            self.langlongdesc = "Changes the language for the server.\nLanguage can only be set by members with the 'Manage Server' permission."
            self.displongdesc = "Changes how your pieces look in Connect 4, Mega Connect 4 and Tic Tac Toe. Works with any custom emoji (including animated), as long as the bot is in the server with that emoji.\nNo Nitro? No problem. Just enter the name of the emoji, and it will still be accepted.\n**This feature can only be used by premium users. Become one [here.](https://patreon.com/CommunityGamesBot/)**"
            self.colourlongdesc = "Changes your display colour (on the little bar on the side) in all games. Use an RGB value or a hex code to set it.\n**This feature can only be used by premium users. Become one [here.](https://patreon.com/CommunityGamesBot/)**"
            self.thisServer = "This Server"
            self.allServers = "All Servers"
            self.lbstates = {"This Server":self.thisServer, "All Servers":self.allServers}
            self.allGames = "All Games"
            self.emptylb = "There's no one on this leaderboard yet!"
            self.emptylb2 = "Will you be the first?"
            self.placings = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th"]
            self.cantSeePerson = "I can't see that person..."
            self.youHaveNoStats = "You don't have any statistics yet!"
            self.theyHaveNoStats = "{} doesn't have any statistics yet!".format(self.user)
            self.personsStats = "{}'s Stats".format(self.user)
            self.wins = "Wins"
            self.losses = "Losses"
            self.draws = "Draws"
            self.highScores = "High Scores"
            self.played = "Games Played"
            self.winRate = "Win Rate"
            self.total = "Total"

            # Pre-Game
            self.addReactions = "Add Reactions"
            self.manageMessages = "Manage Messages"
            self.readHistory = "Read Message History"
            self.externalEmoji = "Use External Emojis"
            self.permissions = {"Add Reactions" : self.addReactions, "Manage Messages" : self.manageMessages, "Read Message History" : self.readHistory, "Use External Emojis" : self.externalEmoji, "":""}

            if type(self.permission) == list:
                needed = []
                for i in self.permission:
                    needed.append(self.permissions[i])
                self.needPerms = "I can't do that at the moment. I need the following permissions:\n- {}\nIf you want to know why, visit the FAQ on the support server at https://discord.gg/dVHsMRK".format("\n- ".join(needed))
            elif type(self.permission) == str: self.needPerms = "I can't do that at the moment. I need the '{}' permission first.\nIf you want to know why, visit the FAQ on the support server at https://discord.gg/dVHsMRK".format(self.permissions[self.permission])
            self.mentionOpponent = "You need to mention an opponent, like so:\n"
            self.botsCantPlay = "Bot's aren't smart enough to play {}!".format(self.games[self.game_])
            self.cantFindPerson = "Hmm, I can't seem to find that person in this server."
            self.cantPlayAgainstSelf = "You can't play against yourself!"
            self.bothPlaying = "Both of you are already playing with each other!"
            self.youreAlreadyPlaying = "You're already playing a game with someone else!"
            self.theyreAlreadyPlaying = "{} is in another game at the moment!".format(self.user)
            self.bothPlayingElsewhere = "You're both playing different games elsewhere!"
            self.theyreOffline = "They appear to be offline right now. Try someone else."
            self.reactToStartGame = "{}, are you ready to play {}?\n\nReact with ✅ in the next 3 minutes to start the game, or it will be cancelled.".format(self.user, self.games[self.game_])
            self.goneElsewhere = "Oh, wait... you two have gone into a game elsewhere!"
            self.userInOtherGame = "Aw man, {} is in another game now. Guess we'll wait up for them.".format(self.user)
            self.finishOtherGameFirst = "Hold up, {}, you're in another game at the moment! Finish that before you do anything else.".format(self.user)
            self.bothGone = "Oh, dear. You've both gone into other games with different people. Come back when you finish!"
            self.userWentOffline = "Oh, no! {} went offline! Guess we can't play now... :shrug:".format(self.user)
            self.noResponse = "{} did not respond. The game has been cancelled.".format(self.user)
            self.whosPlaying4 = "Who wants to play?\n3 people (other than {}) need to react with ✅ to start the game.".format(self.user)
            self.noOneWantsToPlay = "No-one else seems to want to play. Game cancelled."
            self.whosPlayingUnlimited = "Who wants to play {}?\nReact with ✅ to join the game.\n{}, use the same reaction when everyone has joined to start the game.".format(self.games[self.game_], self.user)
            self.cancelUnlimited = "Looks like the person that started the game decided they didn't want to play. Game cancelled."
            self.startMaxPlayers = "Maximum number of players reached. Let's start the game!"
            self.premiumCanHaveMore = "Premium games can have up to {} players! Visit https://patreon.com/CommunityGamesBot/ to learn more.".format(self.number)
            self.gameStarting = "{}... The game is starting!".format(self.user)
            self.needToDM = "{}, I need to be able to DM you in order to set up the game.\nTo fix this, go to the server dropdown (next to the server's name), select 'Privacy Settings' and enable the 'Allow direct messages from server members' setting.".format(self.user)

            # General Game Phrases
            self.playersTurn = "It's {}'s turn!".format(self.user)
            self.playerWon = "{} won!".format(self.user)
            if type(self.user2) == list: losers = ", ".join(self.user2[:-1]) + " and " + self.user2[-1]
            else: losers = self.user2
            self.playerWonAgainst = "{} won the {} game against {}!".format(self.user, self.games[self.game_], losers)
            self.draw = "It's a Draw!"
            if type(self.user) == list: people = ", ".join(self.user[:-1]) + " and " + self.user[-1]
            else: people = self.user
            self.endedInDraw = "The {} game between {} ended in a draw!".format(self.games[self.game_], people)
            self.gameWasStopped = "This game was manually stopped"
            self.error = "Oops! An error occured."
            self.errorStopped = "Oops! An error occured. The game has been stopped."
            self.errorWon = "An error occured, however, {} won!".format(self.user)

            # Specific Game Phrases
            self.c4HowTo = "React with the number corresponding to the row you wish to use.\nYou have 30 seconds to make your move."
            self.c4Timeout = "{} took too long to answer. A random row was selected.".format(self.user)
            self.c4Offline = "{} is offline. A random row was selected.".format(self.user)

            self.tttHowTo = "Use the reaction corresponding to the tile you wish to take.\nYou have 30 seconds to choose."
            self.tttTimeout = "{} took too long! Their turn was skipped.".format(self.user)

            self.mmWaitForCodes = "Waiting for codes to be created..."
            self.prepareMakeCode = "Get ready to create your code!"
            self.createCode = "Create your 6-digit code!"
            self.mmTimeLimit = "You have 20 seconds to input each individual part of the code."
            self.codeFinished = "Code finished!"
            self.goToChannel = "Now head to the channel the game was started in to play!"
            self.previousTurns = "Previous turns:"
            self.roundNumber = "Round "
            self.thisTurn = "This turn:"
            self.resultsFromTurn = "Results from {}'s turn:".format(self.user)
            if self.mode == "colour": self.codeType =  "The colour"
            else: self.codeType = "The number"
            self.mmInfo = "✅ = {} is in the correct position\n❔ = {} is somewhere else in the code\n❌ = {} is not in the code".format(self.codeType, self.codeType, self.codeType)
            self.reactWhenReady = "React with 👍 when you are ready to proceed"
            self.notOverYet = "It's not over yet!"
            self.userFinishGameCont = "{} may have finished, but the game continues until both of you are done!".format(self.user)
            self.gameEndedPossibleWinner = "The game ended prematurely, but it seems to be a win for {}!".format(self.user)
            self.gameEndedWinner = "The game ended prematurely, but {} won!".format(self.user)
            self.gameEnded = "The game ended prematurely"
            self.noRounds = "No rounds were completed"
            self.userDidNotComplete = "{} did not get to complete their first round".format(self.user)

            self.waitForShips = "Waiting for ships to be planted..."
            self.preparePlaceShips = "Preparing to place ships..."
            if self.shipType == "Aircraft Carrier": self.ship = "Aircraft Carrier"
            elif self.shipType == "Battleship": self.ship = "Battleship"
            elif self.shipType == "Destroyer": self.ship = "Destroyer"
            elif self.shipType == "Submarine": self.ship = "Submarine"
            elif self.shipType == "Patrol Boat": self.ship = "Patrol Boat"
            else: self.ship = ""
            self.placingShip = "Placing {}".format(self.ship)
            self.positionSetTimeout = "The position will be automatically set if no adjustment is made in 15 seconds"
            self.fleetReady = "Fleet ready!"
            self.userAiming = "{} is aiming...".format(self.user)
            self.selectX = "You have 20 seconds to select an x co-ordinate"
            self.selectY = "You have 20 seconds to select a y co-ordinate"
            self.alreadyFiredThere = "You've already fired there, try somewhere else."
            self.firing = "Firing..."
            self.hit = "Hit!"
            self.missed = "Missed"
            self.sunkShip = "{} sunk {}'s {}!".format(self.user, self.user2, self.ship)
            self.usersShots = "{}'s shots:\n".format(self.user)
            self.possibleWinner = "At this point, it looks to be a win for {}!".format(self.user)
            self.possibleDraw = "At this point, it looks to be a draw!"

            self.hmEnglishWords = "Please note: Words selected at random by the bot are all in English"
            self.hmModeVote = "What gamemode do you want to play in?\nReact with :wrestling: to vote for competitive, or :handshake: for co-op\n\nYou have 10 seconds to cast your votes"
            self.calculateResult = "Calculating result..."
            self.voteDraw = "A draw? I'll put my vote in then..."
            self.modes = {"comp":"competitive", "co-op":"co-op", "colour":"", "number":""}
            if self.mode: self.gameModeSelected = "**{}** game mode selected. Let's begin!".format(self.modes[self.mode].capitalize())
            self.hmOnePlayer = "Just you? Alright then."
            self.incorrectGuesses = "Incorrect Guesses:"
            self.takeAGuess = "{}, take a guess".format(self.user)
            if self.wordPhrase == "word": self.wordPhrase = "word"
            else: self.wordPhrase = "phrase"
            self.hmHowTo = "Type in the letter you think is in the {}, or the {} itself.\nYou have {} seconds to make a guess".format(self.wordPhrase, self.wordPhrase, self.number)
            self.alreadyGuessed = random.choice(["Looks like", "Whoops,", "Uhh,", "Hmm,"]) + " you've already guessed that! Try something else."
            self.invalidLetter = random.choice(["Oops,", "Whoops,", "Uh oh,", "Hmm,"]) + " that's not a valid letter! Try again."
            self.invalidWord = random.choice(["Oops,", "Whoops,", "Uh oh,", "Hmm,"]) + " that's not a valid {}! Try again.".format(self.wordPhrase)
            self.letterNotInWord = "The letter {} is not in the {}".format(self.other, self.wordPhrase)
            self.incorrectWord = "'{}' is not the {}.".format(self.other, self.wordPhrase)
            self.letterAppearsOnce = "The letter {} appears once in the {}".format(self.other, self.wordPhrase)
            self.letterAppearsTwice = "The letter {} appears twice in the {}".format(self.other, self.wordPhrase)
            self.letterAppears = "The letter {} appears {} times in the {}".format(self.other, self.other2, self.wordPhrase)
            self.hmTimeout = "You ran out of time to make your guess!"
            self.failedToGuess = "You failed to guess the {}".format(self.wordPhrase)
            self.wordWas = "The {} was: ".format(self.wordPhrase)
            self.youWin = "You win!"
            s1 = ""
            if self.other != "1": s1 = "s"
            s2 = ""
            if self.other2 != "1": s2 = "es"
            self.coOpWinStats = "You took a total of {} attempt{} to guess the {}, with {} incorrect guess{} to spare.".format(self.other, s1, self.wordPhrase, self.other2, s2)
            if type(self.user) == list: people = ", ".join(self.user[:-1]) + " and " + self.user[-1]
            else: people = self.user
            s = ""
            if self.other != "1": s = "s"
            self.hmCoOpEnd = "{} successfully figured out the {} - '{}' - in {} attempt{}".format(people, self.wordPhrase, self.other, self.other2, s)

            self.yes = "yes"
            self.waitForWords = "Waiting for people to create words..."
            self.hmSetup = "What's your word? Just type it in. You have one minute to come up with something."
            self.hmSetupTimeout = "Well, your minute's up. I'll just go ahead and pick a random word for you...\nYou can go to the channel the game was started in now."
            self.hmSetupInvalid = "Sorry, that's invalid. Use only English alphanumeric characters and basic punctuation."
            self.hmTooLong = "That {} is too long! The maximum length is 100 characters".format(self.wordPhrase)
            self.hmTooShort = "That {} is too short! The minimum length is 4 letters".format(self.wordPhrase)
            self.hmSetupConfirm = "Your word is: **{}**\nType 'yes' to confirm, or a different word if you want to change it.".format(self.other)
            self.hmSetupConfirmTimeout = "No response? I'll confirm it for you, then.\nHead over to the channel the game was started in to play!"
            self.hmSetupComplete = "Cool, you're all set up. Head on over to the channel the game was started in to play!"
            self.hmSetupCancel = "Oh, nevermind... The game's been stopped."
            self.hmAllSetupsComplete = "Now that everyone's got their words in, let's get started!"
            self.yourTurn = "Your turn, {}!".format(self.user)
            self.wordFinished = "You finished the {}!".format(self.wordPhrase)
            if self.other == 1: s1 = ""
            else: s1 = "s"
            if self.other2 == 1: s2 = ""
            else: s2 = "s"
            self.personFinished = "You took {} attempt{} to guess the {}, with {} incorrect attempt{} to spare!\nStick around for the results when everyone's finished!".format(self.other, s1, self.wordPhrase, self.other2, s2)
            self.hmeliminated = "You failed to guess the word. You have been eliminated."
            self.everyoneFinished = "Everyone's finished! Calculating results..."
            self.totalAttempts = "Total Attempts: "
            self.correctAttempts = "Correct Attempts: "
            self.incorrectAttempts = "Incorrect Attempts: "
            self.score = "Score: "
            self.scoreUnavailable = "-Score unavailable-"
            self.highScore = "High Score: "


            self.promotitles = [
                "Hey, you seem to be enjoying these games a lot.",
                "You've been playing quite a bit, haven't you?",
                "Wow, you really like these games, don't you?",
                "Woah, you've played a lot of games recently."]
            self.promodesc = [
                "Have you considered [becoming a patron?](https://patreon.com/CommunityGamesBot)\nA pledge would help towards expanding this bot for more capabilities.",
                "If you've got any spare change, why not [become a patron?](https://patreon.com/CommunityGamesBot)\nEven the smallest of pledges would help expand this bot :)",
                "You could help this bot get around by [voting for it.](https://top.gg/bot/656058788020879370/vote)\nIf you could take a few seconds to do so, it would be greatly appreciated :)",
                "Why not give me a vote over at [top.gg](https://top.gg/bot/656058788020879370/vote)?\nI'd really appreciate it :)"]

            self.onlyPremium = "Only premium users can use this feature!"
            self.becomePremium = "Become one [here](https://patreon.com/CommunityGamesBot/)"
            self.displaySet = "Connect 4 and Tic Tac Toe display for {} set to {}".format(self.user, self.other)
            self.displaySetDesc = "If you ever want to set your display back to the default, use 'clear' or 'reset' instead of an emoji"
            self.displayDefault = "Display for {} set to default".format(self.user)
            self.noEmojiFound = "Sorry, I couldn't find that emoji in this server."
            self.invalidEmoji = "Sorry, you may not use that emoji."
            self.enterEmoji = "Please enter an emoji, like so:"
            self.invalidRGB = "Invalid RGB value."
            self.invalidRGBDesc = "Be sure to only use integers between 0 and 255.\nAlternatively, you can use a hex code (such as #f42cb1), or a common colour name."
            self.invalidHex = "Invalid hex value."
            self.invalidHexDesc = "Be sure to only use 0-9 and a-f.\nAlternatively, you can use an RGB value (such as 61, 26, 125), or a common colour name."
            self.invalidInput = "Invalid input."
            self.invalidDesc = "Make sure you enter a valid RGB (such as 61, 26, 125) or hex value (such as #f42cb1), or a standard colour name."
            self.colourSet = "Colour for {} set to {}".format(self.user, self.other)
            self.colourSetDesc = "If you ever want to set your display back to the default, use 'clear' or 'reset' instead of a colour value"
            self.colourDefault = "Colour for {} set to default".format(self.user)
            self.notWhite = "Don't worry, it's normal for it to not appear white, because Discord treats it as its own default value.\nIf you want white, I would recommend using #fefefe (or 254, 254, 254) instead."
            self.enterColour = "Please enter a colour, like so:"
            self.colours = {"red":"red", "orange":"orange", "gold":"gold", "yellow":"yellow", "green":"green", "aqua":"aqua", "blue":"blue", "purple":"purple", "violet":"violet", "magenta":"magenta", "pink":"pink", "white":"white", "gray":"gray", "black":"black", "reset":"reset", "clear":"clear"}

            self.downtime = "Hang on, I'm just gonna have some brief downtime (probably to update). I'll be back in a few minutes!"
            self.comingSoon = "This game is coming soon!\nWant to play it now? Become a beta tester at https://patreon.com/CommunityGamesBot/"

        if self.lang == "Spanish": # Translation by JDTheQwerty
            self.translatorID = 146009145290653696
            # Command Names
            self.c4 = "Conecta 4"
            self.mc4 = "Mega Conecta 4"
            self.ttt = "Tres en Línea"
            self.bs = "Batalla Naval"
            self.mm = "Mente Maestra"
            self.hm = "El Ahorcado"
            self.games = {"Connect 4":self.c4, "Mega Connect 4":self.mc4, "Tic Tac Toe":self.ttt, "Battleship":self.bs, "MasterMind":self.mm, "Hangman":self.hm, "":""}
            self.stop = "Parar"
            self.lb = "Clasificación"
            self.stats = "Estadísticas"
            self.ping = "Ping"
            self.prefix = "Prefijo"
            self.language = "Lenguaje"
            self.disp = "Presentación"
            self.colour = "Color"
            self.help = "Ayuda"

            # Utility Commands
            self.ending = "Está bien. Terminando el juego en un momento..."
            self.stopped = "El juego ha sido parado."
            self.mustBeInGame = "¡Debes de estar *dentro* de un juego antes de poder pararlo!"
            self.okayToStop = "{}, está bien si el juego es parado?".format(self.user)
            self.pong = "¡Pong!"
            self.connection = "Conexión a Discord: "
            self.processDelay = "Retraso del Proceso: "
            self.latency = "Latencia total: "
            self.enterPrefix = "Por favor ingresa un prefijo, así:"
            self.prefixSet = "Prefijo puesto como `{}`".format(self.prfx)
            self.prefixTooLong = "¡El prefijo es demasiado largo! Debe de ser de 8 caracteres o menos."
            self.askAdminPrefix = "Debes tener el permiso 'Gestionar servidor' para usar este comando. Pregúntale a un admin que cambie el prefijo."
            self.askAdminLanguage = "Debes tener el permiso 'Gestionar servidor' para usar este comando. Pregúntale a un admin que cambie el lenguaje."
            self.setLanguageHeader = "Ajusta el Lenguaje"
            self.setlang = "Lenguaje puesto a español"
            self.setlangdesc = "Traducido por {}".format(self.other)

            # Help
            self.gamecommands = "Comandos de Juego"
            self.c4shortdesc = "Consigue 4 en línea para ganar"
            self.mc4shortdesc = "Conecta 4, para 4 jugadores"
            self.bsshortdesc = "Hunde las naves de tu oponente"
            self.tttshortdesc = "Consigue 3 en línea para ganar"
            self.mmshortdesc = "Resuelve el código de tu oponente"
            self.hmshortdesc = "Descubre la palabra antes de ser ahorcado"
            self.moreinfo = "Escribe {}ayuda (comando) para ver mas información del comando.".format(self.prfx)

            self.misccommands = "Comandos Misceláneos/de Utilidad"
            self.stopshortdesc = "Termina el juego en el que estas"
            self.lbshortdesc = "Te muestra la clasificación(es)"
            self.statsshortdesc = "Te muestra las estadísticas de una persona seleccionada."
            self.pingshortdesc = "Chequea la latencia del bot"
            self.prefixshortdesc = "Cambia el prefijo del bot"
            self.langshortdesc = "Cambia el idioma del bot"
            self.dispshortdesc = "**(Solo usuarios premium)** Cambia tu apariencia en Conecta 4 y Tres en línea"
            self.colourshortdesc = "**(Solo usuarios premium)** Cambia tu color de display para todos los juegos"
            self.helpshortdesc = "Hace esto, duh"

            self.links = "Enlaces"
            self.patreon = "Patreon"
            self.vote = "Dale un voto en la Lista de Bots de Discord"
            self.suggest = "Sugiere un Juego"
            self.invite = "Invítame a Tu Servidor"
            self.support = "Servidor de Ayuda"

            self.opponent = "@oponente"
            self.gamemode = "modo de juego"
            self.game = "juego"
            self.command = "comando"
            self.winrateoption = "triunfos/ratio"
            self.globallocal = "global/local"
            self.local = "local"
            self.person = "persona"
            self.newprefix = "nuevo prefijo"
            self.emoji = "emoji"
            self.value = "valor"
            if type(self.commands) == list: self.canBeTriggeredWith = "Este comando también puede ser usado con '{}' y '{}'".format("', '".join(self.commands[:-1]), self.commands[-1], self.commands[-1])
            else: self.canBeTriggeredWith = "Este comando también puede ser usado con '{}'".format(self.commands)
            self.bslongdesc = "Dos jugadores pondrán sus naves en una cuadrícula de 10x10 secretamente. Los jugadores toman turnos para adivinar la ubicación de esas mismas naves, usando resultados de las rondas anteriores como referencia. Ellos van a ver si le dieron a una nave o fallaron rotundamente. El juego continua hasta que alguien haya hundido todas las naves del jugador contrario."
            self.mmlongdesc= "Dos jugadores crearan un código para que el otro lo descubra. Los jugadores tomarán turnos para adivinar los códigos, usando los resultados de las rondas anteriores como referencia. Ellos verán si el dígito estaba en la posición correcta, en otro lugar del código o si ni siquiera estaba en el código. El juego continua hasta que ambos jugadores hayan resuelto completamente el código. \n\nEl argumento 'mode de juego' es opcional. Este sera por predeterminado 'colores' si se queda vacío, pero puedes poner \"números\", \"n\" o \"numero\" para entrar el mode numero, o poner \"colores\", \"color\" o \"c\" porque puedes."
            self.c4longdesc = "Selecciona una fila para soltar verticalmente tu ficha. Apílalas encima de cada una para obtener un 4 en línea - horizontal, vertical o diagonalmente - antes de que tu oponente lo haga para ganar."
            self.mc4longdesc = "Aplican las mismas reglas que en Conecta 4, pero aquí hay 4 jugadores. \nSelecciona una fila para soltar verticalmente tu ficha. Apílalas encima de cada una para obtener un 4 en línea - horizontal, vertical o diagonalmente - antes de que tus oponentes lo hagan para ganar."
            self.tttlongdesc = "Tomen turnos para reclamar cuadrados en una cuadrícula 3x3. El primer jugador en obtener un 3 en línea,  - horizontal, vertical o diagonalmente - gana."
            self.hmlongdesc = "Descubre la palabra para evitar ser ahorcado. De 1-4 jugadores, pero **juegos premium pueden tener hasta 16 jugadores.**\nSi el argumente de modo de juego es dejado en blanco, todos los jugadores tomaran un voto para el mode de juego que ellos quisieran jugar.\nModo cooperativo: Todos los jugadores toman turnas para resolver la misma palabra.\nMode competitivo: Todos los jugadores secretamente eligen una palabra, que se le es dada a otro jugador para resolver. El ganador es el primero en resolver su palabra con el menor número de intentos incorrectos."
            self.helplongdesc = "Te muestra todos los comandos, o los detalles de un comando en específico."
            self.pinglongdesc = "Te devuelva la latencia del momento del bot."
            self.stoplongdesc = "Después de preguntar al otro jugador/ a los otros jugadores, si están de acuerdo, el juego en el que estas terminara prematuramente. El juego terminara instantáneamente si todos los otros jugadores están online. Útil si alguien necesita salir inmediatamente."
            self.lblongdesc = "Muestra la clasificación por el juego pedido del mismo comando, en todos los servidores, o solo el servidor ene el que estas. Puedes navegar las clasificaciones por mayor cantidad de triunfos, o por mayor ratio de triunfos. Todos los argumentos son opcionales, el orden no importa."
            self.statslongdesc = "Te muestra las estadísticas de la persona seleccionada. Si no hay persona seleccionada, te mostrará las tuyas."
            self.prefixlongdesc = "Cambia el prefijo del bot en este servidor. \nEl prefijo debe ser de menos de 8 caracteres o menos, y puesto por alguien por el permiso de 'Gestionar Servidor'."
            self.langlongdesc = "Cambia el lenguaje para el servidor.\nEl lenguaje solo puede ser cambiado por usuarios que tengan el permiso de 'Manejar el Servidor'."
            self.displongdesc = "Cambia como tus piezas se muestran en Conecta 4, Mega Conecta 4 y Tres en Línea. Funciona con cualquier emoji personalizado (incluyendo los animados), si el bot esta en el servidor con ese emoji. \n¿No tienes nitro? Ningún problema, solo pon el nombre del emoji, y será aceptado.\n**Esta característica solo puede ser usada por usuarios premium. Haste uno [aquí.](https://patreon.com/CommunityGamesBot/)**"
            self.colourlongdesc = "Cambia el color de la pantalla (en la pequeña barra de al lado) en todos los juegos. Usa un valor RGB o un código hex para ponerlo.\n**Esta característica solo la pueden usar usuarios premium. Conviértete en uno [aquí.](https://patreon.com/CommunityGamesBot/)**"
            self.thisServer = "Este Servidor"
            self.allServers = "Todos los Servidores"
            self.lbstates = {"This Server":self.thisServer, "All Servers":self.allServers}
            self.allGames = "Todos los Juegos"
            self.emptylb = "¡No hay nadie en esta clasificación aún!"
            self.emptylb2 = "¿Serás el primer?"
            self.placings = ["1ro", "2do", "3ro", "4to", "5to", "6to", "7to", "8vo", "9no", "10mo"]
            self.cantSeePerson = "No puede ver a esa persona..."
            self.youHaveNoStats = "¡Aun no tienes estadísticas!"
            self.theyHaveNoStats = "¡{} aun no tiene estadísticas!".format(self.user)
            self.personsStats = "Estadísticas de {}".format(self.user)
            self.wins = "Triunfos"
            self.losses = "Derrotas"
            self.draws = "Empates"
            self.highScores = "Mejores Puntajes"
            self.played = "Juegos"
            self.winRate = "Ratio de Triunfos"
            self.total = "Total"

            # Pre-Game
            self.addReactions = "Añadir Reacciones"
            self.manageMessages = "Gestionar Mensajes"
            self.readHistory = "Leer el historial de mensajes"
            self.externalEmoji = "Usar emojis externos"
            self.permissions = {"Add Reactions" : self.addReactions, "Manage Messages" : self.manageMessages,
                                "Read Message History" : self.readHistory, "Use External Emojis" : self.externalEmoji, "":""}

            if type(self.permission) == list:
                needed = []
                for i in self.permission:
                    needed.append(self.permissions[i])
                self.needPerms = "No puedo hacer esto en este momento. Necesito los siguientes permisos:\n- {}\nSi no sabes porque, visita la FAQ en el servidor de ayuda en https://discord.gg/dVHsMRK".format("\n- ".join(needed))
            elif type(self.permission) == str:
                self.needPerms = "No puedo hacer esto en ese momento. Necesito el permiso '{}' antes.\nSi no sabes porque, visita la FAQ en el servidor de ayuda en https://discord.gg/dVHsMRK".format(self.permissions[self.permission])
            self.mentionOpponent = "Necesitas mencionar un oponente, así:\n"
            self.botsCantPlay = "¡Bots no son tan inteligentes para jugar {}!".format(self.games[self.game_])
            self.cantFindPerson = "Hmm, no puede encontrar a ese persona en este servidor."
            self.cantPlayAgainstSelf = "¡No puedes jugar contra ti mismo!"
            self.bothPlaying = "¡Ambos ya están jugando un juego con el otro!"
            self.youreAlreadyPlaying = "¡Esta en otro juego ahora mismo! Termina ese juego primero antes de empezar otro."
            self.theyreAlreadyPlaying = "¡{} esta en otro juego en el momento!".format(self.user)
            self.bothPlayingElsewhere = "¡Ambos están jugando otros juegos en otra parte!"
            self.theyreOffline = "Parece que está offline en este momento. Intenta con otra personas?"
            self.reactToStartGame = "¿{}, estas listo para jugar {}?\n\nReacciona con ✅ en los siguientes 3 minutos para empezar el juego, o sera cancelado.".format(self.user, self.games[self.game_])
            self.goneElsewhere = "Oh, espera... ustedes dos ya están en otro juego en otra parte."
            self.userInOtherGame = "Aw man, {} ya esta en otro juego ahora. Supongo que esperaremos por el/ella.".format(self.user)
            self.finishOtherGameFirst = "¡Espera, {}, estas en otro juego en este momento! Termina eso antes de que te unas a otra cosa.".format(self.user)
            self.bothGone = "Hay mi madre. Ustedes ya están en otro juego con diferentes personas. ¡Vuelvan cuando terminen!"
            self.userWentOffline = "¡Oh no! {} esta offline! Supongo que no podemos jugar ahora... :shrug:".format(self.user)
            self.noResponse = "{} no respondió. EL juego ha sido cancelado.".format(self.user)
            self.whosPlaying4 = "¿Quién quiere jugar?\n3 personas (ademas de {}) deben de reaccionar con ✅ para empezar el juego.".format(self.user)
            self.noOneWantsToPlay = "Parece que nadie más quiere jugar. El juego ha sido cancelado."
            self.whosPlayingUnlimited = "¿Quién quiere jugar {}?\nReacciona con ✅ para unirte al juego,\n{}, usa la misma reacción cuando todos se han unido para empezar el juego.".format(self.games[self.game_], self.user)
            self.cancelUnlimited = "Parece que la personas que empezó el juego no quizo jugar. El juego ha sido cancelado."
            self.startMaxPlayers = "El número máximo de jugadores a sido alcanzado. ¡Ha empezar el juego!"
            self.premiumCanHaveMore = "Juegos premium pueden tener hasta {} jugadores! Visita ttps://patreon.com/ CommunityGamesBot/ para saber más.".format(self.number)
            self.gameStarting = "{}... El juego esta empezando!".format(self.user)
            self.needToDM = "{}, Necesito poder mandarte mensajes directos para empezar el juego. \nPara arreglar esto ve al despegable del server (al lado del nombre del servidor), selecciona 'Ajustes de Privacidad' y enciende el ajuste de 'Permitir mensajes directos de miembros del servidor'.".format(self.user)

            # General Game Phrases
            self.playersTurn = "¡Es el turno de {}!".format(self.user)
            self.playerWon = "¡{} ganó!".format(self.user)
            if type(self.user2) == list: losers = ", ".join(self.user2[:-1]) + " y " + self.user2[-1]
            else: losers = self.user2
            self.playerWonAgainst = "{} gano el juego de {} contra {}!".format(self.user, self.games[self.game_], losers)
            self.draw = "¡Es un empate!"
            if type(self.user) == list: people = ", ".join(self.user[:-1]) + " y " + self.user[-1]
            else: people = self.user
            self.endedInDraw = "¡El juego de {} entre {} terminó en empate!".format(self.game, people)
            self.gameWasStopped = "El juego ha sido parado manualmente."
            self.error = "¡Ups! Ocurrió un error."
            self.errorStopped = "¡Ups! Ocurrió un error. El juego ha sido parado."
            self.errorWon = "Ocurrió un error, sin embargo, {} gano!".format(self.user)

            self.modes = {"comp":"competitivo", "co-op":"cooperativo", "colour":["colores", "color", "c"], "number":["números", "n", "numero", "numeros"]}

            # Specific Game Phrases
            self.c4HowTo = "Reacciona con el numero correspondiente a la fila que deseas usar.\nTienes 30 segundos para hacer tu jugada."
            self.c4Timeout = "{} se tomo demasiado tiempo para responder. Una fila aleatoria fue seleccionada.".format(self.user)
            self.c4Offline = "{}esta offline. Una fila aleatoria fue seleccionada.".format(self.user)

            self.tttHowTo = "Usa la reacción correspondiente a la ficha que deseas tomar.\nTienes 30 segundos para elegir."
            self.tttTimeout = "¡{} se tomo demasiado tiempo! Su turno fue saltado.".format(self.user)

            self.mmWaitForCodes = "Esperando a que los códigos sean creados..."
            self.prepareMakeCode = "¡Prepárense para crear sus códigos!"
            self.createCode = "¡Crea tu código de 6 dígitos!"
            self.mmTimeLimit = "Tienes 20 segundos para elegir cada parte individual del código."
            self.codeFinished = "¡Código terminado!"
            self.goToChannel = "¡Ahora ve al canal donde se empezó el juego para jugar!"
            self.previousTurns = "Rondas anteriores:"
            self.roundNumber = "Ronda "
            self.thisTurn = "Esta ronda:"
            self.resultsFromTurn = "Resultados del turno de {}:".format(self.user)
            if self.mode == "colour": self.codeType =  "color"
            else: self.codeType = "número"
            self.mmInfo = """✅ = El {} correcto esta en su posición correcta.\n❔ = El {} esta en otra parte del código.\n❌ = El {} no esta en el código.""".format(self.codeType, self.codeType, self.codeType)
            self.reactWhenReady = "Reacciona con 👍 para cuando estes listo para proceder."
            self.notOverYet = "¡Esto no se ha acabado aún!"
            self.userFinishGameCont = "{} ya a terminado, ¡pero el juego continua hasta que ambos terminen!".format(self.user)
            self.gameEndedPossibleWinner = "El juego ha terminado prematuramente, ¡pero parece que este es un triunfo para {}!".format(self.user)
            self.gameEndedWinner = "El juego ha terminado prematuramente, ¡pero {} ganó!".format(self.user)
            self.gameEnded = "El juego ha terminado prematuramente"
            self.noRounds = "Ninguna ronda fue completada"
            self.userDidNotComplete = "{} no pudo terminar su primera ronda".format(self.user)

            self.waitForShips = "Esperando que las naves sean plantadas..."
            self.preparePlaceShips = "Preparándose para poner la naves..."
            if self.shipType == "Aircraft Carrier": self.ship = "Portador"
            elif self.shipType == "Battleship": self.ship = "Acorazado"
            elif self.shipType == "Destroyer": self.ship = "Destructor"
            elif self.shipType == "Submarine": self.ship = "Submarino"
            elif self.shipType == "Patrol Boat": self.ship = "Bote de Patrulla"
            else: self.ship = ""
            self.placingShip = "Poniendo {}".format(self.ship)
            self.positionSetTimeout = "La posición sera automáticamente puesta si ningún ajuste es hecho en 15 segundos"
            self.fleetReady = "¡Flota lista!"
            self.userAiming = "{} esta apuntando...".format(self.user)
            self.selectX = "Tienes 20 segundos para elegir la coordenada x"
            self.selectY = "Tienes 20 segundos para elegir la coordenada y"
            self.alreadyFiredThere = "Ya has disparado aquí, intenta otro lugar."
            self.firing = "Disparando..."
            self.hit = "Impacto!"
            self.missed = "Fallaste."
            self.sunkShip = "¡{} hundió el {} de {}!".format(self.user, self.ship, self.user2)
            self.usersShots = "Disparos de {}:\n".format(self.user)
            self.possibleWinner = "A este punto, parece un triunfo para {}!".format(self.user)
            self.possibleDraw = "A este punto, parece un empate!"

            self.hmEnglishWords = "Nota: Todas las palabras del seleccionadas aleatoriamente por el bot están en ingles"
            self.hmModeVote = "¿Que modo de juego quieres jugar?\nReacciona con :wrestling: para votar competitivo, o :handshake: para cooperativo\n\nTienen 10 segundos para votar"
            self.calculateResult = "Calculando resultado..."
            self.voteDraw = "¿Empate? Pondré mi voto entonces..."
            if self.mode: self.gameModeSelected = "El mode de juego **{}** ha sido seleccionado. ¡Empecemos!".format(self.modes[self.mode])
            self.hmOnePlayer = "¿Solo tú? Está bien."
            self.incorrectGuesses = "Adivinanzas incorrectas:"
            self.takeAGuess = "{}, es tu turno para intentar adivinar".format(self.user)
            if self.wordPhrase == "word": self.wordPhrase = "palabra"
            elif self.wordPhrase == "phrase": self.wordPhrase = "frase"
            self.hmHowTo = "Escribe la letra que crees que esta en la {}, o la misma {}\nTienes 30 segundos para elegir".format(self.wordPhrase, self.wordPhrase)
            self.alreadyGuessed = random.choice(["¡Parece que", "¡Ups,", "¡Uhh,", "¡Hmm,"]) + " ya has adivinaste esto! Intenta otra cosa."
            self.invalidLetter = random.choice(["¡Parece que", "¡Ups,", "¡Uhh,", "¡Hmm,"]) + " esa no es una letra valida! Intenta otra vez."
            self.invalidWord = random.choice(["¡Parece que", "¡Ups,", "¡Uhh,", "¡Hmm,"]) + " esa no es una {} valida! Intenta de nuevo.".format(self.wordPhrase)
            self.letterNotInWord = "La letra {} no esta en la {}".format(self.other, self.wordPhrase)
            self.incorrectWord = "'{}' no es la {}.".format(self.other, self.wordPhrase)
            self.letterAppearsOnce = "La letra {} aparece 1 vez en la {}".format(self.other, self.wordPhrase)
            self.letterAppearsTwice = "La letra {} aparece 2 veces en la {}".format(self.other, self.wordPhrase)
            self.letterAppears = "La letra {} aparece {} veces en la {}".format(self.other, self.other2, self.wordPhrase)
            self.hmTimeout = "¡Se terminó tu tiempo para adivinar!"
            self.failedToGuess = "Fallaste para adivinar la {}".format(self.wordPhrase)
            self.wordWas = "La {} era: ".format(self.wordPhrase)
            self.youWin = "¡Ganaste!"
            s1 = ""
            if self.other != "1": s1 = "s"
            s2 = ""
            if self.other2 != "1": s2 = "s"
            self.coOpWinStats = "Ustedes colectivamente tomaron {} intento{} para adivinar {}, con {} adivinanza{} incorrecta{} de sobra.".format(self.other, s1, self.wordPhrase, self.other2, s2, s2)
            if type(self.user) == list: people = ", ".join(self.user[:-1]) + " y " + self.user[-1]
            else: people = self.user
            s = ""
            if self.other != "1": s = "s"
            self.hmCoOpEnd = "{} exitosamente adivinaron la {} en {} intento{}".format(people, self.wordPhrase, self.other, s)

            self.yes = "si"
            self.waitForWords = "Esperando a que las personas creen palabras..."
            self.hmSetup = "¿Cual es tu palabra? Solo escríbela.. Tienes un minuto para esto."
            self.hmSetupTimeout = "Parece que se acabo tu tiempo. Solo elegiré una palabra aleatoria para ti...\nPuedes ir al canal donde el juego empezó ahora."
            self.hmSetupInvalid = "Lo siento, eso es invalido. Solo usa caracteres ingleses alfanuméricos y puntuación básica"
            self.hmTooLong = "Esa {} es demasiado larga! El máximo es 100 caracteres".format(self.wordPhrase)
            self.hmTooShort = "Esa {} es demasiado corta! El mínimo es 4 caracteres".format(self.wordPhrase)
            self.hmSetupConfirm = "Tu palabra es: **{}**\nEscribe 'si' para confirmar, o elige otra palabra si deseas cambiarla.".format(self.other)
            self.hmSetupConfirmTimeout = "¿No hay respuesta? Te la confirmare por ti entonces.\n¡Ve al canal dónde se empezó el juego para jugar!"
            self.hmSetupComplete = "Bien, estas todo listo. ¡Ve al canal dónde se empezó el juego para jugar!"
            self.hmSetupCancel = "Oh, no importa... El juego ha sido parado."
            self.hmAllSetupsComplete = "Ahora que todo el mundo creo sus palabras, ¡empecemos!"
            self.yourTurn = "Tu turno, {}!".format(self.user)
            self.wordFinished = "¡Terminaste la palabra!"
            if self.other == "1": s1 = ""
            else: s1 = "s"
            if self.other2 == "1": s2 = ""
            else: s2 = "s"
            self.personFinished = "¡Tomaste {} intento{} para adivinar la {}, con {} adivinanza{} incorrecta{} de sobra!\n¡Quedate para ver los resultados para cuando todos terminen!".format(self.other, s1, self.wordPhrase, self.other2, s2, s2)

            self.hmeliminated = "Fallaste para adivinar {}. Has sido eliminado.".format(wordPhrase)
            self.everyoneFinished = "¡Todo el mundo ha terminado! Calculando resultados..."
            self.totalAttempts = "Intentos Totales: "
            self.correctAttempts = "Intentos Correctos: "
            self.incorrectAttempts = "Intentos Incorrectos: "
            self.score = "Puntaje: "
            self.scoreUnavailable = "-Puntaje no disponible-"
            self.highScore = "Mejor Puntaje: "

            self.promotitles = [
                "Hey, he visto que estas disfrutando mucho de estos juegos.",
                "Has estado jugando mucho, ¿no?",
                "Wow, te encantan estos juegos, ¿no?",
                "Woah, has estado jugando muchos juegos reciente mente."]
            self.promodesc = [
                "¿Por qué no votar por mi en [top.gg](https://top.gg/bot/656058788020879370/vote)?\nLo apreciaría mucho.",
                "Has considerado [convertirte en un patron?](https://patreon.com/CommunityGamesBot)\nUna donación ayudaría para expandir las capabilidades de este bot?",
                "Tu pudieras ayudar impulsar a este bot [votando por él.](https://top.gg/bot/656058788020879370/vote)\nSi pudieras tomarte algunos segundos para esto, seria de gran aprecio.",
                "Si tienes un poco de dinero de sobra, ¿por qué no [convertirte en un patron?](https://patreon.com/CommunityGamesBot)\nHasta las menores donaciones ayudarían a expandir este bot."]


            self.onlyPremium = "¡Solo usuarios premium pueden usar esta característica!"
            self.becomePremium = "Haste un [aquí](https://patreon.com/CommunityGamesBot/)"
            self.displaySet = "Como se muestra Conecta 4 y Tres en línea para {} puesto a {}".format(self.user, self.other)
            self.displaySetDesc = "Si quieres tu display de vuelta a lo normal, usa 'borrar' o 'resetear' envés de un emoji"
            self.displayDefault = "El display de {} vuelve a lo normal".format(self.user)
            self.noEmojiFound = "Lo siento, no pude encontrar ese emoji en este servidor."
            self.enterEmoji = "Por favor ingresa un emoji, así:"
            self.invalidRGB = "Valor de RGB invalido."
            self.invalidRGBDesc = "Debes usar solo números entre 0 y 255.\nTambién puedes usar códigos hex (como #f42cb1), o un nombre de color común."
            self.invalidHex = "Valor de hex invalido."
            self.invalidHexDesc = "Debes usar solo 0-9 y a-f.\nTambién, puedes usar un valor RGB (como 61, 26, 125), o un nombre de color común."
            self.invalidInput = "Entrada invalida."
            self.invalidDesc = "Debes poner un código RGB valido (como 61, 26, 125) o un valor hex (como #f42cb1), o un nombre de color común."
            self.colourSet = "Color para {} puesto como {}".format(self.user, self.other)
            self.colourSetDesc = "Si quieres que se vea de vuelta a lo norma, usa 'borrar' o 'resetear' en vez de un valor de color"
            self.enterColour = "Por favor ingresa un color, así:"
            self.notWhite = "No importa, es muy normal que no aparezca blanco, porque Discord lo trata como su propio valor predeterminado.\nSi quieres blanco, recomiendo usar #fefefe (o 254, 254, 254)"
            self.colourDefault = "Color para {} vuelve a lo normal".format(self.user)
            self.colours = {"red":"rojo", "orange":"naranja", "gold":"dorado", "yellow":"amarillo", "green":"verde", "aqua":"aqua", "blue":"azul", "purple":"morado", "violet":"violeta", "magenta":"magenta", "pink":"rosado", "white":"blanco", "gray":"gris", "black":"negro", "reset":"resetear", "clear":"borrar"}

            self.downtime = "Espera, solo voy a estar fuera de linea por un tiempo (probablemente para actualizarme). ¡Estaré devuelta en algunos minutos!"
            self.comingSoon = "¡Este juego viene pronto!\n¿Quieres jugarlo ahora? Conviértete en betatester en https://patreon.com/CommunityGamesBot/"


        if self.lang == "Italian": # Translation by Enrico
            self.translatorID = 350363572045348875
            # Command Names
            self.c4 = "Connetti 4"
            self.mc4 = "Mega Connetti 4"
            self.ttt = "Tris"
            self.bs = "Battaglia navale"
            self.mm = "MasterMind"
            self.hm = "Impiccato"
            self.games = {"Connect 4":self.c4, "Mega Connect 4":self.mc4, "Tic Tac Toe":self.ttt,
                            "Battleship":self.bs, "MasterMind":self.mm, "Hangman":self.hm, "":""}
            self.stop = "Stop"
            self.lb = "Classifica"
            self.stats = "Statistiche"
            self.ping = "Ping"
            self.prefix = "Prefisso"
            self.language= "Lingua"
            self.disp = "Display"
            self.colour = "Colore"
            self.help = "Aiuto"

            # Utility Commands
            self.ending = "Ok. Terminazione della partita in corso..."
            self.stopped = "La partita è stata terminata."
            self.mustBeInGame = "Devi partecipare ad una partita prima di poterla abbandonare!"
            self.okayToStop = "{}, posso terminare la partita?".format(self.user)
            self.pong = "Pong!"
            self.connection = "Connessione a Discord: "
            self.processDelay = "Ritardo di Sistema: "
            self.latency = "Latenza totale: "
            self.enterPrefix = "Perfavore inserire un prefisso, esempio:"
            self.prefixSet = "Prefisso impostato a `{}`".format(self.prfx)
            self.prefixTooLong = "Il prefisso indicato è troppo lungo! Deve essere di 8 o meno caratteri."
            self.askAdminPrefix = "Devi avere il permesso di 'Gestire il Server' per poter eseguire questo comando. Chiedi ad un admin di cambiare il prefisso."
            self.askAdminLanguage = "Devi avere il permesso di 'Gestire il Server' per poter eseguire questo comando. Chiedi ad un admin di cambiare la lingua."
            self.setLanguageHeader = "Imposta Lingua"
            self.setlang = "Lingua impostata ad Italiano"
            self.setlangdesc = "Tradotto da {}".format(self.other)

            # Help
            self.gamecommands = "Comandi di Gioco"
            self.c4shortdesc = "Ottieni 4 in fila per vincere!"
            self.mc4shortdesc = "Connetti 4, per 4 giocatori!"
            self.bsshortdesc = "Affonda le navi del tuo avversario!"
            self.tttshortdesc = "Ottieni 3 in fila per vincere!"
            self.mmshortdesc = "Decodifica il codice del tuo avversario!"
            self.hmshortdesc = "Trova la parola prima di rimanere *impiccato*"
            self.moreinfo = "Scrivi {}aiuto (comando) per maggiori informazioni sul comando".format(self.prfx)

            self.misccommands = "Extra"
            self.stopshortdesc = "Termina la partita che stai giocando"
            self.lbshortdesc = "Mostra la classifica"
            self.statsshortdesc = "Mostra le informazioni riguardo la persona indicata"
            self.pingshortdesc = "Controlla la latenza del bot"
            self.prefixshortdesc = "Cambia il prefisso del bot"
            self.langshortdesc = "Imposta la lingua del bot"
            self.dispshortdesc = "**(Solo utenti premium)** Cambia la tua apparenza in Connetti 4 e Tris"
            self.colourshortdesc = "**(Solo utenti premium)** Cambia il colore di tutti i giochi"
            self.helpshortdesc = "Fa questo, mi pare abbastanza ovvio"

            self.links = "Link"
            self.patreon = "Patreon"
            self.vote = "Valuta in Discord Bot List"
            self.suggest = "Suggerisci un nuovo gioco"
            self.invite = "Invitami nel tuo server"
            self.support = "Supporta il Server"

            self.opponent = "@avversario"
            self.gamemode = "modalità di gioco"
            self.game = "gioco"
            self.command = "comando"
            self.winrateoption = "vincite/percentuale"
            self.globallocal = "mondiale/locale"
            self.local = "locale"
            self.person = "persona"
            self.newprefix = "nuovo prefisso"
            self.emoji= "emoji"
            self.value = "valore"
            if type(self.commands) == list: self.canBeTriggeredWith = "Questo comando può essere eseguito anche con '{}' e '{}'".format("', '".join(self.commands[:-1]), self.commands[-1])
            else: self.canBeTriggeredWith = "Questo comando può essere eseguito anche con '{}'".format(self.commands)
            self.bslongdesc = "I due giocatori piazzeranno in segreto le loro navi in una griglia 10x10. Poi a turno poveranno ad indovinare la posizione delle navi, con i risultati dei tentativi precedenti come riferimento. Gli sarà in seguito mostrato se hanno colpito o mancato. La partita continua fino a quando qualcuno non ha afondato tutte le navi dell'altro."
            self.mmlongdesc= "I due giocatori creeranno un codice che l'avversario dovrà scoprire. Poi a turno proveranno ad indovinare il codice, con i risultati dei tentativi precedenti come riferimento. Verrà poi indicato se il carattere indicato è corretto, si torva in un altra posizione o è assente. La partita continua fino a quando entrambi i giocatori non hanno scoperto il codice. \n\nL'argomento 'modalità di gioco' è opzionale. Di abse sarà colori, ma può anche essere \"numeri\", \"n\" o \"numero\" per selezionare modalità numero, o inserisci \"colori\", \"colore\" o \"c\" perchè si può."
            self.c4longdesc = "Seleziona una colonna per inserire la tua pedina. Continua ad impilarle fino a quando non ne ottieni 4 in fila - orizzontalmente, verticalmente o diagonalmente - prima che il tuo avversario vinca."
            self.mc4longdesc = "Le stesse regole di conneti 4, ma con 4 giocatori. \nSeleziona una colonna per inserire la tua pedina. Continua ad impilarle fino a quando non ne ottieni 4 in fila - orizzontalmente, verticalmente o diagonalmente - prima che i tuoi avversari vincano."
            self.tttlongdesc = "Uno per volta si prende possesso di un quadratino su una griglia 3x3. Il primo giocatore ad ottenerne 3 in fila - orizzontalmente, verticalmente o diagonalmente - vince."
            self.hmlongdesc = "Trova la parola prima di finire impiccato. Per 1-4 giocatori, ma **premium permette fino a 16.**\nSe l'argomento della modalità di gioco è lasciato vuoto, tutti i giocatori voteranno per la modalità di gioco in cui desiderano giocare.\nModalità cooperativa: tutti cercano di trovare la stessa parola.\nModalità competitiva: tutti i giocatori scelgono segretamente una parola, che viene assegnata ad un altor giocatore per trovarla. Il vincitore è il primo a trovare la parola con il minor numero di sentativi scorretti."
            self.helplongdesc = "Mostra tutti i comandi o dettagli di uno specifico comando."
            self.pinglongdesc = "Indica la latenza attuale del bot."
            self.stoplongdesc = "Dopo aver chiesto conferma agli altri partecipanti, il gioco finirà prematuramente. Il gioco finirà instantaneamente se tutti i partecipanti vanno offline. Utile se qualcuno ha bisogno di lasciare di fretta."
            self.lblongdesc = "Mostra la classifica per il gioco richiesto nello stesso comando, in tutti i server, o solo nel server in cui ti trovi. Puoi ordinare la classifica per il maggior numero di vittorie o per la maggior percentuale di vincite. Tutti gli argomenti sono opzionali e l'ordine di questi non importa."
            self.statslongdesc = "Mostra le statistiche della persona selezionata. Se nessuna persona è selezionata, mostrerà i tuoi dati."
            self.prefixlongdesc = "Cambia il prefisso del bot per il server.\nIl prefisso deve essere lungo almeno 8 caratteri o meno, e deve essere configurato da qualcuno che ha il permesso di 'Gestire il Server'."
            self.langlongdesc = "Cambia la lingua per il server.\nLa lingua può essere cambiata solo dagli utenti col permesso di 'Gestire il Server'."
            self.displongdesc = "Cambia lo stile delle pedine di Connetti 4, Mega Connetti 4 e Tris. Funziona con tutte le emoji, anche quelle personalizzate e animate, ma il bot necessita di essere nel server con quell'emoji.\nNiente Nitro? Nessun problema, semplicemente inserisci il nome dell'emoji, e verrà comunque accettato.\n**Questa funzione può essere utilizzata solo da utenti premium. Puoi diventarne uno [qui.](https://patreon.com/CommunityGamesBot/)**"
            self.colourlongdesc = "Cambia il tuo colore (quella piccola barra sul lato) in tutti i giochi. Inserisci un valore RGB o codice hex per impostarlo.\n**Questa funzione può essere utilizzata solo da utenti premium. Puoi diventarne uno [qui.](https://patreon.com/CommunityGamesBot/)**"
            self.thisServer = "Questo server"
            self.allServers = "Tutti i server"
            self.lbstates = {"This Server":self.thisServer, "All Servers":self.allServers}
            self.allGames = "Tutti i giochi"
            self.emptylb = "Non c'è nessuno i questa classifica!"
            self.emptylb2 = "Sarai tu il primo?"
            self.placings = ["1°", "2°", "3°", "4°", "5°", "6°", "7°", "8°", "9°", "10°"]
            self.cantSeePerson = "Non posso vedere quella persona..."
            self.youHaveNoStats = "Non hai ancora nessuna classifica!"
            self.theyHaveNoStats = "{} non ha ancora nessuna statistica!".format(self.user)
            self.personsStats = "Statistica di {}".format(self.user)
            self.wins = "Vittorie"
            self.losses = "Sconfitte"
            self.draws = "Pareggi"
            self.highScores = "Record"
            self.played = "Partite giocate"
            self.winRate = "Percentuale vittorie"
            self.total = "Totali"

            # Pre-Game
            self.addReactions = "Aggiungere Reazioni"
            self.manageMessages = "Gestire Messaggi"
            self.readHistory = "Leggere I Messaggi"
            self.externalEmoji = "Utilizzare Emoji Esterne"
            self.permissions = {"Add Reactions" : self.addReactions, "Manage Messages" : self.manageMessages,
                                "Read Message History" : self.readHistory, "Use External Emojis" : self.externalEmoji, "":""}

            if type(self.permission) == list:
                needed = []
                for i in self.permission:
                    needed.append(self.permissions[i])
                self.needPerms = "Non posso fare quello al momento. Ho prima bisogno dei seguenti permessi:\n- {}\nSe vuoi sapere perchè, visita il FAQ sul server di supporto a https://discord.gg/dVHsMRK".format("\n- ".join(needed))
            elif type(self.permission) == str:
                self.needPerms = "Non posso fare questo al momento. Ho prima bisogno della permesso per '{}'.\nSe vuoi sapere perchè, visita il FAQ sul server di supporto a https://discord.gg/dVHsMRK".format(self.permissions[self.permission])
            self.mentionOpponent = "Devi menzionare uno sfidante, così:\n"
            self.botsCantPlay = "I computer non sono abbastanza inteligenti per giocare a {}!".format(self.games[self.game_])
            self.cantFindPerson = "Hmm, non riesco a trovare quella persona in questo server."
            self.cantPlayAgainstSelf = "Non puoi giocare da solo! *La socializzazione è importante!*"
            self.bothPlaying = "Entrambi siete pronti a giocare!"
            self.youreAlreadyPlaying = "Sei attualmente in un altra partita! Finisci quella che stai giocando prima di iniziarne una nuova."
            self.theyreAlreadyPlaying = "{} è attualmente in un altra partita!".format(self.user)
            self.bothPlayingElsewhere = "State partecipando tutti e due un gioco diverso!"
            self.theyreOffline = "Sembra che l'utente sia offline. Prova con qualcun altro."
            self.reactToStartGame = "{}, sei pronto per giocare a {}?\n\nReagisci con ✅ entro 3 minuti per far iniziare il gioco, altrimenti verrà cancellato.".format(self.user, self.games[self.game_])
            self.goneElsewhere = "Oh, aspetta un secondo . . . voi due avete iniziato a giocare da qualche altra parte!"
            self.userInOtherGame = "F nella chat, {} è attualmente in un'altra partita. Mi sà che dovrai aspettarlo.".format(self.user)
            self.finishOtherGameFirst = "Aspetta un attimo, {}, sei attualmente in un'altra partita! Finisci quella che stai giocando prima di iniziarne una nuova.".format(self.user)
            self.bothGone = "Oh cavolo. Siete andati tutti e due in altre prartite con altre persone. Tornate quando finite, mi raccomando!"
            self.userWentOffline = "Oh, no! {} è andato offline! Mi sa che non potrai più giocare adesso... :shrug:".format(self.user)
            self.noResponse = "{} non ha risposto. La partita è stata cancellata.".format(self.user)
            self.whosPlaying4 = "Chi vuole giocare?\n3 persone (oltre a {}) devono reagire con ✅ per iniziare la partita.".format(self.user)
            self.noOneWantsToPlay = "Nessuno sembra voler giocare. La partita è cancellata."
            self.whosPlayingUnlimited = "Chi vuole giocare a {}?\nReagisci con ✅ per partecipare alla partita. \n{}, utilizza la stessa reazione, quando tutti sono entrati, per far partire il gioco.".format(self.games[self.game_], self.user)
            self.cancelUnlimited = "Sembra che la persona che inizialmente voleva giocare abbia deciso di lasciarci. La partita è cancellata."
            self.startMaxPlayers = "Il numero massimo di giocatori è stato raggiunto. Iniziamo!!"
            self.premiumCanHaveMore = "I giochi premium possono ospitare fino a {} giocatori! Visita https://patreon.com/CommunityGamesBot/ per saperne di più.".format(self.number)
            self.gameStarting = "{}... La partita stà iniziando!".format(self.user)
            self.needToDM = "{}, ho bisogno di poterti scrivere in privato per iniziare il gioco.\nPer risolvere, vai al menù del server (vicino al nome del server), seleziona 'Impostazioni della Privacy' e abilita 'Permetti messaggi da membri del server'.".format(self.user)

            self.playersTurn = "È il turno di {}!".format(self.user)
            self.playerWon = "{} vince!".format(self.user)
            if type(self.user2) == list: losers = ", ".join(self.user2[:-1]) + " e " + self.user2[-1]
            else: losers = self.user2
            self.playerWonAgainst = "{} vince la partita di {} contro {}!".format(self.user, self.games[self.game_], losers)
            self.draw = "È un pareggio!"
            if type(self.user) == list: people = ", ".join(self.user[:-1]) + " e " + self.user[-1]
            else: people = self.user
            self.endedInDraw = "La partita di {} tra {} è finita in un pareggio!".format(self.games[self.game_], people)
            self.gameWasStopped = "Questa partita è stata terminata manualmente"
            self.error = "Whoops! È successo un errore."
            self.errorStopped = "Whoops! È successo un errore. La partita è stata terminata."
            self.errorWon = "È successo un errore, però, {} vince!".format(self.user)
            
            self.modes = {"comp":"competitiva", "co-op":"cooperativa", "colour":["colori", "colore", "c"], "number":["numeri", "numero", "n"]}

            self.c4HowTo = "Reagisci con il numero corrispondente alla colonna nella quale desideri inserire la tua pedina.\nHai 30 secondi per fare la tua mossa."
            self.c4Timeout = "{} ci ha messo troppo per rispondere. Una colonna a caso è stata selezionata.".format(self.user)
            self.c4Offline = "{} è offline. Una colonna a caso è stata selezionata.".format(self.user)

            self.tttHowTo = "Utilizza la reazione corrispondente allo spazio che vuoi prendere. Hai 30 secondi per fare la tua scelta."
            self.tttTimeout = "{} ci ha messo troppo per rispondere e ha saltato il turno!".format(self.user)

            self.mmWaitForCodes = "Aspettando per la crezione dei codici..."
            self.prepareMakeCode = "Preparati a creare il tuo codice!"
            self.createCode = "Crea il tuo codice di 6 cifre!"
            self.mmTimeLimit = "Hai 20 second per inserire ogni singola parte del codice."
            self.codeFinished = "Codice finito!"
            self.goToChannel = "Spostati sul canale dove la partita è stata iniziata per giocare!"
            self.previousTurns = "Turni precedenti:"
            self.roundNumber = "Turno "
            self.thisTurn = "Questo turno:"
            self.resultsFromTurn = "Risultati dal turno di {}:".format(self.user)
            if self.mode == "colour":
                self.codeType =  "colore"
            else:
                self.codeType = "numero"
            self.mmInfo = """✅ = Il {} è nella posizione corretta\n❔ = Il {} è da qualche altra parte nel codice\n❌ = Il {} non è nel codice""".format(self.codeType, self.codeType, self.codeType)
            self.reactWhenReady = "Reagisci con 👍 quando sei pronto a procedere"
            self.notOverYet = "Non è ancora finito!"
            self.userFinishGameCont = "{} potrebbe aver finito, ma il gioco continua fino a quando entrambi hanno finito!".format(self.user)
            self.gameEndedPossibleWinner = "Il gioco è terminato prematuramente, ma sembra che sia una vittoria per {}!".format(self.user)
            self.gameEndedWinner = "Il gioco è terminato prematuramente, ma vince {}!".format(self.user)
            self.gameEnded = "Il gioco è terminato prematuramente"
            self.noRounds = "Nessun turno è stato completato"
            self.userDidNotComplete = "{} non è riuscito a completare il suo primo turno".format(self.user)

            self.waitForShips = "Aspettando che vengano piazzate le navi..."
            self.preparePlaceShips = "Preparazione per piazzare le navi..."
            if self.shipType == "Aircraft Carrier": self.ship = "la porta aerei"
            elif self.shipType == "Battleship": self.ship = "la nave da battaglia"
            elif self.shipType == "Destroyer": self.ship = "il distruttore"
            elif self.shipType == "Submarine": self.ship = "il sottomarino"
            elif self.shipType == "Patrol Boat": self.ship = "la motovedetta"
            else: self.ship = ""
            self.placingShip = "Piazzare {}".format(self.ship)
            self.positionSetTimeout = "La posizione verrà automaticamente impostata se nessuna correzione viene fatta in 15 secondi"
            self.fleetReady = "Flotta pronta!"
            self.userAiming = "{} sta mirando...".format(self.user)
            self.selectX = "Hai 20 second per scegliere una coordinata x"
            self.selectY = "Hai 20 second per scegliere una coordinata y"
            self.alreadyFiredThere = "Hai già lanciato qua, prova da qualceh altra parte."
            self.firing = "Fuoco..."
            self.hit = "Colpito!"
            self.missed = "Mancato"
            self.sunkShip = "{} ha affondato {} di {}!".format(self.user, self.ship, self.user2)
            self.usersShots = "Colpi di {}:\n".format(self.user)
            self.possibleWinner = "A questo punto, sembra essere vittoria per {}!".format(self.user)
            self.possibleDraw = "A questo punto, sembra essere un pareggio!"

            self.hmEnglishWords = "Attenzione: Le parole selezionate casualmente sono in inglese"
            self.hmModeVote = "In che modalità volete giocare?\nReagisci con :wrestling: per competitiva oppure :handshake: per cooperativa\n\nHai 10 secondi per scegliere una modalità"
            self.calculateResult = "Calcolo risultato..."
            self.voteDraw = "Pari? Sceglierò io allora..."
            if self.mode: self.gameModeSelected = "Selezionata modalità **{}**. Iniziamo!".format(self.modes[self.mode])
            self.hmOnePlayer = "Solo te? Ok."
            self.hereWeGo = "Ok, andiamo!"
            self.incorrectGuesses = "Tentativi scorretti:"
            self.takeAGuess = "{}, prova ad indovinare".format(self.user)
            if self.wordPhrase == "word": self.wordPhrase = "parola"
            elif self.wordPhrase == "phrase": self.wordPhrase = "frase"
            self.hmHowTo = "Scrivi la lettera che pennsi sia nella {}, o la {} intera.\nHai {} secondi per fare un tentativo".format(self.wordPhrase, self.wordPhrase, self.number)
            self.alreadyGuessed = "Hmm, hai già provato quello! Prova qualcos'altro."
            self.invalidLetter = "Uh oh, quella non è una lettera valida! Prova di nuovo."
            self.invalidWord = "Oops, quella non è una valida {}! Prova di nuovo".format(self.wordPhrase)
            self.letterNotInWord = "La lettera {} non è una valida {}".format(self.other, self.wordPhrase)
            self.incorrectWord = "'{}' non è la {}.".format(self.other, self.wordPhrase)
            self.letterAppearsOnce = "La lettera {} appare una nella {}".format(self.other, self.wordPhrase)
            self.letterAppearsTwice = "La lettera {} appare due nella {}".format(self.other, self.wordPhrase)
            self.letterAppears = "La lettera {} appare {} volte nella {}".format(self.other, self.other2, self.wordPhrase)
            self.hmTimeout = "Sei rimasto senza tempo per fare un tentativo!"
            self.failedToGuess = "Non sei riuscito ad indovinare la {}".format(self.wordPhrase)
            self.wordWas = "La {} era: ".format(self.wordPhrase)
            self.youWin = "Hai vinto!"
            if self.other == "1": s1 = ""
            else: s1 = "s"
            if self.other2 == "1": s2 = ""
            else: s2 = "es"
            self.coOpWinStats = "In totale avete fatto {} tentativi per indovinare la {}, con {} tentativi scorretti rimanenti.".format(self.other, self.wordPhrase, self.other2)
            if type(self.user) == list: people = ", ".join(self.user[:-1]) + " e " + self.user[-1]
            else: people = self.user
            if self.other == "1": s = ""
            else: s = "s"
            self.hmCoOpEnd = "{} sono riusciti a trovare la {} in {} tentativi.".format(people, self.wordPhrase, self.other)

            self.yes = "si"
            self.waitForWords = "Aspettando che le persone creino le parole..."
            self.hmSetup = "Qual è la tua parola? Scrivila. Hai un minuto per scegliere."
            self.hmSetupTimeout = "Be', il tuo tempo è finito. Sceglierò io una parola a caso per te...\nPuoi andare nel canale dove la partita è stata iniziata per continuare a giocare."
            self.hmSetupInvalid = "Mi dispiace, ma l'input non è valido. Utilizza solo caratteri alfanumerici inglesi e punteggiatura base."
            self.hmTooLong = "Quella {} è troppo lunga! La lunghezza massima è 100 caratteri".format(self.wordPhrase)
            self.hmTooShort = "Quella {} è troppo corta! La lunghezza minima è 4 caratteri".format(self.wordPhrase)
            self.hmSetupConfirm = "La tua parola è: **{}**\nScrivi 'si' per confermare, o una parola diversa per cambiarla.".format(self.other)
            self.hmSetupConfirmTimeout = "Nessuna risposta? Lo prenderò come un si.\nVai al canale dove la partita è stata creata per continuare a giocare!"
            self.hmSetupComplete = "Ottimo, siamo pronti. Vai al canale dove la partita è stata creata per continuare a giocare!"
            self.hmSetupCancel = "Oh, lascia stare... La partita è stata cancellata."
            self.hmAllSetupsComplete = "Adesso che tutti hanno le loro parole, iniziamo!"
            self.yourTurn = "Tocca a te, {}!".format(self.user)
            self.wordFinished = "Hai finito la parola!"
            if self.other == "1": s1 = ""
            else: s1 = "s"
            if self.other2 == "1": s2 = ""
            else: s2 = "s"
            self.personFinished = "Hai fatto {} tentativi per indovinare la {}, con {} tentativi scorretti rimanenti.\nRimani fino alla fine della partita per i risultati di tutti!".format(self.other, self.wordPhrase, self.other2)

            self.hmeliminated = "Non sei riuscito ad indovinare la parola. Sei stato espulso."
            self.everyoneFinished = "Tutti hanno finito! Sto calcolando i risultati..."
            self.totalAttempts = "Tentativi totali: "
            self.correctAttempts = "Tentativi corretti: "
            self.incorrectAttempts = "Tentativi incorretti: "
            self.score = "Punteggio: "
            self.scoreUnavailable = "-Score unavailable-"
            self.highScore = "Punteggio migliore"


            self.promotitles = [
                "Sembra che ti stiano piacendo molto questi giochi.",
                "Giochi cìda un po' non è vero?",
                "Wow, ti piacono molto questi giochi, vero?",
                "Woah, hai giocato una sacco ultimamente."]
            self.promodesc = [
                "Perchè non valutarmi su [top.gg](https://top.gg/bot/656058788020879370/vote)\nSarebbe molto apprezato :)",
                "Potresti aiutare a far conoscere questo bot [votando.](https://top.gg/bot/656058788020879370/vote)\nSe potessi prendere qualche secondo per farlo sarebbe molto apprezzato.",
                "Hai considerato [diventare un supportatore su patreon?](https://patreon.com/CommunityGamesBot/)\nUna donazione aiuterebbe un sacco ad espandere la copacità di questo bot.",
                "Se hai un po' di resto, perchè non [diventare un supportatore su patreon?](https://patreon.com/CommunityGamesBot/)"]


            self.downtime = "Dammi un attimo, Andrò ofline per un pochino (probabilmente per un aggiornamento). Torno subito!"
            self.comingSoon = "Questo gioco sta per arrivare!\nVuoi giocarci adesso? Diventa un beta tester a https://patreon.com/CommunityGamesBot/"

            self.onlyPremium = "Solo utenti premium possono usare questa opzione!"
            self.becomePremium = "Diventane uno [qui](https://patreon.com/CommunityGamesBot/)"
            self.displaySet = "Icona di {} per Conetti 4 e Tris impostata a {}".format(self.user, self.other)
            self.displaySetDesc = "Se vuoi reimpostare la tua icona a default, utilizza 'cancella' o 'reset' al posto di un emoji"
            self.displayDefault = "L'emoji di {} impostata al predefinito".format(self.user)
            self.noEmojiFound = "Mi dispiace, ma non sono riuscito a trovare quell'emoji in questo server"
            self.enterEmoji = "Perfavore inserire un emoji, esempio:"
            self.invalidRGB = "Valore RGB non valido."
            self.invalidRGBDesc = "Fai attenzione ad usare solo valori interi tra 0 e 255.\nAlternativamente, puoi usare i codici hex (tipo #f42cb1), o nomi dei colori comuni."
            self.invalidHex = "Valore hex non valido."
            self.invalidHexDesc = "Fai attenzione ad utilizzare solo numeri da 0 a 9 e lettere da A a F.\nAlternativamente, puoi usareu un valore RGB (tipo 61, 26, 125), o nomi dei colori comuni."
            self.invalidInput = "Input non valido."
            self.invalidDesc = "Fai attenzione ad inserire un valore RGB valido (tipo 61, 26, 125) o valore hex (tipo #f42cb1), o nomi dei colori comuni."
            self.colourSet = "Il colore di {} impostato a {}".format(self.user, self.other)
            self.colourSetDesc = "Se vuoi reimpostare il tuo colore a default, utilizza 'cancella' o 'reset' al posto di un colore"
            self.colourDefault = "Colore per {} impostato al predefinito".format(self.user)
            self.notWhite = "Non ti preoccupare, è normale per me non apparire bianco, perchè Discord lo tratta come il suo colore di default.\nSe vuoi bianco, ti consiglio invece di usare #fefefe (o 254, 254, 254)."
            self.enterColour = "Perfavore inserire un colore, esempio:"
            self.colours = {"red":"rosso", "orange":"arancione", "gold":"oro", "yellow":"giallo", "green":"verde", "aqua":"acqua", "blue":"blu", "purple":"viola", "violet":"violetto", "magenta":"magenta", "pink":"rosa", "white":"bianco", "gray":"grigio", "black":"nero", "reset":"reset", "clear":"cancella"}


        if self.lang == "French": # Translation by L3mmy
            self.translatorID = 387918981698289674
            # Command Names
            self.c4 = "Puissance 4"
            self.mc4 = "Méga Puissance 4"
            self.ttt = "Morpion"
            self.bs = "bataille navale"
            self.mm = "MasterMind"
            self.hm = "Pendu"
            self.games = {"Connect 4":self.c4, "Mega Connect 4":self.mc4, "Tic Tac Toe":self.ttt, "Battleship":self.bs, "MasterMind":self.mm, "Hangman":self.hm, "":""}
            self.stop = "Stop"
            self.lb = "Classement"
            self.stats = "Statistiques"
            self.disp = "Pion"
            self.colour = "Couleur"
            self.prefix = "Préfix"
            self.language = "Language"
            self.ping = "Ping"
            self.help = "Aide"

            # Utility Commands
            self.ending = "Bien reçu. Je mets fin à la partie momentanément..."
            self.stopped = "Le jeu a été arrêté."
            self.mustBeInGame = "Tu doit être *dans une partie* pour pouvoir l'arrêter!"
            self.okayToStop = "{}, c'est ok si le jeu s'arrête?".format(self.user)
            self.pong = "Pong!"
            self.connection = "Connexion à Discord: "
            self.processDelay = "Délai du processus: "
            self.latency = "Latence totale: "
            self.enterPrefix = "Saisit un préfix, comme cela:"
            self.prefixSet = "Préfix définit à `{}`".format(self.prfx)
            self.prefixTooLong = "Préfix trop long! Il doit faire 8 caractères ou moins!"
            self.askAdminPrefix = "Tu doit avoir la permission 'Gérer le serveur' pour utiliser cette commande. Demande à un admin de changer le préfix."
            self.askAdminLanguage = "Tu doit avoir la permission 'Gérer le serveur' pour utiliser cette commande. Demande à un admin de changer la langue."
            self.setLanguageHeader = "Définir la langue"
            self.setlang = "Langue définit sur Français"
            self.setlangdesc = "Traduit par {}".format(self.other)


            # Help
            self.gamecommands = "Commandes de jeu"
            self.c4shortdesc = "Fait un puissance 4 pour gagner!"
            self.mc4shortdesc = "Puissance 4, avec 4 joueurs!"
            self.bsshortdesc = "Coule le bateau de ton adversaire!"
            self.tttshortdesc = "Fait un 3 à la suite pour gagner!"
            self.mmshortdesc = "Résout le code de ton adversaire!"
            self.hmshortdesc = "Devine les mots et évite d'être pendu!"
            self.moreinfo = "Envoie {}aide (commande) pour avoir plus d'information sur une commande".format(prefix)

            self.misccommands = "Commandes diverses/utiles"
            self.stopshortdesc = "Mets fin à la partie"
            self.lbshortdesc = "T'indique montre le classement"
            self.statsshortdesc = "T'indique les stats de la personne choisi"
            self.pingshortdesc = "Vérifier la latence du bot"
            self.prefixshortdesc = "Définit la langue du bot"
            self.langshortdesc = "Définit la langue du bot"
            self.dispshortdesc = "**(Utilisateurs prémium seulement)** Change la couleur de tes pions pour Puissance 4 et le morpion"
            self.colourshortdesc = "**(Utilisateurs prémium seulement)** Change la couleur pour tout les jeux"
            self.helpshortdesc = "Ca fait ça."

            self.links = "Liens"
            self.patreon = "Patreon"
            self.vote = "Donne un vote sur la liste de Bots Discord"
            self.suggest = "Propose un jeu"
            self.invite = "Invite moi sur ton serveur"
            self.support = "Supporte le serveur"

            self.opponent = "@adversaire"
            self.gamemode = "mode de jeu"
            self.game = "jeu"
            self.command = "commande"
            self.winrateoption = "victoires/ratio"
            self.globallocal = "globale/local"
            self.local = "local"
            self.person = "personne"
            self.newprefix = "nouveau préfix"
            self.emoji= "émoji"
            self.value = "value"
            if type(self.commands) == list: self.canBeTriggeredWith = "Cette commande peut aussi être activée avec '{}' et '{}'".format("', '".join(self.commands[:-1]), self.commands[-1])
            else: self.canBeTriggeredWith = "Cette commande peut aussi être activée avec '{}'".format(self.commands)
            self.bslongdesc = "Les deux joueurs posent leurs bateaux sur une grille de 10x10 secrètement. Les joueurs, à tour de roles, essaye de deviner l'endroit des beateaux, se basant sur leur tour précedent comme référence, Il leur sera montré si c'est touché ou raté. La partie continue tant que quelqu'un n'as pas coulé tout les bateau de son adversaire."
            self.mmlongdesc= "Les deux joueurs vont créer un code pour que l'autre essaye de le deviner. Les joueurs, à tour de roles, vont essayer de deviner la combinaison de l'autre, utilisant les résultats précédents pour les guider. Il leur sera montré quel chose est dans le bon endroit, si c'est la bonne chose mais au mauvaise endroit ou si la chose n'est pas du tout dans le code. La partie continue tant que les deux codes n'ont pas été résolu.\n\nL'argument \"mode de jeu\" est optionel. Il est réglé sur les couleurs si rien n'est entré, mais il est possible de le régler sur \"numéros\", \"n\" ou \"numéro\" pour le régler sur le mode numéro, ou alors \"couleurs\",\"couleur\" or même \"c\", parceque c'est possible :sunglasses:"
            self.c4longdesc = "Choisi une colonne pour lâcher ton pion dedans. Aligner les par 4 - horizontalement, verticalement ou en diagonale - en rangée pour gagner, avant que ton adversaire ne fasse de même"
            self.mc4longdesc = "Même règles que le puissance 4, mais à 4 joueurs.\nChoisi une rangée pour lâcher ton pion dedans. Aligner les par 4 - horizontalement, verticalement ou en diagonale - en rangée, avant que un de tes adversaire ne fasse de même."
            self.tttlongdesc = "Joue à tour de rôle sur une grille de 3x3. Le premier jouer à aligner 3 en rangée - horizontalement, verticalement ou en diagonale - gagne."
            self.hmlongdesc = "Devine le mot sans être pendu, se joue de 1 à 4 joueurs **mais les parties crées par des joueurs premium peuvent avoir jusqu'à 16 joueurs!**\nSi l'argument pour le mode de jeu est vide, tout les joueurs voterons pour le mode qu'il veulents.\nMode coopération: Tout les joueurs travaillent ensemble pour deviner le même mot.\nMode compétition: Chaque joueurs devinent un mot, choisi par un autre joueur, pour gagner il faut deviner le mot en faisant le moins de fautes possibles."
            self.helplongdesc = "Montre toutes les commandes, ou tous les détails d'une commande spécifique."
            self.pinglongdesc = "Te notifie de la latence au moment même du bot."
            self.stoplongdesc = "Après avoir demandé aux autres joueur(s) si ils sont ok avec ça, le jeu au quel tu joue s'arrête.\nLe jeu s'arrête directement si tous les joueurs sont hors ligne. Pratique si jamais quelqu'un à besoin de partir en vitesse."
            self.lblongdesc = "Indique le classement pour le jeu demandé de la même commande, dans tout les servers, ou juste le server dans lequel tu est. Tu peux trier par le nombre de victoires ou même le plus grand ratio de victoire par rapport aux défaites. Tout les arguments sont otionels et l'ordre n'est pas important."
            self.statslongdesc = "Indique les statistiques de la personne choisie. Si personne n'est choisi, tes statistiques seront montré"
            self.prefixlongdesc = "Change le préfix du bot.\nIl doit comporter 8 caractères ou moins et doit être mis par quelqu'un avec la permission 'Gérer le serveur'."
            self.langlongdesc = "Change la langue du bot.\nIl doit comporter 8 caractères ou moins et doit être mis par quelqu'un avec la permission 'Gérer le serveur'."
            self.displongdesc = "Change l'apparence de tes pièces pour Puissance 4, Méga puissance 4 et le Morpion. Fonctionne avec n'importe quel émoji custom (même animé) tant que le bot est dans le serveur avec cet émoji.\nPas Nitro? Pas de problème. Écrit le nom de l'émoji, il sera accepté.\n**Cette fonctionalité peut uniquement être utilisé  par les utilisateurs premium. Deviens en un [içi.](https://patreon.com/CommunityGamesBot)**"
            self.colourlongdesc = "Change la couleur du display lors de ton tour (la petite barre sur le côté) dans tout les jeux? Utilise une value RGB (#ff0000) ou un code Hex (#FFFF00) pour définir la couleur.\n**Cette fonctionalité peut uniquement être utilisé  par les utilisateurs premium. Deviens en un [içi.](https://patreon.com/CommunityGamesBot)**"
            self.thisServer = "Ce serveur"
            self.allServers = "Tout les serveurs"
            self.lbstates = {"This Server":self.thisServer, "All Servers":self.allServers}
            self.allGames = "Tout les jeux"
            self.emptylb = "Il n'y a encore personne sur ce classement!"
            self.emptylb2 = "Sera tu le premier?"
            self.placings = ["1er", "2ème", "3ème", "4ème", "5ème", "6ème", "7ème", "8ème", "9ème", "10ème"]
            self.cantSeePerson = "Je ne peux pas voir cette personne :disappointed_relieved:"
            self.youHaveNoStats = "Tu n'as encore aucune statistiques!"
            self.theyHaveNoStats = "{} n'as pas encore aucune statistiques!".format(self.user)
            self.personsStats = "Statistiques de {}".format(self.user)
            self.wins = "Victoires"
            self.losses = "Défaites"
            self.draws = "Match nuls"
            self.highScores = "Meilleur Score"
            self.played = "Jeux joués"
            self.winRate = "Ratio victoire/défaite"
            self.total = "Total"

            self.addReactions = "Ajouter des réactions"
            self.manageMessages = "Gérer les messages"
            self.readHistory = "Voir les anciens messages"
            self.externalEmoji = "Utiliser des émojis externes"
            self.permissions = {"Add Reactions" : self.addReactions, "Manage Messages" : self.manageMessages, "Read Message History" : self.readHistory, "Use External Emojis" : self.externalEmoji, "":""}

            if type(self.permission) == list:
                needed = []
                for i in self.permission:
                    needed.append(self.permissions[i])
                self.needPerms = "Je peux pas faire ça pour l'instant. J'ai besoin des permissions suivantes:\n- {}\nSi tu veux savoir pourquoi, regarde la FAQ sur le serveur support: https://discord.gg/dVHsMRK".format("\n- ".join(needed))
            elif type(self.permission) == str: self.needPerms = "Je ne peux pas faire cela pour le moment. J'ai besoin de la permission '{}' d'abord.\nSi tu veux savoir pourquoi, regarde la FAQ sur le serveur support: https://discord.gg/dVHsMRK".format(self.permissions[self.permission])
            self.mentionOpponent = "Tu dois aussi mentionner un adversaire, comme ça:\n"
            self.botsCantPlay = "Les bots ne sont pas assez intelligent pour jouer à {}!".format(self.games[self.game_])
            self.cantFindPerson = ":thinking: Je ne trouve pas cette personne dans ce serveur."
            self.cantPlayAgainstSelf = "Tu ne peux pas jouer contre toi même!"
            self.bothPlaying = "Vous êtes déjà entrain de jouer l'un contre l'autre!"
            self.youreAlreadyPlaying = "Tu joue déjà avec quelqu'un d'autre!"
            self.theyreAlreadyPlaying = "{} est déjà dans une autre partie en ce moment!".format(self.user)
            self.bothPlayingElsewhere = "Vous êtes déjà dans des parties différentes!"
            self.theyreOffline = "Il a l'air d'être hors ligne. Essaye quelqu'un d'autre..."
            if self.game_ == "Tic Tac Toe": thing = "au"
            elif self.game_ == "Battleship": thing = "à la"
            else: thing = "à"
            self.reactToStartGame = "{}, es tu prêt à jouer {} {}?\n\nRéagit avec ✅ dans les 3 minutes qui suivent pour jouer, ou la partie sera annulée".format(self.user, thing, self.games[self.game_])
            self.goneElsewhere = "Mais attends... vous deux êtes partie dans une partie dans un autre serveur!"
            self.userInOtherGame = "Rah non, {} est déjà dans un autre partie, j'imagine qu'on va devoir l'attendre...".format(self.user)
            self.finishOtherGameFirst = "Attends {}, t'est dans une autre partie en ce moment! Finie ta partie avant d'en rejoindre une autre".format(self.user)
            self.bothGone = "Oh non. Vous êtes tous partis dans une autre partie avec différente personnes. Revenez quand vous avez finit!"
            self.userWentOffline = "Oh non! {} est hors ligne! J'imagine qu'on peut pas jouer maintenant... :shrug:".format(self.user)
            self.noResponse = "{} n'as pas répondu... La partie à été annulée.".format(self.user)
            self.whosPlaying4 = "Qui veut jouer ?\n3 personnes (autre que {}) doivent réagir avec ✅ pour commencer une partie.".format(self.user)
            self.noOneWantsToPlay = "Personne n'as l'air d'avoir envie de jouer. Partie annulée."
            self.whosPlayingUnlimited = "Qui veux jouer au {}?\nRéagit avec ✅ pour rejoindre la partie.\n{}, utilise la même réaction quand tout le monde est prêt pour lancer la partie.".format(self.games[self.game_].lower(), self.user)
            self.cancelUnlimited = "On dirait que la personne qui a lancé le jeu ne veux plus jouer, partie annulée."
            self.startMaxPlayers = "Nombre maximum de joueurs atteint, lancement du jeu!"
            self.premiumCanHaveMore ="Les parties lancées par les premium peuvent avoir jusqu'à {} participants! Visite https://patreon.com/CommunityGamesBot/ pour en savoir plus.".format(self.number)
            self.gameStarting = "{}... La partie va être lancée!".format(self.user)
            self.needToDM = "{}, j'ai besoin to t'envoyer un message privée pour le jeu.\nPour réparer ce problème, clique sur la flèche à côté du nom du serveur, clique sur 'Paramètrès de sécurité' et active 'Autoriser les messages directs des membres du serveur'.".format(self.user)

            self.playersTurn = "C'est le tour de {}!".format(self.user)
            self.playerWon = "{} à gagné!".format(self.user)
            if type(self.user2) == list: losers = ", ".join(self.user2[:-1]) + " et " + self.user2[-1]
            else: losers = self.user2
            self.playerWonAgainst = "{} a gagné au jeu {} contre {}!".format(self.user, self.games[self.game_], losers)
            self.draw = "Match nul!"
            if type(self.user) == list: people = ", ".join(self.user[:-1]) + " et " + self.user[-1]
            else: people = self.user
            self.endedInDraw = "Le jeu {} entre {} a fini en match nul!".format(self.games[self.game_], people)
            self.gameWasStopped = "Le jeu a été arrêté manuellement"
            self.error = "Oops! Une erreur est servenue."
            self.errorStopped = "Oops! Une erreur est servenue. Le jeu à été arrêté"
            self.errorWon = "Une erreur est survenue mais {} à gagné!".format(self.user)

            self.modes = {"comp":"compétition", "co-op":"coopération", "colour":["couleurs", "couleur", "c"], "number":["numéros", "numéro", "n"]}

            self.c4HowTo = "Réagit avec le numéro de la colonne dans lequel tu veux mettre ton pion.\nTu as 30 secondes pour réfléchir et jouer."
            self.c4Timeout = "{} a pris trop de temps à réagir. Une colonne aléatoire a été choisi".format(self.user)
            self.c4Offline = "{} est hors ligne. Une colonne aléatoire a été choisi.".format(self.user)

            self.tttHowTo = "Utilise la réaction correspondante à l'emplacement que tu veux prendre.\nTu as 30 secondes pour réfléchir et réagir."
            self.tttTimeout = "{} n'as plus de temps! Son tour à été passé.".format(self.user)

            self.mmWaitForCodes = "J'attends que les codes sont crées..."
            self.prepareMakeCode = "Préparez vous à créer vos codes!"
            self.createCode = "Écrivez vos codes de 6 de long!"
            self.mmTimeLimit = "Tu as 20 secondes pour saisit chaque partie individuelle du code."
            self.codeFinished = "Code reçu!"
            self.goToChannel = "Maintenant vas dans le salon dans lequel tu veux jouer!"
            self.needToDM = "{}, je doit pouvoir t'envoyer un message privé pour que tu puisse me dire ton code.\nPour réparer ce problème, vas dans les paramètres de confidentialité du serveur dans la file déroulante et active le paramètre \"Autoriser les messages privés en provenance des membres du serveur\".".format(self.user)
            self.previousTurns = "Tours précedents:"
            self.roundNumber = "Round n°"
            self.thisTurn = "Ce tour:"
            self.resultsFromTurn = "Résultats du tour de {}:".format(self.user)
            if self.mode == "colour":
                self.codeType =  "La couleur"
            else:
                self.codeType = "Ce numéro"
            self.mmInfo = """✅ = {} est correcte et est dans la bonne position\n❔ = {} est autre part d'autre dans le code\n❌ = {} couleur n'est pas dans code""".format(self.codeType, self.codeType, self.codeType)
            self.reactWhenReady = "Réagit avec 👍 quand tu es prêt à continuer"
            self.notOverYet = "Ce n'est pas encore fini!"
            self.userFinishGameCont = "{} a peut-être fini, mais la partie continue tant que vous n'avez pas découvert les deux codes!".format(self.user)
            self.gameEndedPossibleWinner = "Le jeu à été arrête prématurément, mais c'est une victoire pour {}!".format(self.user)
            self.gameEndedWinner = "Le jeu à été arrête prématurément, mais {} a gagné!".format(self.user)
            self.gameEnded = "Le jeu à été arrête prématurément."
            self.noRounds = "Aucun round n'as été fini"
            self.userDidNotComplete = "{} n'as pas fini son premier round".format(self.user)

            self.waitForShips = "En attente que les bateaux sont placés..."
            self.preparePlaceShips = "Je me prépare à placer les bateaux..."
            if self.shipType == "Aircraft Carrier": self.ship = "Porte-Avion"
            elif self.shipType == "Battleship": self.ship = "bateau de guerre"
            elif self.shipType == "Destroyer": self.ship = "Destroyer"
            elif self.shipType == "Submarine": self.ship = "Sous-marin"
            elif self.shipType == "Patrol Boat": self.ship = "bateau de patrouille"
            else: self.ship = ""
            self.placingShip = "Placement du bateau {}".format(self.ship)
            self.positionSetTimeout = "La position va être automatiquement décidée si aucun ajustement n'est fait dans 15 secondes"
            self.fleetReady = "La flotte est prête!"
            self.userAiming = "{} est en train de viser...".format(self.user)
            self.selectX = "Tu as 20 secondes pour sélectionner une position sur l'axe des X"
            self.selectY = "Tu as 20 secondes pour sélectionner une position sur l'axe des Y"
            self.alreadyFiredThere = "Tu as déjà tiré içi, essaye quelque part d'autre!"
            self.firing = "Lancement du missile..."
            self.hit = "Touché!"
            self.missed = "Raté"
            self.sunkShip = "{} a coulé le {} de {}!".format(self.user, self.ship, self.user2)
            self.usersShots = "Les tirs de {}:\n".format(self.user)
            self.possibleWinner = "En ce moment, on dirait que {} va gagner!".format(self.user)
            self.possibleDraw = "En ce moment, on dirait que ça être un match nul!"

            self.hmEnglishWords = "Pour ton information: tout les mots séléctionné sont en Anglais"
            self.hmModeVote = "Quel mode de jeu voulez-vous jouer?\nRéagit avec :wrestling: pour jouer en mode compétition, ou :handshake: pour coopération co-op\n\nVous avez 10 secondes pour voter"
            self.calculateResult = "Calcul des résultats..."
            self.voteDraw = "Égalité? Je vote dans ce cas..."
            if self.mode: self.gameModeSelected = "**{}** mode de jeu choisi. Commençons!".format(self.modes[self.mode].capitalize())
            self.hmOnePlayer = "Seulement toi? D'accord."
            self.incorrectGuesses = "Fautes:"
            self.takeAGuess = "{}, essaye de deviner".format(self.user)
            if self.wordPhrase == "word": self.wordPhrase = "le mot"
            else: self.wordPhrase = "la phrase"
            self.hmHowTo = "Écrit la lettre qui est dans {}, ou dans {}.\nTu as {} secondes pour trouver".format(self.wordPhrase, self.wordPhrase, self.number)	
            self.alreadyGuessed = random.choice(["On dirait", "Whoops,", "Uhh,", "Hmm,"]) + " tu as déjà dit cette lettre! Essaye une autre lettre."
            self.invalidLetter = random.choice(["Oops,", "Whoops,", "Uh oh,", "Hmm,"]) + " ce n'est pas une lettre valide! Réessaye."
            self.invalidWord = random.choice(["Oops,", "Whoops,", "Uh oh,", "Hmm,"]) + " {} n'est pas valide! Réessaye.".format(self.wordPhrase)
            self.letterNotInWord = "La lettre {} n'est pas dans {}".format(self.other, self.wordPhrase)
            self.incorrectWord = "'{}' n'est pas dans {}.".format(self.other, self.wordPhrase)
            self.letterAppearsOnce = "La lettre {} apparait une seul fois dans {}".format(self.other, self.wordPhrase)
            self.letterAppearsTwice = "La lettre {} apparait deux fois dans {}".format(self.other, self.wordPhrase)
            self.letterAppears = "La lettre {} apparait {} fois dans {}".format(self.other, self.other2, self.wordPhrase)
            self.hmTimeout = "Tu n'as plus de temps pour deviner!"
            self.failedToGuess = "Tu n'as pas réussit à deviner {}".format(self.wordPhrase)
            self.wordWas = "L{} était: ".format(self.wordPhrase[1:])
            self.youWin = "Tu as gagné!"
            s1 = ""
            if self.other != 1: s1 = "s"
            s2 = ""
            if self.other2 != 1: s2 = "s"
            self.coOpWinStats = "Tu as prit un total de {} essai{} pour deviner {}, avec {} faute{} en plus.".format(self.other, s1, self.wordPhrase, self.other2, s2)
            if type(self.user) == list: people = ", ".join(self.user[:-1]) + " et " + self.user[-1]
            else: people = self.user
            s = ""
            if self.other != "1": s = "s"
            self.hmCoOpEnd = "{} à réussi à trouver {} - '{}' - avec {} essais{}".format(people, self.wordPhrase, self.other, self.other2, s)

            self.yes = "oui"
            self.waitForWords = "J'attends que les personnes concernés créent des mots..."
            self.hmSetup = "C'est quoi ton mot? Tu as juste à l'écrire et à l'envoyer. Je te laisse une minute pour trouver un mot."	
            self.hmSetupTimeout = "Une minute est passée. Je vais choisir un mot à ta place \nTu peux aller dans le channel où la partie à été lancée."	
            self.hmSetupInvalid = "Je ne comprends pas. Utilise uniquement des caractères basic avec une ponctuation simple"
            self.hmTooLong = "Ce {} est trop long! La longueur maximale est de 100 caractères".format(self.wordPhrase)
            self.hmTooShort = "Ce {} est trop court! La longueur minimale est de 4 caractères".format(self.wordPhrase)
            self.hmSetupConfirm = "Le mot que tu as choisi est: **{}**\nÉcrit 'oui' pour confirmer, ou bien écrit un autre mot si tu veux changer de mot.".format(self.other)
            self.hmSetupConfirmTimeout = "Pas de réponse? Je vais le valider pour toi alors.\nTu peux aller dans le channel où la partie à été lancée"	
            self.hmSetupComplete = "Super, j'ai bien enregistré ton mot. Tu peux aller dans le channel où la partie à été lancée"	
            self.hmSetupCancel = "Oublie ça, la partie a été annulée..."	
            self.hmAllSetupsComplete = "Maintenant que j'ai un mot pour tout le monde, lançons la partie!!"	
            self.yourTurn = "C'est ton tour, {}!".format(self.user)	
            self.wordFinished = "Tu as finit le {}".format(self.wordPhrase)	
            if self.other == "1": s1 = ""	
            else: s1 = "s"	
            if self.other2 == "1": s2 = ""	
            else: s2 = "s"	
            self.personFinished = "Tu as prit {} essai{} pour deviner le {}, avec {} faute{} restantes!\nReste içi pour voir les résultats finaux".format(self.other, s1, self.wordPhrase, self.other2, s2)
            self.hmeliminated = "Tu n'as pas réussi à deviner le mot. Tu as été éliminé."	
            self.everyoneFinished = "La partie est finie! Je calcule les résultats..."	
            self.totalAttempts = "Nombre total d'essais: "	
            self.correctAttempts = "Essais correct: "	
            self.incorrectAttempts = "Fautes: "
            self.score = "Score: "
            self.scoreUnavailable = "-Score inconnu-"
            self.highScore = "Meilleur Score: "


            self.promotitles = ["Hey, tu a l'air de bien t'amuser avec la panoplie des jeux disponibles.", "T'as joué à pas mal de jeux, hein?", "Wow, t'adore vraiment ces jeux, hein?", "Woah, t'as joué beaucoup de parties récemment."]
            self.promodesc = ["Pourquoi tu voterais pas pour moi sur [top.gg?](https://top.gg/bot/656058788020879370/vote)\nJe serais super content :)", "Est-ce que tu as pensé à [devenir un patreon?](https://patreon.com/CommunityGamesBot)\De l'aide serait la bienvenue pour faire encore mieux!", "Tu peux m'aider en [votant pour moi.](https://top.gg/bot/656058788020879370/vote)\nSi tu prends un peu de temps pour le faire, ca serait vraiment apprécié! :)", "Si tu as un peu de monnaie de côté, pourquoi ne pas [devenir un patreon?](https://patreon.com/CommunityGamesBot) même la plus petite des aides ferait le plus grands des bien pour que je m'améliore :D"]


            self.onlyPremium = "Seul les membres premium on le droit de faire cela!"	
            self.becomePremium = "Deviens en un [içi](https://patreon.com/CommunityGamesBot/)"	
            self.displaySet = "Définit ton pion pour Puissance 4 et le Morpion pour {}, en ce moment {}".format(self.user, self.other)	
            self.displaySetDesc = "Si jamais tu veux remettre ton pion à zéro, utilise 'reset' à la place d'un emoji"	
            self.displayDefault = "Pion pour {} remit à zéro".format(self.user)	
            self.noEmojiFound = "Désolé, mais je ne parvient pas à trouver cet émoji dans ce serveur"
            self.enterEmoji = "Saisit une émoji, comme cela:"
            self.invalidRGB = "Valeur RGB pas valide."	
            self.invalidRGBDesc = "Utilise uniquement des numéros entre **0** et **255**.\nSinon, tu peux utiliser un code hex (comme #f42cb1) ou même le nom d'une couleur."
            self.invalidHex = "Valeur hex pas valide."	
            self.invalidHexDesc = "Utilise uniquement des numéros de **0** à **9** et des lettres de **a** à **f**.\nSinon, tu peux utiliser un valeur RGB (comme 244, 44, 177 ) ou même le nom d'une couleur."	
            self.invalidInput = "Ce que tu as envoyé est invalide."	
            self.invalidDesc = "Soit sûr que tu ait envoyé une valeur RGB valide (comme 244, 44, 177) ou une valueur Hex (comme #f42cb1)ou même le nom d'une couleur."	
            self.colourSet = "Couleur pour {} définit à {}".format(self.user, self.other)	
            self.colourSetDesc = "Si jamais tu veut mettre la couleur du display comme celle d'avant, utilise 'reset' à la place de la couleur"	
            self.colourDefault = "Couleur pour {} remit à zéro".format(self.user)	
            self.notWhite = "Pas de panique, c'est normal que ça n'apparait pas blanc, c'est parceque Discord le traite comme une valeur de base.\nSi tu veux du blanc, utilise #fefefe (ou 254 ,254 , 254) à la place."	
            self.enterColour = "Saisit une couleur, comme cela:"
            self.colours = {"red":"rouge", "orange":"orange", "gold":"or", "yellow":"jaune", "green":"vert", "aqua":"cyan", "blue":"bleu", "purple":"pourpre", "violet":"violet", "magenta":"magenta", "pink":"rose", "white":"blanc", "gray":"gris", "black":"noir", "reset":"reset", "clear":"nettoyer"}	
            
            self.downtime = "Attends un peu, je vais devoir me déconnecter pour un petit moment (sûrement une mise à jour). Je serait de retour dans quelques minutes!"	
            self.comingSoon = "Ce jeu arrive bientôt!\nTu veux y jouer maintenant? Devient un beta tester en cliquant sur le lien! https://patreon.com/CommunityGamesBot/"
        
        
        if self.lang == "Chinese": # Translation by rubberduckie0701
            self.translatorID = 629082225014734851
            # Command Names
            self.c4 = "连接4"
            self.mc4 = "巨型连接4"
            self.ttt = "井字游戏"
            self.bs = "战舰"
            self.mm = "策划者"
            self.hm = "Man子手"
            self.games = {"Connect 4":self.c4, "Mega Connect 4":self.mc4, "Tic Tac Toe":self.ttt, "Battleship":self.bs, "MasterMind":self.mm, "Hangman":self.hm, "":""}
            self.stop = "停"
            self.lb = "排行榜"
            self.stats = "统计"
            self.ping = "呯"
            self.prefix = "前缀"
            self.disp = "显示"
            self.colour = "颜色"
            self.language = "语言"
            self.help = "帮助"

            # Utility Commands
            self.ending = "好吧。游戏即将结束..."
            self.stopped = "游戏已被停止。"
            self.mustBeInGame = "您要先*在*一场游戏里才可以停止它！"
            self.okayToStop = "{}, 可以停止游戏吗？".format(self.user)
            self.pong = "嗙！"
            self.connection = "跟Discord 的连接："
            self.processDelay = "处理延迟："
            self.latency = "全面延迟："
            self.prefixSet = "前缀已被设置成`{}`".format(self.prfx)
            self.prefixTooLong = "前缀太长啦！不可以超过8个字符。"
            self.enterPrefix = "请键入一个前缀，像这样："
            self.askAdminPrefix = "你需要有‘管理服务器’权限才能用这个命令。去问一位管理员来改变前缀吧。"
            self.askAdminLanguage = "你需要有‘管理服务器’权限才能用这个命令。去问一位管理员来改变语言吧。"
            self.setLanguageHeader = "设置语言"
            self.setlang = "语言已被设置为简体中文"
            self.setlangdesc = "被 {} 翻译".format(self.other)

            # Help
            self.gamecommands = "游戏指令"
            self.c4shortdesc = "四连一串来赢！"
            self.mc4shortdesc = "连接4，为四位玩家！"
            self.bsshortdesc = "击沉对手的船!"
            self.tttshortdesc = "三连一串来赢！"
            self.mmshortdesc = "破解对手的代码！"
            self.hmshortdesc = "在你被吊前猜对字！"
            self.moreinfo = "键入{}help（命令）以查看有关命令的更多信息".format(self.prefix)

            self.misccommands = "程序命令"
            self.stopshortdesc = "结束你正在玩的游戏"
            self.lbshortdesc = "为你展示排行榜"
            self.statsshortdesc = "查看被选玩家的统计"
            self.pingshortdesc = "查看机器人的等待延迟时间"
            self.prefixshortdesc = "更改机器人的前缀"
            self.langshortdesc = "更改机器人的语言"
            self.dispshortdesc = "（只为高级用户）改变你在连接4和井字游戏里的样子！"
            self.colourshortdesc = "（只为高级用户）改变你在所有游戏中的显示颜色。"
            self.helpshortdesc = "做这个，当然啦"

            self.links = "链接"
            self.patreon = "Patreon"
            self.vote = "在 Discord Bot 页面上为 Community Games 投张票"
            self.suggest = "建议一个新游戏"
            self.invite = "把我邀请到你的服务器里"
            self.support = "支援服务器"

            self.opponent = "@对手"
            self.gamemode = "游戏模式"
            self.game = "游戏"
            self.command = "命令"
            self.winrateoption = "胜/率"
            self.globallocal = "全球/本地"
            self.local = "本地"
            self.person = "人"
            self.newprefix = "新前缀"
            self.emoji = "表情符号"
            self.value = "值"
            if type(self.commands) == list: self.canBeTriggeredWith = "也可以使用'{}'或'{}'来触发此命令。".format("', '".join(self.commands[:-1]), self.commands[-1])
            else: self.canBeTriggeredWith = "也可以使用'{}'来触发此命令。".format(self.commands)
            self.bslongdesc = "两位玩家会秘密的在一张10x10的网格上安排ta们的船只位置。玩家们会轮流猜对手船只的位置。Ta们会看见船有没有被打到。游戏会一直进行到一位玩家击沉了另外一位的所有船只。"
            self.mmlongdesc= "两位玩家将为彼此创建代码。以先前轮流的结果来参考，ta们要轮流猜对手的代码。然后ta们会看见ta们猜的数字是在对的地方，应该在别的地方还是完全不在代码里。游戏会继续到两位玩家都解决了代码。\n\n参数‘游戏模式’是可选的。如果你没有写它游戏会默认到颜色模式，但是如果你想玩数字模式，你可以键入“数字”或“n”，或键入“颜色”或“c”，因为你可以。"
            self.c4longdesc = "选一行把你的棋放进去。将它们堆叠在一起来一连四个。横着竖着斜着都行-在你的对手连到四个之前你就赢了。"
            self.mc4longdesc = "和连接4的规矩一样，但是有四位玩家。\n选一行把你的棋放进去。将它们堆叠在一起来一连四个。横着竖着斜着都行-在你的对手们连到四个之前你就赢了。"
            self.tttlongdesc = "轮流占住在一张3x3网格上的正方形。第一位可以连到3个正方形的人-横着竖着斜着都行-就赢了。"
            self.hmlongdesc = "在你被吊前猜对字。为1-4玩家，可是**高级版游戏可以有到16玩家。**\n如果你没有填入一个游戏模式参数，玩家们将会投票选择游戏模式。\n团队模式：所有玩家轮流帮助彼此来猜对一个从英文字典里随机抽出的字。\n竞争模式：所有玩家自己选一个字，这个字会被传给别的玩家让他们来猜。第一位以最少错误尝试次数猜对字的玩家就会获胜。"
            self.helplongdesc = "为你显示所有命令，或特定命令的所有详细信息。"
            self.pinglongdesc = "发给你机器人当前的延迟时间。"
            self.stoplongdesc = "在询问其他玩家后，你所在的游戏将提前结束。 如果所有其他玩家都离线，游戏会立即结束。 如果有人突然需要离开挺有用的。"
            self.lblongdesc = "用同一个命令显示在所有服务器中或仅在您所在的服务器中请求的游戏的排行榜。你可以按最多获胜次数或最高获胜率对排行榜进行排序。 所有参数都是可选的，顺序无关紧要。"
            self.statslongdesc = "显示所选玩家的统计信息。 如果未选择任何人，它将显示你自己。"
            self.prefixlongdesc = "在这个服务器里改变机器人的前缀。\n前缀不得超过8个字符，而且必须要是被一位有‘管理服务器’权限的人来设置。"
            self.langlongdesc = "在这个服务器里改变机器人的语言。\n语言必须是被一位有‘管理服务器’权限的人来设置。"
            self.displongdesc = "改变你的棋子在连接4，巨型连接4和井字游戏里的样子。任何的自定义表情符号（包括动画表情符号），只要机器人是在那个服务器里就行。\n没有Nitro？没问题。键入表情符号的名字就可以了。\n**这个功能只有高级用户才能用。在[这里](https://patreon.com/CommunityGamesBot)成为一位。**"
            self.colourlongdesc = "改变你在所有游戏里的显示颜色（侧面的颜色小条）。使用RGB值或十六进制代码进行设置。\n**这个功能只有高级用户才能用。在[这里](https://patreon.com/CommunityGamesBot)成为一位。**"
            self.thisServer = "该服务器"
            self.allServers = "所有服务器"
            self.lbstates = {"This Server":self.thisServer, "All Servers":self.allServers}
            self.allGames = "所有游戏"
            self.emptylb = "现在还没有人在这个牌行榜上！"
            self.emptylb2 = "你会是第一位吗？"
            self.placings = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th"]
            self.cantSeePerson = "我看不见那位... "
            self.youHaveNoStats = "你还没有任何统计呢！"
            self.theyHaveNoStats = "{}还没有任何统计呢！".format(self.user)
            self.personsStats = "{}的统计".format(self.user)
            self.wins = "胜局"
            self.losses = "输局"
            self.draws = "平手"
            self.highScores = "高分"
            self.played = "玩过的游戏"
            self.winRate = "胜率"
            self.total = "统计"

            self.addReactions = "添加反应"
            self.manageMessages = "管理消息"
            self.readHistory = "阅读消息历史"
            self.externalEmoji = "使用外部表情符号"
            self.permissions = {"Add Reactions" : self.addReactions, "Manage Messages" : self.manageMessages,
                                "Read Message History" : self.readHistory, "Use External Emojis" : self.externalEmoji, "":""}

            if type(self.permission) == list:
                needed = []
                for i in self.permission:
                    needed.append(self.permissions[i])
                self.needPerms = "我现在还做不到。我需要以下权限：\n- {}\n如果你想知道为什么，看一看在支援服务器上的常见问题解答，在https://discord.gg/dVHsMRK".format("\n- ".join(needed))
            elif type(self.permission) == str:
                self.needPerms = "我现在还做不到。我需要'{}'权限。\n如果你想知道为什么，看一看在支援服务器上的常见问题解答，在https://discord.gg/dVHsMRK".format(self.permissions[self.permission])
            self.mentionOpponent = "你需要提及一位对手，像这样：\n"
            self.botsCantPlay = "机器人们不够聪明，玩不了{}!".format(self.games[self.game_])
            self.cantFindPerson = "嗯，我好像在这个服务器里找不到那位"
            self.cantPlayAgainstSelf = "你不能自己跟自己玩啊！"
            self.bothPlaying = "你们两个已经正在跟对方玩着哪！"
            self.youreAlreadyPlaying = "你正在跟别人一起玩啊！"
            self.theyreAlreadyPlaying = "{} 现在还正在另一场游戏里！".format(self.user)
            self.bothPlayingElsewhere = "你们两个正在另一个地方玩游戏啊！"
            self.theyreOffline = "Ta好像不在线。试试别人吧"
            self.reactToStartGame = "{}，你准备好玩 {} 了吗？\n\n在接下来的3分钟内用✅进行反应以开始游戏，否则它将被取消。".format(self.user, self.games[self.game_])
            self.goneElsewhere = "哦，等一下... 你们两个已经再别的地方开始一场游戏啦！"
            self.userInOtherGame = "哎呀，{} 现在已在另一场游戏里了。我猜我们要等ta喽。".format(self.user)
            self.finishOtherGameFirst = "等一下，{}, 你现在还在另一场游戏里呢！玩儿完那一场再加入其他的。".format(self.user)
            self.bothGone = "哦，亲爱的。你们两个都跟别人开始了其他的游戏。玩完了再回来吧！"
            self.userWentOffline = "哦，不！{}刚下线了！我猜我们玩不了了... :shrug:".format(self.user)
            self.noResponse = "{} 没有反应。游戏已被取消。".format(self.user)
            self.whosPlaying4 = "谁想玩？\n要开始游戏，（除了{}）3位玩家需要用✅进行反应。".format(self.user)
            self.noOneWantsToPlay = "好像没有别人想要玩。游戏已被取消。"
            self.whosPlayingUnlimited = "谁想玩？\n用✅反应来加入游戏。\n{}，用大家开始游戏时候的都用的那个反应来开始游戏。".format(self.user)
            self.cancelUnlimited = "看起来开始游戏的那个人不想玩了。游戏已被取消。"
            self.startMaxPlayers = "已达到最多玩家人数。 让我们开始游戏吧！"
            self.premiumCanHaveMore = "高级游戏里可以有{}位玩家！访问https://patreon.com/CommunityGamesBot/来了解更多信息。"
            self.gameStarting = "{}... 游戏要开始了！".format(self.user)
            self.needToDM = "{},你需要给我私聊你的权限我才能帮你准备好游戏。\n来解决此问题，请转到服务器下拉菜单（服务器名称旁边），选择‘私隐设置’然后启用‘允许服务器成员直接向您发起私聊’。".format(self.user)

            self.playersTurn = "轮到{}了！".format(self.user)
            self.playerWon = "{}赢了！".format(self.user)
            if type(self.user2) == list: losers = "，".join(self.user[:-1]) + "和" + self.user[-1]
            else: losers = self.user2
            self.playerWonAgainst = "{}在{}游戏里胜过了{}！".format(self.user, self.games[self.game_], losers)
            self.draw = "是平手！"
            if type(self.user) == list: people = ", ".join(self.user[:-1]) + "和" + self.user[-1]
            else: people = self.user
            self.endedInDraw = "{}的{}游戏以打平手的结果结束了！".format(people, self.game)
            self.gameWasStopped = "这场游戏以被手动停止"
            self.error = "哎呀！发生了错误。"
            self.errorStopped = "哎呀！发生了错误。游戏已被停止。"
            self.errorWon = "发生了一个错误，但是，{}赢了！".format(self.user)

            self.modes = {"comp":"竞争", "co-op":"团队", "colour":["颜色", "c"], "number":["数字", "n"]}

            self.c4HowTo = "在你要使用的行下，用对应的数字做出反应。\n你有30秒来采取行动"
            self.c4Timeout = "{}用了太长的时间来回答。一个随机行被选择了。".format(self.user)
            self.c4Offline = "{}下线了。一个随机的行被选择了。".format(self.user)

            self.tttHowTo = "使用与您想要的格子对应的反应。 您有30秒的选择时间"
            self.tttTimeout = "{}花太长时间啦！Ta的回合被跳过了。".format(self.user)

            self.mmWaitForCodes = "正在等待代码被创建..."
            self.prepareMakeCode = "准备创建你的代码！"
            self.createCode = "创建你的6位代码！"
            self.mmTimeLimit = "你有20秒的时间输入代码的每个部分。"
            self.codeFinished = "代码完成了！"
            self.goToChannel = "现在去游戏开始的频道！"
            self.previousTurns = "先前回合："
            self.roundNumber = "回合"
            self.thisTurn = "此回合："
            self.resultsFromTurn = "{}轮流的结果：".format(self.user)
            if self.mode == "颜色":
                self.mmInfo =  "✅ = 正确的颜色在正确的位置\n❔ = 这个颜色在代码里别的位置\n❌ = 这个颜色不在代码里"
            else:
                self.mmInfo = "✅ = 正确的数字在正确的位置\n❔ = 这个数字在代码里别的位置\n❌ = 这个数字不在代码里"
            self.reactWhenReady = "你准备好继续时用👍反应"
            self.notOverYet = "还没有结束！"
            self.userFinishGameCont = "{}可能结束了，但是你们两个都结束时游戏才会结束！".format(self.user)
            self.gameEndedPossibleWinner = "游戏提前结束了，但是看起来{}赢了！".format(self.user)
            self.gameEndedWinner = "游戏提前结束了，但是{}赢了！".format(self.user)
            self.gameEnded = "游戏提前结束了"
            self.noRounds = "没有回合被完成"
            self.userDidNotComplete = "{}没有机会来完成第一轮回合".format(self.user)

            self.waitForShips = "等待船只被植入..."
            self.preparePlaceShips = "准备放置船只..."
            if self.shipType == "Aircraft Carrier": self.ship = "航空母舰"
            elif self.shipType == "Battleship": self.ship = "战舰"
            elif self.shipType == "Destroyer": self.ship = "驱逐舰"
            elif self.shipType == "Submarine": self.ship = "潜艇"
            elif self.shipType == "Patrol Boat": self.ship = "巡逻艇"
            else: self.ship = ""
            self.placingShip = "放置{}".format(self.ship)
            self.positionSetTimeout = "如果15秒内你没有反应我会随便选一个位置。"
            self.fleetReady = "舰队准备好了！"
            self.userAiming = "{} 正在瞄准...".format(self.user)
            self.selectX = "你有20秒来选择一个x坐标"
            self.selectY = "你有20秒来选择一个y坐标"
            self.alreadyFiredThere = "你已经炸过那里了，试试其他的地方吧。"
            self.firing = "正在发射..."
            self.hit = "打中了！"
            self.missed = "没打中。"
            self.sunkShip = "{}沉没了{}的{}！".format(self.user, self.user2, self.ship)
            self.usersShots = "{}的炸：\n".format(self.user)
            self.possibleWinner = "现在看起来是{}赢了！".format(self.user)
            self.possibleDraw = "看起来你们打了个平手！"

            self.hmEnglishWords = "请注意：被机器人随机选择的字都是英文的。" 
            self.hmModeVote = "你想玩哪一个游戏模式？\n用:wrestling:反应来为竞争模式投票，或用:handshake:为团队模式。\n\n你有十秒钟的投票时间。"
            self.calculateResult = "计算结果..."
            self.voteDraw = "平局？那我也投一票..."
            if self.mode: self.gameModeSelected = "**{}** 模式被选了。我们开始吧！".format(self.modes[self.mode])
            self.hmOnePlayer = "只有你？那好吧。"
            self.incorrectGuesses = "猜错的："
            self.takeAGuess = "{}，猜猜".format(self.user)
            if self.wordPhrase == "word": self.wordPhrase = "单词"
            else: self.wordPhrase = "短语"
            self.hmHowTo = "键入一位你觉得在这个{}里的字符，或者键入整个{}。\n你有{}秒的时间来猜".format(self.wordPhrase, self.wordPhrase, self.wordPhrase)
            self.alreadyGuessed = "嗯，你已经猜过那个啦！试试其他的吧。"
            self.invalidLetter = "呃，那个字符是无效的！再试试吧。"
            self.invalidWord = "哎呀，那个{}是无效的！再试试吧。".format(self.wordPhrase)
            self.letterNotInWord = "字符{}不在此{}里".format(self.other, self.wordPhrase)
            self.incorrectWord = "‘{}’不是{}。".format(self.other, self.wordPhrase)
            self.letterAppearsOnce = "{}在此{}里出现一次".format(self.other, self.wordPhrase)
            self.letterAppearsTwice = "{}在此{}里出现两次".format(self.other, self.wordPhrase)
            self.letterAppears = "{}在此{}里出现{}次".format(self.other, self.wordPhrase, self.other2)
            self.hmTimeout = "你没时间啦！"
            self.failedToGuess = "您没有猜对{}".format(self.wordPhrase)
            self.wordWas = "那{}是：".format(self.wordPhrase)
            self.youWin = "你赢啦！"
            self.coOpWinStats = "你们总共一起尝试了{}次就猜到了次{}，还剩下{}次可以猜错的机会。".format(self.other, self.wordPhrase, self.other2)
            if type(self.user) == list: people = ", ".join(self.user[:-1]) + "和" + self.user[-1]
            else: people = self.user
            self.hmCoOpEnd = "{}尝试了{}次，成功的猜到了{}！".format(people, self.other, self.wordPhrase)

            self.yes = "是"
            self.waitForWords = "等待其他玩家创建他们的字..."
            self.hmSetup = "你的单词/短语是什么？键入它就行了。你有一分钟来决定。"
            self.hmSetupTimeout = "你的分钟结束了。我为你随便选一个单词吧...\n你现在可以去此游戏开始的频道里了。"
            self.hmSetupInvalid = "对不起，那是无效的。 你只可以使用英文字母数字字符和基本标点符号"
            self.hmTooLong = "{}太长了！最多100个字符".format(self.wordPhrase)
            self.hmTooShort = "{}太短了！最少4个字符".format(self.wordPhrase)
            self.hmSetupConfirm = "你的{}是：**{}**\n键入'是'来确认，键入另一个（单词/短语）如果你想要改变它。".format(self.wordPhrase, self.other)
            self.hmSetupConfirmTimeout = "没反应？那我就替你确认咯。\n现在去游戏开始的频道去玩吧！"
            self.hmSetupComplete = "很好，你都准备好了。去游戏开始的频道去玩吧！"
            self.hmSetupCancel = "哦，算了...游戏已经被结束了。" 
            self.hmAllSetupsComplete = "现在大家都准备好了，我们开始吧！"
            self.yourTurn = "{}，到你了！".format(self.user)
            self.wordFinished = "你猜到{}了！".format(self.wordPhrase)
            self.personFinished = "你尝试了{}次来猜这个{}，还剩下{}次可以猜错的机会！\n再呆一会你就可以看到别人的结果啦！".format(self.other, self.wordPhrase, self.other2)

            self.hmeliminated = "你没猜到这个（单词/短语）。 您已被淘汰。"
            self.everyoneFinished = "大家都好了！正在计算结果..."
            self.totalAttempts = "总尝试次数："
            self.correctAttempts = "正确尝试次数："
            self.incorrectAttempts = "错误尝试次数："
            self.score = "得分"
            self.scoreUnavailable = "-Score unavailable-"
            self.highScore = "High Score: "


            self.promotitles = [
                "嗨，你好像挺喜欢这些游戏的。",
                "你玩这些还玩的还挺多，对吧？",
                "哇，你真的很喜欢这些游戏，对吧？",
                "哇，你最近玩了很多游戏呢。"]
            self.promodesc = [
                "你有考虑[当我的patreon](https://patreon.com/CommunityGamesBot)吗？\n那会将有助于扩展这位机器人以获得更多功能。",
                "如果你有几块零钱的话，不妨[成为我的patreon](https://patreon.com/CommunityGamesBot)?\n就算是最小的",
                "你可以去[为它投票](https://top.gg/bot/656058788020879370/vote)来帮这个机器人！\n如果你可以因此奉献几秒钟的时间，我会很感激的。",
                "不妨去 [top.gg](https://top.gg/bot/656058788020879370/vote) 给我投个票吧？\n我会很感激的。"]

            self.onlyPremium = "只有高级用户才能用这个功能！"
            self.becomePremium = "在[这里](https://patreon.com/CommunityGamesBot/)成为一位"
            self.displaySet = "{}的连接4和井字游戏显示已被改成{}".format(self.user, self.other)
            self.displaySetDesc = "如果你想把显示改回成默认的，用‘清除’或‘重设’，而不是用表情符号。"
            self.displayDefault = "为{}的显示已被设为默认".format(self.user)
            self.noEmojiFound = "抱歉，我在这个服务器里找不到那个表情符号。"
            self.invalidEmoji = "抱歉，你不能用那个表情符号"
            self.enterEmoji = "请键入一个表情符号，像这样："
            self.invalidRGB = "RGB值无效。"
            self.invalidRGBDesc = "确保只你使用了0到255之间的整数。\n或者，你可以使用十六进制代码（例如＃f42cb1）"
            self.invalidHex = "十六进制值无效。"
            self.invalidHexDesc = "确保只你使用了0-9和a-f的字符。\n或者，你可以使用RGB值（例如61、26、125）"
            self.invalidInput = "输入无效。"
            self.invalidDesc = "确保你输入了有效的RGB（例如61、26、125）或十六进制值（例如＃f42cb1）"
            self.colourSet = "{}的颜色已被设置成{}".format(self.user, self.other)
            self.colourSetDesc = "如果你想把你的显示颜色改回成默认颜色，用'清除'或'重设'，而不是一个颜色值。"
            self.colourDefault = "{}的颜色已被设为默认".format(self.user)
            self.enterColour = "请键入一个颜色，像这样："
            self.notWhite = "不用担心，它看起来不纯白是正常的，因为Discord会把它看成默认值。如果你想要白色，我会推荐#fefefe。\n如果你想把显示颜色改回成默认的，用‘清除’或‘重设’，而不是用颜色。"
            self.colours = {"red":"红", "orange":"橘", "gold":"金", "yellow":"黄", "green":"绿", "aqua":"青", "blue":"蓝", "purple":"紫", "violet":"紫罗兰", "magenta":"品红", "pink":"粉", "white":"白", "gray":"灰", "black":"黑", "reset":"重设", "clear":"清除"}

            self.downtime = "等一下，我会停机一小段时间（估计是要更新）。我几分钟就会回来！"
            self.comingSoon = "该游戏即将推出！\想现在就玩吗？ 在https://patreon.com/CommunityGamesBot/成为Beta测试人员" 


        if self.lang == "Russian": # Translation by Plida
            self.translatorID = 640872118107504650
            # Command Names
            self.c4 = "Четыре в ряд"
            self.mc4 = "Мега Четыре в ряд"
            self.ttt = "Крестики-нолики"
            self.bs = "Морской бой"
            self.mm = "Быки и Коровы"
            self.hm = "Виселица"
            self.games = {"Connect 4":self.c4, "Mega Connect 4":self.mc4, "Tic Tac Toe":self.ttt, "Battleship":self.bs, "MasterMind":self.mm, "Hangman":self.hm, "":""}
            self.stop = "Стоп"
            self.lb = "Доска лидеров"
            self.stats = "Статистика"
            self.ping = "Пинг"
            self.prefix = "Префикс"
            self.disp = "Дисплей"
            self.colour = "Цвет"
            self.language = "Язык"
            self.help = "Помощь"

            # Utility Commands
            self.ending = "Понял. Завершаю игру..."
            self.stopped = "Игра была остановлена."
            self.mustBeInGame = "Тебе нужно находиться *в* игре, перед тем как её останавливать!"
            self.okayToStop = "{}, не против остановки игры?".format(self.user)
            self.pong = "Понг!"
            self.connection = "Подсоединение к Discord: "
            self.processDelay = "Задержка процесса: "
            self.latency = "Общая задержка: "
            self.enterPrefix = "Пожалуйста, выберите префикс, например:"
            self.prefixSet = "Префикс был изменён на `{}`".format(self.prfx)
            self.prefixTooLong = "Слишком длинный префикс! Он должен быть не больше 8 символов."
            self.askAdminPrefix = "Для использования этой команды у Вас должно быть разрешение 'Управление Сервером'. Попросите администратора изменить префикс."
            self.askAdminLanguage = "Для использования этой команды у Вас должно быть разрешение 'Управление Сервером'. Попросите администратора изменить язык."
            self.setlang = "Выбран русский язык"
            self.setlangdesc = "Переведено {}".format(self.other)
            self.setLanguageHeader = "Выбор языка"

            # Help
            self.gamecommands = "Игровые команды"
            self.c4shortdesc = "Поставьте 4 в ряд, чтобы выиграть!"
            self.mc4shortdesc = "4 в ряд, для 4 игроков!"
            self.bsshortdesc = "Потопите корабли своего оппонента!"
            self.tttshortdesc = "Поставьте 3 свой фигуры в ряд, чтобы выиграть!"
            self.mmshortdesc = "Решите код своего оппонента!"
            self.hmshortdesc = "Отгадайте слово, чтобы Вас не повесили!"
            self.moreinfo = "Напечатайте {}помощь [команда], чтобы увидеть больше информации о команде".format(self.prefix)

            self.misccommands = "Разное/Утилиты"
            self.stopshortdesc = "Заканчивает игру, в которой Вы находитесь"
            self.lbshortdesc = "Показывает доск(у/и) лидеров"
            self.statsshortdesc = "Показывает статистику выбранного человека"
            self.pingshortdesc = "Показывает задержку бота"
            self.prefixshortdesc = "Изменяет префикс бота"
            self.langshortdesc = "Изменяет язык бота"
            self.dispshortdesc = "**(Только Премиум пользователи)** Поменять Ваш вид в Четыре в ряд и Крестики-нолики"
            self.colourshortdesc = "**(Только Премиум пользователи)** Поменять Ваш отображаемый цвет для всех игр"
            self.helpshortdesc = "Делает это, duh"

            self.links = "Ссылки"
            self.patreon = "Патреон"
            self.vote = "Проголосуйте за нас в Discord Bot List"
            self.suggest = "Предложите новую игру"
            self.invite = "Пригласите меня на ваш сервер"
            self.support = "Техническая поддержка"

            self.opponent = "@оппонент"
            self.gamemode = "игровой режим"
            self.game = "игра"
            self.command = "команда"
            self.winrateoption = "победы/процент"
            self.globallocal = "глобальный/локальный"
            self.local = "локальный"
            self.person = "человек"
            self.newprefix = "новый префикс"
            self.emoji= "эмоджи"
            self.value = "значение"
            if type(self.commands) == list: self.canBeTriggeredWith = "Эта команда также может быть запущена с помощью '{}' и '{}'".format("', '".join(self.commands[:-1]), self.commands[-1])
            else: self.canBeTriggeredWith = "Эта команда также может быть запущена с помощью '{}'".format(self.commands)
            self.bslongdesc = "Два игрока тайно ставят свои корабли на поле 10х10. Игроки по очереди угадывают местоположение указанных кораблей, используя в качестве ориентира результаты предыдущих ходов. Затем им будет показано, попали ли они в корабль или промазали. Игра продолжается, пока кто-то не потопит все корабли другого игрока."
            self.mmlongdesc= "Два игрока создают код для друг друга. Игроки по очереди отгадывают коды, опираясь на результаты предыдущих ходов. Затем будет показано, в правильном ли месте знак, он где-то в другом месте кода, или его вообще нет в коде. Игра продолжается до тех пор, пока оба игрока полностью не решат свои коды.\nАргумент 'игровой режим' не обязателен. По умолчанию будут выбраны цвета, если Вы ничего не ввели. Но Вы можете ввести \"числа\", \"ч\", \"число\", чтобы выбрать режим с числами, или ввести \"цвета\", \"цвет\" или \"ц\", просто потому что Вы можете."
            self.c4longdesc = "Поместите свою шашку в выбранный ряд. Сложите их друг на друга, чтобы получить 4 в ряд - по горизонтали, вертикали или диагонали - прежде чем Ваш оппонент победит."
            self.mc4longdesc = "Те же правила, что и в 'Четыре в ряд', но с 4 игроками.\nПоместите свою шашку в выбранный ряд. Сложите их друг на друга, чтобы получить 4 в ряд - по горизонтали, вертикали или диагонали - прежде чем кто-то из Ваших оппонентов победит."
            self.tttlongdesc = "Игроки по очереди занимают клетки на 3х3 поле. Первый игрок получивший 3 в ряд - горизонтально, вертикально или диагонально - побеждает."
            self.hmlongdesc = "Отгадайте слово, чтобы Вас не повесили. Для 1-4 игроков, но **премиум игры могут иметь до 16 игроков**\nЕсли игровой режим не был выбран, все игроки будут голосовать за игровой режим в который они хотят поиграть.\nСовместный режим: Все игроки по очереди помогают решить то же слово.\nСоревновательный режим: Все игроки тайно выбирают слово, которое будет дано другому игроку на решение. Победитель тот, кто первый решит своё слово с минимальным количеством неправильных попыток."
            self.helplongdesc = "Показывает Вам всем команды, или всю информацию о конкретной команде."
            self.pinglongdesc = "Показывает задержку бота в данное время."
            self.stoplongdesc = "После того, как вы спросите других игроков, согласны ли они с этим, игра, в которой вы участвуете, закончится преждевременно. Игра закончится мгновенно, если все остальные игроки не в сети. Полезно, если кому-то нужно уйти в спешке."
            self.lblongdesc = "Отображает таблицу лидеров для запрошенной игры той же команды, на всех серверах или только на сервере, на котором Вы находитесь. Вы можете отсортировать таблицу лидеров по наибольшему количеству выигрышей или по наибольшему проценту выигрыша. Все аргументы являются необязательными, и порядок не имеет значения."
            self.statslongdesc = "Отображает статистику выбранного человека. Если человек не был выбран, показывает Ваши собственные статы."
            self.prefixlongdesc = "Меняет префикс бота на сервере.\nПрефикс обязан быть не более 8 символов, и его может поставить только пользователь с разрешением 'Управление Сервером'."
            self.langlongdesc = "Меняет язык для сервера.\nЯзык может быть изменён только пользователем с разрешением 'Управление Сервером'."
            self.displongdesc = "Изменяет вид ваших фигур в Четыре в ряд, Мега Четыре в ряд и Крестики-нолики. Работает с любыми кастомными эмоджи (включая анимированные), если бот находится на том же сервере с этим эмоджи.\nНет Nitro? Всё пучком. Просто введите имя эмоджи, и оно всё равно будет одобрено.\n**Эта функция может быть использована только Премиум пользователями. Станьте им [здесь.](https://patreon.com/CommunityGamesBot/)**"
            self.colourlongdesc = "Меняет Ваш отображаемый цвет (на маленькой полоске сбоку) во всех играх. Используйте значение RGB или шестнадцатеричный код, чтобы установить его.\n**Эта функция может быть использована только Премиум пользователями. Станьте им [здесь.](https://patreon.com/CommunityGamesBot/)**"
            self.thisServer = "Этот Сервер"
            self.allServers = "Все Сервера"
            self.lbstates = {"This Server":self.thisServer, "All Servers":self.allServers}
            self.allGames = "Все Игры"
            self.emptylb = "На этой доске лидеров ещё никого нет!"
            self.emptylb2 = "Станете ли вы первыми?"
            self.placings = ["1-й", "2-й", "3-й", "4-й", "5-й", "6-й", "7-й", "8-й", "9-й", "10-й"]
            self.cantSeePerson = "Я не могу найти этого человека..."
            self.youHaveNoStats = "У Вас пока нечего отображать на статистике!"
            self.theyHaveNoStats = "У {} пока нечего отображать на статистике!".format(self.user)
            self.personsStats = "Статистика {}".format(self.user)
            self.wins = "Победы"
            self.losses = "Поражения"
            self.draws = "Ничьи"
            self.highScores = "Лучшие результаты"
            self.played = "Игр сыграно"
            self.winRate = "Процент выигрышей"
            self.total = "Общее"

            self.addReactions = "Добавить Реакции"
            self.manageMessages = "Управление Сообщениями"
            self.readHistory = "Прочитать Историю Сообщений"
            self.externalEmoji = "Использовать Посторонние Эмоджи"
            self.permissions = {"Add Reactions" : self.addReactions, "Manage Messages" : self.manageMessages,
                                "Read Message History" : self.readHistory, "Use External Emojis" : self.externalEmoji, "":""}

            if type(self.permission) == list:
                needed = []
                for i in self.permission:
                    needed.append(self.permissions[i])
                self.needPerms = "Я пока не могу это сделать. Мне нужны следующие разрешения:\n- {}\nЕсли хотите знать почему, посетите FAQ на сервере технической поддержки, https://discord.gg/dVHsMRK.".format("\n- ".join(needed))
            elif type(self.permission) == str:
                self.needPerms = "Я пока не могу это сделать. Мне сначала нужно '{}' разрешение.\nЕсли хотите знать почему, посетите FAQ на сервере технической поддержки, https://discord.gg/dVHsMRK.".format(self.permissions[self.permission])
            self.mentionOpponent = "Вам нужно упомянуть оппонета, вот так:\n"
            self.botsCantPlay = "Боты не настолько умны, чтобы играть в {}!".format(self.games[self.game_])
            self.cantFindPerson = "Хмм, я не могу найти этого человека на этом сервере."
            self.cantPlayAgainstSelf = "Вы не можете играть против себя!"
            self.bothPlaying = "Вы оба уже играете друг с другом!"
            self.youreAlreadyPlaying = "Вы уже играете с кем-то другим!"
            self.theyreAlreadyPlaying = "{}, на данный момент, играет в другую игру!".format(self.user)
            self.bothPlayingElsewhere = "Вы оба играете в разные игры где-то в другом месте!"
            self.theyreOffline = "Кажется, они сейчас в оффлайне. Попробуйте кого-нибудь другого."
            self.reactToStartGame = "{}, Вы готовы сыграть в {}?\n\nОтреагируйте с ✅ в течение 3 минут, чтобы начать игру, иначе она будет отменена.".format(self.user, self.games[self.game_])
            self.goneElsewhere = "Ох, постой... вы оба играете где-то в другом месте!"
            self.userInOtherGame = "Ах, увы, {} находится в другой игре. Кажется, нам придётся подождать.".format(self.user)
            self.finishOtherGameFirst = "Погоди, {}, Вы уже в другой игре! Завершите её, прежде чем Вы начнёте что-либо ещё.".format(self.user)
            self.bothGone = "Ах, увы. Вы оба ушли играть в разные игры с разными людьми. Вернитесь, когда вы закончите!"
            self.userWentOffline = "Ох, нет! {} ушёл в оффлайн! Полагаю, мы не можем поиграть... :shrug:".format(self.user)
            self.noResponse = "{} не ответил. Игра была отменена.".format(self.user)
            self.whosPlaying4 = "Кто хочет поиграть?\n3 человека (кроме {}) должны отреагировать с ✅, чтобы начать игру.".format(self.user)
            self.noOneWantsToPlay = "Кажется, никто больше не хочет играть. Игра была остановлена."
            self.whosPlayingUnlimited = "Кто хочет поиграть в игру {}?\nОтреагируйте с ✅, чтобы присоединиться к игре.\n{}, используйте ту же реакцию, когда все остальные присоединятся, чтобы начать игру.".format(self.games[self.game_], self.user)
            self.cancelUnlimited = "Кажется, человек, который начал игру, решил, что он не хочет играть. Игра отменена."
            self.startMaxPlayers = "Максимальное количество игроков было достигнуто. Давайте начинать игру!"
            self.premiumCanHaveMore = "Премиум игры могут иметь до {} игроков! Посети https://patreon.com/CommunityGamesBot/ для большей информации.".format(self.number)
            self.gameStarting = "{}... Игра начинается!".format(self.user)
            self.needToDM = "{}, мне нужно прислать Вам личное сообщение, чтобы начать игру.\nЧтобы это починить, перейдите в настройки сервера (рядом с именем сервера), выберите «Настройки конфиденциальности» и включите параметр «Разрешить личные сообщения от участников сервера».".format(self.user)

            self.playersTurn = "Очередь {}!".format(self.user)
            self.playerWon = "{} победил!".format(self.user)
            if type(self.user2) == list: losers = ", ".join(self.user2[:-1]) + " и " + self.user2[-1]
            else: losers = self.user2
            self.playerWonAgainst = "{} победил игру в {} против {}!".format(self.user, self.games[self.game_], losers)
            self.draw = "Это ничья!"
            if type(self.user) == list: people = ", ".join(self.user[:-1]) + " и " + self.user[-1]
            else: people = self.user
            self.endedInDraw = "Игра в {} между {} закончилась ничьёй!".format(self.games[self.game_], people)
            self.gameWasStopped = "Эта игра была вручную остановлена"
            self.error = "Упс! Случилась ошибка."
            self.errorStopped = "Упс! Случилась ошибка. Игра была остановлена"
            self.errorWon = "Случилась ошибка, однако, {} победил!".format(self.user)

            self.modes = {"comp":"cоревновательный", "co-op":"cовместный", "colour":["цвета", "цвет", "ц"], "number":["числа", "ч", "число"]}

            self.c4HowTo = "Реагируйте с цифрой, соответствующей строке, которую Вы хотите использовать.\nУ Вас есть 30 секунд, чтобы сделать ход."
            self.c4Timeout = "{} слишком долго думал. Случайная строка была выбрана.".format(self.user)
            self.c4Offline = "{} ушёл в оффлайн. Случайная строка была выбрана.".format(self.user)

            self.tttHowTo = "Используйте реакции, соответствующие ячейке, которую Вы хотите занять. На выбор у Вас есть 30 секунд."
            self.tttTimeout = "{} слишком долго думал! Их очередь была пропущена.".format(self.user)

            self.mmWaitForCodes = "Жду, когда коды будут созданы..."
            self.prepareMakeCode = "Будьте готовы к созданию своего кода!"
            self.createCode = "Создайте свой 6-значный код!"
            self.mmTimeLimit = "У Вас есть 20 секунд, чтобы вставить каждую индивидуальную часть кода."
            self.codeFinished = "Код завершён!"
            self.goToChannel = "А теперь идите в тот канал, где игра была начата, чтобы поиграть!"
            self.previousTurns = "Предыдущие ходы:"
            self.roundNumber = "Раунд "
            self.thisTurn = "Этот ход:"
            self.resultsFromTurn = "Результаты хода от {}:".format(self.user)
            if self.mode == "colour":
                self.mmInfo =  "✅ = Правильный цвет в правильной позиции\n❔ = Этот цвет в другом месте кода\n❌ = Этого цвета нет в коде"
            else:
                self.mmInfo = "✅ = Правильная цифра в правильной позиции\n❔ = Эта цифра в другом месте кода\n❌ = Этой цифры нет в коде"
            self.reactWhenReady = "Отреагируйте с 👍, когда Вы будете готовы продолжить"
            self.notOverYet = "Это ещё не конец!"
            self.userFinishGameCont = "{} может быть и закончил, но игра продолжается до тех пор, пока вы оба не решите код!".format(self.user)
            self.gameEndedPossibleWinner = "Игра закончилась преждевременно, но, кажется, это победа для {}!".format(self.user)
            self.gameEndedWinner = "Игра закончилась преждевременно, но {} победил!".format(self.user)
            self.gameEnded = "Игра закончилась преждевременно"
            self.noRounds = "Раунды не были завершены"
            self.userDidNotComplete = "{} ещё не успел завершить его первый раунд".format(self.user)

            self.waitForShips = "В ожидании посадки судов..."
            self.preparePlaceShips = "Подготовка к размещению кораблей..."
            if self.shipType == "Aircraft Carrier": self.ship = "Авианосец"
            elif self.shipType == "Battleship": self.ship = "Линкор"
            elif self.shipType == "Destroyer": self.ship = "Разрушитель"
            elif self.shipType == "Submarine": self.ship = "Подводную лодку"
            elif self.shipType == "Patrol Boat": self.ship = "Патрульный катер"
            else: self.ship = ""
            self.placingShip = "Размещаем {}".format(self.ship)
            self.positionSetTimeout = "Положение будет установлено автоматически, если в течение 15 секунд не было выполнено никаких действий"
            self.fleetReady = "Флот готов!"
            self.userAiming = "{} целится...".format(self.user)
            self.selectX = "У вас есть 20 секунд, чтобы выбрать x координату"
            self.selectY = "У вас есть 20 секунд, чтобы выбрать y координату"
            self.alreadyFiredThere = "Вы уже стреляли туда, попробуйте куда-нибудь ещё"
            self.firing = "Стреляем..."
            self.hit = "Ранение!"
            self.missed = "Промах."
            self.sunkShip = "{} потопил {} {}!".format(self.user, self.ship, self.user2)
            self.usersShots = "Выстрелы от {}:\n".format(self.user)
            self.possibleWinner = "На данный момент, это выглядит как победа для {}!".format(self.user)
            self.possibleDraw = "На данный момент, это выглядит как ничья!"

            self.hmEnglishWords = "Пожалуйста, помните: рандомные слова выбираются ботом на английском."
            self.hmModeVote = "В какой игровой режим вы хотите поиграть?\nОтреагируйте с :wrestling:, чтобы проголосовать за Соревновательный режим, или :handshake: за Совместный режим\n\nУ вас есть 10 секунд на голосование"
            self.calculateResult = "Подсчитываем результаты..."
            self.voteDraw = "Ничья? Тогда я тоже проголосую..."
            if self.mode: self.gameModeSelected = "**{}** режим был выбран. Давайте начинать!".format(self.modes[self.mode].capitalize())
            self.hmOnePlayer = "Только ты? Ладно."
            self.hereWeGo = "Хорошо, начинаем!"
            self.incorrectGuesses = "Неправильные попытки:"
            self.takeAGuess = "{}, угадывайте".format(self.user)
            if self.wordPhrase == "word": self.wordPhrase, self.wordPhrase2, self.wordPhrase3 = "слово", "слове", "слово"
            else: self.wordPhrase, self.wordPhrase2, self.wordPhrase3 = "фраза", "фразе", "фразу"
            try:
                try: not10s = str(self.number)[-2] != "1"
                except: not10s = True
                if str(self.number)[-1] == "1" and not10s: s = "а"
                elif 4 >= int(str(self.number)[-1]) >= 2 and not10s: s = "ы"
                else: s = ""
                self.hmHowTo = "Введите букву, которая, по-вашему, находится в {}, или отгадайте сразу {}.\nУ вас есть {} секунд{} на предположение".format(self.wordPhrase2, self.wordPhrase3, self.number, s)
            except: pass
            self.alreadyGuessed = "Хм, вы уже это предполагали! Попробуйте что-то ещё."
            self.invalidLetter = "Ой-ой, это неправильная буква! Попробуйте снова."
            self.invalidWord = "Упс, это неправильн(ое/ая) {}! Попробуйте снова.".format(self.wordPhrase)
            self.letterNotInWord = "Буква {} не находится в {}".format(self.other, self.wordPhrase2)
            self.incorrectWord = "'{}' не находится в {}.".format(self.other, self.wordPhrase2)
            self.letterAppearsOnce = "Буква {} появляется единожды в {}".format(self.other, self.wordPhrase2)
            self.letterAppearsTwice = "Буква {} появляется дважды в {}".format(self.other, self.wordPhrase2)
            self.letterAppears = "Буква {} появляется {} раза в {}".format(self.other, self.other2, self.wordPhrase2)
            self.hmTimeout = "Вам не хватило времени, чтобы сделать свое предположение!"
            self.failedToGuess = "Вы не смогли угадать {}".format(self.wordPhrase3)
            self.wordWas = "{} было: ".format(self.wordPhrase)
            self.youWin = "Вы победили!"
            try:
                if self.other == "1": s1 = "у"
                elif 2 <= int(self.other) <= 4: s1 = "и"
                else: s1 = "ок"
                if self.other2 == "1": s2 = "у"
                elif 2 <= int(self.other2) <= 4: s2 = "и"
                else: s2 = "ок"
                self.coOpWinStats = "У Вас заняло {} попытк{}, чтобы угадать {}, с {} неправильн{} попытк{}".format(self.other, s1, self.wordPhrase3, self.other2, s2, s2)
            except: pass
            if type(self.user) == list: people = ", ".join(self.user[:-1]) + " и " + self.user[-1]
            else: people = self.user
            try:
                if self.other == "1": s = ""
                elif 2 <= int(self.other) <= 4: s = "и"
                else: s = "ок"
                self.hmCoOpEnd = "{} успешно отгадали {} с {} попытк{}".format(people, self.wordPhrase3, self.other, s)
            except: pass

            self.yes = "да"
            self.waitForWords = "Ожидаю создания слов..."
            self.hmSetup = "Какое слово Вы загадали? Просто напишите его. У Вас есть одна минута, чтобы его придумать."
            self.hmSetupTimeout = "Увы, время вышло. Я просто выберу случайное слово за Вас...\nВы можете идти в канал, где игра началась."
            self.hmSetupInvalid = "Извините, но вы не можете это использовать. Вводите только английские буквенно-цифровые символы и простую пунктуацию."
            self.hmTooLong = "{} по количеству символов превышает лимит! Максимальная длина - 100 символов".format(self.wordPhrase)
            self.hmTooShort = "{} по количеству символов ниже лимита! Минимальная длина - 4 символа".format(self.wordPhrase)
            self.hmSetupConfirm = "Ваше слово: **{}**\nНапишите 'да', чтобы подтвердить, или другое слово, если Вы хотите его поменять.".format(self.other)
            self.hmSetupConfirmTimeout = "Без ответа? Я подтвержу его за Вас, тогда.\nИдите в тот канал, где игра была начата, чтобы поиграть!"
            self.hmSetupComplete = "Клёво, всё настроено. Идите в тот канал, где игра была начата, чтобы поиграть!"
            self.hmSetupCancel = "Ох, неважно... Игра была остановлена."
            self.hmAllSetupsComplete = "А теперь, раз все закончили придумывать слова, давайте начинать!"
            self.yourTurn = "Ваш ход, {}!".format(self.user)
            self.wordFinished = "Вы закончили слово!"
            try:
                if self.other == "1": s1 = ""
                elif 2 <= int(self.other) <= 4: s1 = "ки"
                else: s1 = "ок"
                if self.other2 == "1": s2, s3 = "ой", "ой"
                elif 2 <= int(self.other2): s2, s3 = "ыми", "ами"
                self.personFinished = "У Вас заняло {} попытк{} чтобы угадать {}, с {} неправильн{} попыт{}!\nНе уходите далеко, чтобы увидеть результаты, когда все остальные завершат!".format(self.other, s1, self.wordPhrase3, self.other2, s2, s3)
            except: pass

            self.hmeliminated = "Вы не смогли отгадать слово. Вы были устранены из игры."
            self.everyoneFinished = "Все закончили! Подсчитываю результаты..."
            self.totalAttempts = "Общее кол-во попыток: "
            self.correctAttempts = "Кол-во правильных попыток: "
            self.incorrectAttempts = "Кол-во неправильных попыток: "
            self.score = "Результат: "
            self.scoreUnavailable = "-Score unavailable-"
            self.highScore = "High Score: "


            self.promotitles = [
                "Хей, кажется, Вы очень наслаждаетесь этими играми.",
                "Вы играли довольно много, не так ли?",
                "Вау, Вам очень нравятся эти игры, не так ли?",
                "Ваушки, Вы играли в очень много игр в последнее время."]
            self.promodesc = [
                "Почему бы не проголосовать за меня на [top.gg?](https://top.gg/bot/656058788020879370/vote)\nМне было бы очень приятно.",
                "Вы думали о [становлении членом патреона?](https://patreon.com/CommunityGamesBot/)\nДополнительная денюжка может помочь в развитии бота для больших возможностей.",
                "Вы можете помочь в развитии этого бота, если Вы [проголосуете за него.](https://top.gg/bot/656058788020879370/vote)\nЕсли Вы потратите пару лишних секунд на это, мы будем очень признательны. :)",
                "Если у Вас есть лишние деньги, почему бы не [стать патреоном?](https://patreon.com/CommunityGamesBot/)\nДаже малейшие суммы денег могут помочь развитию этого бота. :)"]

            self.onlyPremium = "Только премиум пользователи могут использовать эту функцию!"
            self.becomePremium = "Станьте одним [здесь](https://patreon.com/CommunityGamesBot/)"
            self.displaySet = "Дисплей в Четыре в ряд и Крестики-нолики для {} был изменён на {}".format(self.user, self.other)
            self.displaySetDesc = "Если Вы когда-нибудь захотите вернуть дисплей по умолчанию, используйте «очистить» или «сбросить» вместо эмоджи"
            self.displayDefault = "Дисплей для {} был поставлен по умолчанию".format(self.user)
            self.noEmojiFound = "Извините, я не смог найти этот эмоджи на этом сервере."
            self.enterEmoji = "Пожалуйста, выберите эмоджи, например:"
            self.invalidRGB = "Неверное значение RGB."
            self.invalidRGBDesc = "Обязательно используйте только целые числа от 0 до 255.\nВ качестве альтернативы, Вы можете использовать шестнадцатеричный код (например, #f42cb1) или стандартное имя цвета."
            self.invalidHex = "Неверное шестнадцатеричное значение."
            self.invalidHexDesc = "Обязательно используйте только 0-9 и a-f.\nВ качестве альтернативы, Вы можете использовать значение RGB (например, 61, 26, 125) или общее имя цвета."
            self.invalidInput = "Неккоректный ввод."
            self.invalidDesc = "Убедитесь, что Вы ввели правильное значение RGB (например, 61, 26, 125) или шестнадцатеричное значение (например, #f42cb1) или стандартное имя цвета."
            self.colourSet = "Цвет для {} был изменён на {}".format(self.user, self.other)
            self.colourSetDesc = "Если Вы когда-нибудь захотите вернуть дисплей по умолчанию, используйте «очистить» или «сбросить» вместо значения цвета"
            self.colourDefault = "Цвет для {} был поставлен по умолчанию".format(self.user)
            self.enterColour = "Пожалуйста, выберите цвет, например:"
            self.notWhite = "Не волнуйтесь, это нормально, что он не выглядит белым, т.к. Discord рассматривает его как значение по умолчанию.\nЕсли Вы хотите белый цвет, я рекомендую использовать #fefefe (или 254, 254, 254).."
            self.colours = {"red":"красный", "orange":"оранжевый", "gold":"золотой", "yellow":"жёлтый", "green":"зелёный", "aqua":"голубой", "blue":"синий", "purple":"фиолетовый", "violet":"лиловый", "magenta":"пурпурный", "pink":"розовый", "white":"белый", "gray":"серый", "black":"чёрный", "reset":"сбросить", "clear":"очистить"}

            self.downtime = "Подождите, у меня небольшой перерыв (возможно из-за апдейта). Я вернусь через несколько минут!"
            self.comingSoon = "Эта игра скоро выйдет!\nХочешь поиграть в неё сейчас? Стань бета-тестером здесь: https://patreon.com/CommunityGamesBot/"



        if self.lang == "Polish": # Translation by KVBA
            self.translatorID = 317778691390439424
            # Command Names
            self.c4 = "Czwórki"
            self.mc4 = "Mega Czwórki"
            self.ttt = "Kółko i Krzyżyk"
            self.bs = "Statki"
            self.mm = "Mastermind"
            self.hm = "Wisielec"
            self.games = {"Connect 4":self.c4, "Mega Connect 4":self.mc4, "Tic Tac Toe":self.ttt,
                            "Battleship":self.bs, "MasterMind":self.mm, "Hangman":self.hm, "":""}
            self.stop = "Zakończ grę"
            self.lb = "Tabela wyników"
            self.stats = "Statystyki"
            self.ping = "Ping"
            self.prefix = "Prefiks"
            self.disp = "Widok"
            self.colour = "Kolor"
            self.language = "Język"
            self.help = "Pomoc"

            # Utility Commands
            self.ending = "Dobra, kończę grę natychmiast..."
            self.stopped = "Gra została zakończona"
            self.mustBeInGame = "Musisz być *w* grze by ją zakończyć!"
            self.okayToStop = "{}, czy zgadzacie się na zakończenie gry?".format(self.user)
            self.pong = "Pong!"
            self.connection = "Połączenie z Discordem: "
            self.processDelay = "Opóźnienie przetwarzania: "
            self.latency = "Całkowite opóźnienie: "
            self.enterPrefix = "Proszę wpisać prefix, np."
            self.prefixSet = "Ustawiono `{}` jako nowy prefiks".format(self.prfx)
            self.prefixTooLong = "Prefiks jest zbyt długi! Musi mieć 8 znaków lub mniej."
            self.askAdminPrefix = "Musisz mieć pozwolenie 'Zarządzanie serwerem' by użyć tej komendy. Poproś admina o zmianę prefiksu"
            self.askAdminLanguage = "Musisz mieć pozwolenie 'Zarządzanie serwerem' by użyć tej komendy. Poproś admina o zmianę języka."
            self.setlang = "Język ustawiony na polski"
            self.setlangdesc = "Przetłumaczone przez {}".format(self.other)
            self.setLanguageHeader = "Ustaw język"

            # Help
            self.gamecommands = "Komendy gier"
            self.c4shortdesc = "Ułóż 4 w rzędzie aby wygrać!"
            self.mc4shortdesc = "Czwórki, dla 4 graczy!"
            self.bsshortdesc = "Zatop statki przeciwnika!"
            self.tttshortdesc = "Miej 3 pola w rzędzie by wygrać!"
            self.mmshortdesc = "Złam kod przeciwnika!"
            self.hmshortdesc = "Odgadnij słowo zanim stracisz wszystkie szanse!"
            self.moreinfo = "Wpisz {}help (komenda) aby zobaczyć więcej informacji na temat komendy".format(self.prefix)

            self.misccommands = "Różne/Komendy Użytkowe"
            self.stopshortdesc = "Kończy grę, w której uczestniczysz"
            self.lbshortdesc = "Pokazuje tabelę wyników"
            self.statsshortdesc = "Pokazuje statystyki wybranej osoby"
            self.pingshortdesc = "Sprawdza opóźnienie bota"
            self.prefixshortdesc = "Zmienia prefix bota."
            self.langshortdesc = "Ustawia język bota"
            self.dispshortdesc = "**(Tylko dla Premium)** Zmień widok Czwórek oraz Kółka i Krzyżyka"
            self.colourshortdesc = "**(Tylko dla Premium)** Zmień wyświetlany kolor wszystkich gier"
            self.helpshortdesc = "Pokazuje tą listę"

            self.links = "Linki"
            self.patreon = "Patreon"
            self.vote = "Oddaj głos na liście Discord Bot List"
            self.suggest = "Zasugeruj nową grę"
            self.invite = "Zaproś mnie na swój serwer"
            self.support = "Wesprzyj serwer"

            self.opponent = "@przeciwnik"
            self.gamemode = "tryb gry"
            self.game = "gra"
            self.command = "komenda"
            self.winrateoption = "wygrane/procent"
            self.globallocal = "globalny/lokalny"
            self.local = "lokalny"
            self.person = "osoba"
            self.newprefix = "nowy prefiks"
            self.emoji = "emoji"
            self.value = "wartość"
            if type(self.commands) == list: self.canBeTriggeredWith = "Ta komenda również działa jako '{}' oraz '{}'".format("', '".join(self.commands[:-1]), self.commands[-1])
            else: self.canBeTriggeredWith = "Ta komenda również działa jako '{}'".format(self.commands)
            self.bslongdesc = "Dwaj gracze umieszczają sekretnie swoje statki na planszy 10x10. Gracze na zmianę zgadują pozycje tych statków, pomagając sobie poprzednimi trafieniami. Wtedy okaże się, czy strzał był celny czy chybiony. Rozgrywka trwa dopóty, dopóki statki jednego z graczy zostaną zatopione."
            self.mmlongdesc= "Dwaj gracze tworzą kody dla siebie nawzajem. Gracze na zmianę zgadują kody przeciwnika, pomagając sobie poprzednimi trafieniami. Potem dowiadują się o tym, czy cyfra jest na poprawnym miejscu, gdzieś indziej lub czy nie ma jej w kodzie. Rozgrywka toczy się dotąd, aż obaj gracze zgadną kod.\n\nArgument 'gamemode' jest opcjonalny. Domyślnie ustawiony jest na kolory, jednak możesz wpisać \"numery\", \"n\" lub \"numer\" by używać numerów, albo \"kolor\", \"kolory\" lub \"k\", ponieważ możesz ._."
            self.c4longdesc = "Wybierz rząd, w którym umieścisz żeton. Wygrywa ten, który jako pierwszy ułoży je tak, by mieć 4 z rzędu - poziomo, pionowo lub ukośnie."
            self.mc4longdesc = "Zasady takie same jak w klasycznych czwórkach, tylko dla 4 graczy.\nWybierz rząd, w którym umieścisz żeton. Wygrywa ten, który jako pierwszy ułoży je tak, by mieć 4 z rzędu - poziomo, pionowo lub ukośnie."
            self.tttlongdesc = "Gracze na zmianę wybierają pole z siatki 3x3. Wygrywa ten, który jako pierwszy będzie miał 3 pola w rzędzie: poziomo, pionowo lub ukośnie."
            self.hmlongdesc = "Odgadnij słowo by uniknąć stryczka. Gra dla 1-4 graczy, lecz **gry premium mogą pomieścić 16 graczy.**\nJeżeli tryb gry jest pusty, gracze będą głosować na tryb, w który chcą zagrać.\nTryb kooperacji: Wszyscy gracze zgadują po kolei to samo słowo\nTryb konkurencji: Wszyscy gracze sekretnie wybierają słowo, które inny gracz musi zgadnąć. Wygrywa ten, który jako pierwszy poprawnie odgadnie słowo z najmniejszą ilością błędów."
            self.helplongdesc = "Pokazuje wszystkie komendy, lub szczegóły wybranej komendy."
            self.pinglongdesc = "Pokazuje opóżnienie bota."
            self.stoplongdesc = "Po zapytaniu pozostałych graczy czy na to pozwalają, gra zakończy się przed rozstrzygnięciem. Gra zakończy się natychmiast gdy pozostali gracze są offline. Przydatne w sytuacji gdy ktoś musi opuścić grę w pośpiechu."
            self.lblongdesc = "Pokazuję tabelę wyników wybranej gry o tej samej komendzie, we wszystkich serwerach, lub tylko w tym serwerze. Możesz sortować tabelę według ilości lub procenta wygranych. Wszystkie argumenty są opcjonalne a ich kolejność jest dowolna."
            self.statslongdesc = "Pokazuje statystyki danej osoby. Jeżeli osoba nie została wskazana, pokaże twoje statystyki."
            self.prefixlongdesc = "Zmienia prefiks bota na serwerze.\nPrefiks musi mieć 8 znaków lub mniej, i może go ustawić osoba z pozwoleniem 'Zarządzanie serwerem'."
            self.langlongdesc = "Zmienia język bota na serwerze.\nJęzyk może być zmieniony tylko przez członków z uprawnieniem 'Zarządzanie serwerem'."
            self.displongdesc = "Zmienia wygląd elementów w Czwórkach, Mega Czwórkach oraz Kółku i Krzyżyku. Działa z każdą zewnętrzną emotką (również animowaną), dopóki bot jest w serwerze z nią.\nNie masz Nitro? Nie przejmuj się. Wpisz \"\\:emotka:\", a zostanie to zaakceptowane.\n**To działa tylko dla użytkowników premium. Możesz zostać nim [tutaj.](https://patreon.com/CommunityGamesBot/)**"
            self.colourlongdesc = "Zmienia wyświetlany kolor (na pasku po lewej) we wszystkich grach. Użyj wartości RGB lub hex.\n**To działa tylko dla użytkowników premium. Możesz zostać nim [tutaj.](https://patreon.com/CommunityGamesBot/)**"
            self.thisServer = "Ten serwer"
            self.allServers = "Wszystkie serwery"
            self.lbstates = {"This Server":self.thisServer, "All Servers":self.allServers}
            self.allGames = "Wszystkie gry"
            self.emptylb = "Nikogo nie ma na tej tabeli!"
            self.emptylb2 = "Może będziesz pierwszy/a!"
            self.placings = list(range(1, 11))
            self.cantSeePerson = "Nie mogę znaleźć tej osoby..."
            self.youHaveNoStats = "Nie masz jeszcze żadnych statystyk!"
            self.theyHaveNoStats = "{} nie ma jeszcze żadnych statystyk!".format(self.user)
            self.personsStats = "Statystyki {}".format(self.user)
            self.wins = "Zwycięztwa"
            self.losses = "Porażki"
            self.draws = "Remisy"
            self.highScores = "Rekord"
            self.played = "Rozegrane gry"
            self.winRate = "Procent wygranych"
            self.total = "Całkowite"

            self.addReactions = "Dodawanie reakcji"
            self.manageMessages = "Zarządzanie wiadomościami"
            self.readHistory = "Czytanie historii czatu"
            self.externalEmoji = "Używanie zewnętrznych emoji"
            self.permissions = {"Add Reactions" : self.addReactions, "Manage Messages" : self.manageMessages,
                                "Read Message History" : self.readHistory, "Use External Emojis" : self.externalEmoji, "":""}

            if type(self.permission) == list:
                needed = []
                for i in self.permission:
                    needed.append(self.permissions[i])
                self.needPerms = "Nie mogę tego zrobić. Potrzebuję tych pozwoleń:\n- {}\nJeśli chcesz dowiedzieć się dlaczego, odwiedź sekcję FAQ na https://discord.gg/dVHsMRK".format("\n- ".join(needed))
            elif type(self.permission) == str:
                self.needPerms = "Nie mogę tego zrobić. Potrzebuję pozwolenia '{}'.\nJeśli chcesz dowiedzieć się dlaczego, odwiedź sekcję FAQ na https://discord.gg/dVHsMRK".format(self.permissions[self.permission])
            self.mentionOpponent = "Musisz dać znać użytkownikowi, o tak:\n"
            self.botsCantPlay = "Boty nie są tak mądre by grać w {}!".format(self.games[self.game_])
            self.cantFindPerson = "Hmm, nie mogę znaleźć takiej osoby."
            self.cantPlayAgainstSelf = "Nie możesz grać przeciwko sobie!"
            self.bothPlaying = "Oboje już gracie ze sobą!"
            self.youreAlreadyPlaying = "Już z kimś grasz!"
            self.theyreAlreadyPlaying = "{} już gra z kimś!".format(self.user)
            self.bothPlayingElsewhere = "Oboje gracie w rózne gry!"
            self.theyreOffline = "Ta osoba wydaje się być offline. Spróbuj z kimś innym."
            self.reactToStartGame = "{}, czy jesteś gotowy/a zagrać w {}?\n\nDodaj reakcję ✅ by zacząć, masz 3 minuty zanim gra będzie anulowana.".format(self.user, self.games[self.game_])
            self.goneElsewhere = "O, czekajcie... oboje już gracie gdzieś indziej!!"
            self.userInOtherGame = "Cholibka, {} już z kimś gra. Chyba musimy poczekać na niego/nią.".format(self.user)
            self.finishOtherGameFirst = "{}, już jesteś w innej grze! Zakończ tamtą zanim dołączysz.".format(self.user)
            self.bothGone = "Ojoj. Oboje już gracie w różne gry z różnymi osobami. Wróćcie jak skończycie!"
            self.userWentOffline = "O nie! {} jest offline! Chyba nie możemy teraz zagrać... :shrug:".format(self.user)
            self.noResponse = "{} nie odpowiedział(a). Gra anulowana.".format(self.user)
            self.whosPlaying4 = "Kto chce zagrać?\n3 osoby (oprócz {}) muszą dać ✅ zanim zaczniemy.".format(self.user)
            self.noOneWantsToPlay = "Nikt nie chce zagrać. Gra anulowana."
            self.whosPlayingUnlimited = "Kto chce zagrać?\nDodaj reakcję ✅ by dołączyć do gry.\n{}, użyj tej reakcji gdy wszyscy dołączą by zacząć grę.".format(self.user)
            self.cancelUnlimited = "Wygląda na to, że osoba, która zaczęła grę nie chce już grać. Gra anulowana."
            self.startMaxPlayers = "Osiągnięto maksymalną liczbę graczy. Zaczynamy!"	
            self.premiumCanHaveMore = "W gry premium można grać w {} graczy! Odwiedź https://patreon.com/CommunityGamesBot/ aby dowiedzieć się więcej.".format(self.number)
            self.gameStarting = "{}... Zaczynamy grę!".format(self.user)
            self.needToDM = "{}, muszę wysłać do ciebie prywatną wiadomość by przygotować grę.\nBy to  naprawić, kliknij nazwę serwera, wybierz \"Ustawienia prywatności\" i włącz \"Zezwól na wiadomości prywatne od członków serwerów\".".format(self.user)

            self.playersTurn = "Kolej na {}!".format(self.user)
            self.playerWon = "{} wygrywa!".format(self.user)
            if type(self.user2) == list: losers = ", ".join(self.user2[:-1]) + " i " + self.user2[-1]
            else: losers = self.user2
            self.playerWonAgainst = "{} wygrał(a) grę {} przeciwko {}!".format(self.user, self.games[self.game_], losers)
            self.draw = "Mamy remis!"
            if type(self.user) == list: people = ", ".join(self.user[:-1]) + " i " + self.user[-1]
            else: people = self.user
            self.endedInDraw = "Gra {} pomiędzy {} zakończyła się remisem!".format(self.games[self.game_], people)
            self.gameWasStopped = "Gra została zakończona manualnie."
            self.error = "Ups! Wystąpił błąd."
            self.errorStopped = "Ups! Wystąpił błąd. Gra została zakończona."
            self.errorWon = "Wystąpił błąd, ale pomimo tego, {} wygrał(a)!".format(self.user)

            self.modes = {"comp":"tryb konkurencji", "co-op":"tryb kooperacji", "colour":["kolor", "kolory", "k"], "number":["numery", "n", "numer"]}

            self.c4HowTo = "Dodaj reakcję odpowiadającą numerowi rzędu.\nMasz 30 sekund na ruch."
            self.c4Timeout = "{} nie odpowiedział w czasie. Wybrano losowy rząd.".format(self.user)
            self.c4Offline = "{} jest offline. Wybrano losowy rząd.".format(self.user)

            self.tttHowTo = "Użyj reakcji odpowiadającej polu, które chesz zaznczyć. Masz 30 sekund na ruch."
            self.tttTimeout = "{} nie zdążył(a)! Ruch pominięty.".format(self.user)

            self.mmWaitForCodes = "Oczekiwanie na kody..."
            self.prepareMakeCode = "Przygotuj się na stworzenie kodu!"
            self.createCode = "Stwórz swój kod!"
            self.mmTimeLimit = "Masz 20 sekund na dodanie każdej części kodu."
            self.codeFinished = "Kod zakończony!"
            self.goToChannel = "Teraz przejdź do kanału, w którym gra została zaczęta!"
            self.previousTurns = "Poprzednie ruchy:"
            self.roundNumber = "Runda "
            self.thisTurn = "Ten ruch:"
            self.resultsFromTurn = "Wyniki z tury {}:".format(self.user)
            if self.mode == "colour":
                self.codeType =  "kolor"
            else:
                self.codeType = "numer"
            self.mmInfo = "✅ = Poprawny {} w poprawnym miejscu\n❔ = Poprawny {}, ale w innym miejscu\n❌ = Tego {}u nie ma w kodzie.".format(self.codeType, self.codeType, self.codeType)
            self.reactWhenReady = "Dodaj reakcję 👍 gdy jesteś gotowy/a"
            self.notOverYet = "Jeszcze nie koniec!"
            self.userFinishGameCont = "{} już skończył(a), ale gra trwa dotąd, aż oboje zgadniecie!".format(self.user)
            self.gameEndedPossibleWinner = "Gra skończyła się przedwcześnie, ale wygląda na to, że {} zwyciężył(a)!".format(self.user)
            self.gameEndedWinner = "Gra skończyła się przedwcześnie, ale {} wygrał(a)!".format(self.user)
            self.gameEnded = "Gra skończyła się przedwcześnie."
            self.noRounds = "Żadna runda nie została zakończona."
            self.userDidNotComplete = "{} nie skończył(a) pierwszej rundy".format(self.user)

            self.waitForShips = "Oczekiwanie na rozstawienie statków..."
            self.preparePlaceShips = "Przygotowanie na umieszczenie statków..."
            if self.shipType == "Aircraft Carrier": self.ship = "Lotniskowiec"
            elif self.shipType == "Battleship": self.ship = "Okręt wojenny"
            elif self.shipType == "Destroyer": self.ship = "Niszczyciel"
            elif self.shipType == "Submarine": self.ship = "Łódź podwodna"
            elif self.shipType == "Patrol Boat": self.ship = "Łódź patrolowa"
            else: self.ship = ""
            self.placingShip = "Umieszczam {}".format(self.ship)
            self.positionSetTimeout = "Pozycja będzie ustawiona automatycznie jeśli w przeciągu 15 sekund nie będzie żadnych poprawek."
            self.fleetReady = "Flota gotowa!"
            self.userAiming = "{} celuje...".format(self.user)
            self.selectX = "Masz 20 sekund na podanie pozycji X"
            self.selectY = "Masz 20 sekund na podanie pozycji Y"
            self.alreadyFiredThere = "Już tam strzelałeś/aś, spróbuj gdzieś indziej."
            self.firing = "Strzelam..."
            self.hit = "Trafienie!"
            self.missed = "Pudło"
            self.sunkShip = "{} zatopił(a) {} gracza {}!".format(self.user, self.ship, self.user2)
            self.usersShots = "Strzały {}:\n".format(self.user)
            self.possibleWinner = "Wygląda na to, że {} wygrał(a)!".format(self.user)
            self.possibleDraw = "Wygląda na to, że mamy remis!"

            self.hmEnglishWords = "Uwaga: Słowa losowane przez bota są tylko po angielsku"
            self.hmModeVote = "W jakim trybie chcecie zagrać?\nDodaj reakcję :wrestling: by grać w trybie konkurencji, lub :handshake: by grać w trybie kooperacji.\n\nMacie 10 sekund na podjęcie decyzji."
            self.calculateResult = "Obliczam wynik..."
            self.voteDraw = "Remis? W takim razie ja też zagłosuję..."
            if self.mode: self.gameModeSelected = "**{}** został wybrany. Zaczynamy!".format(self.modes[self.mode].capitalize())
            self.hmOnePlayer = "Tylko ty? No dobra."
            self.incorrectGuesses = "Pomyłki:"
            self.takeAGuess = "{}, twój ruch".format(self.user)
            self.hmHowTo = "Wpisz literę, która według ciebie występuje w haśle, lub samo hasło.\nMasz na to {} sekund.".format(self.number)
            self.alreadyGuessed = "Hmm, już to odgadłeś! Spróbuj czegoś innego."
            self.invalidLetter = "Ups, to nie jest dobra litera! Spróbuj ponownie."
            self.invalidWord = "Ups, to nie jest poprawne hasło! Spróbuj ponownie."
            self.letterNotInWord = "Litera {} nie występuje w tym haśle".format(self.other)
            self.incorrectWord = "'{}' nie jest hasłem".format(self.other)
            self.letterAppearsOnce = "Litera {} występuje raz w haśle".format(self.other)
            self.letterAppearsTwice = "Litera {} występuje dwa razy w haśle".format(self.other)
            self.letterAppears = "Litera {} występuje {} razy w haśle".format(self.other, self.other2)
            self.hmTimeout = "Czas minął!"
            self.failedToGuess = "Nie udało ci się zgadnąć hasła"
            self.wordWas = "Hasło to: "
            self.youWin = "Wygrałeś/aś!"

            
            try:
                try: not10s = self.other[-2] != "1"
                except: not10s = True
                if self.other == "1": s = "ę"
                elif 2 <= int(self.other) <= 4 and not10s: s = "y"
                else: s = ""
            except: s = ""
            self.coOpWinStats = "Odgadnięcie hasła zajęło ci {} prób{}, z {} szansami w zapasie.".format(self.other, s, self.other2)
            if type(self.user) == list: people = ", ".join(self.user[:-1]) + " i " + self.user[-1]
            else: people = self.user
            self.hmCoOpEnd = "{} poprawnie odgadli hasło w {} prób.".format(people, self.other)

            self.yes = "tak"
            self.waitForWords = "Oczekiwanie na hasła..."
            self.hmSetup = "Wpisz swoje hasło. Masz minutę na wpisanie."
            self.hmSetupTimeout = "Minuta minęła. Wybiorę losowe słowo za ciebie...\nMożesz przejść do kanału, w którym toczyć się będzie gra."
            self.hmSetupInvalid = "Hasło niepoprawne. Używaj liter A-Z (bez polskich znaków), cyfr oraz podstawowej interpunkcji"
            self.hmTooLong = "Hasło jest za długie! Maksymalna długość wynosi 100 znaków"
            self.hmTooShort = "Hasło jest za krótkie! Musi mieć co najmniej 4 litery"
            self.hmSetupConfirm = "Twoje hasło to: **{}**\nWpisz 'tak' by potwierdzić, lub wpisz inne słowo jeśli chcesz je zmienić.".format(self.other)
            self.hmSetupConfirmTimeout = "Brak odpowiedzi? Potwierdzę za ciebie.\nPrzejdź do kanału, w którym zaczęła się gra!"
            self.hmSetupComplete = "OK, jesteś gotowy/a. Przejdź do kanału, w którym zaczęła się gra"
            self.hmAllSetupsComplete = "Wszyscy wymyślili hasła. Zaczynamy!"
            self.yourTurn = "Twoja kolej, {}!".format(self.user)
            self.wordFinished = "Odgadłeś/aś hasło!"
            self.personFinished = "Odgadnięcie hasła zajęło ci {} prób{}, z {} szansami w zapasie.\nZostań by zobaczyć wyniki innych graczy gdy skończą!".format(self.other, s, self.other)
            self.hmeliminated = "Nie udało ci się odgadnąć hasła. Zostałeś/aś wyeliminowany/a."
            self.everyoneFinished = "Wszyscy skończyli! Liczę wyniki..."
            self.totalAttempts = "Wszystkich prób: "
            self.correctAttempts = "Poprawnych prób: "
            self.incorrectAttempts = "Pomyłek: "
            self.score = "Wynik: "
            self.scoreUnavailable = "-Wynik niedostępny-"
            self.highScore = "Rekord: "

            self.downtime = "Chwileczkę, będę niedostępny przez krótki moment (prawdopodobnie przez aktualizację). Wrócę za kilka minut!"
            self.comingSoon = "Ta gra będzie dostępna wkrótce!\nChcesz zagrać teraz? Zostań testerem na https://patreon.com/CommunityGamesBot/"

            self.promotitles = [
                "Hej, wydajesz się bardzo lubić te gry.",
                "Grałeś/aś w to już jakiś czas, prawda?",
                "Wow, bardzo lubisz te gry, co nie?",
                "Łoo, rozegrałeś/aś sporo gier."]
            self.promodesc = [
                "Myślałeś/aś może nad [zostawieniem paru groszy](https://patreon.com/CommunityGamesBot)?\nDrobna kwota pomoże w ulepszaniu tego bota.",
                "Jeśli masz kilka groszy, dlaczego nie [zostać patronem na Patreon?](https://patreon.com/CommunityGamesBot)\nNawet najmniejsze kwoty pomogą ulepszać tego bota :)",
                "Możesz pomóc temu botu poprzez [głosowanie na niego.](https://top.gg/bot/656058788020879370/vote)\nGdybyś poświęcił(a) na to kilka sekund, byłbym bardzo wdzięczny.",
                "Dlaczego więc nie oddać głosu na [top.gg](https://top.gg/bot/656058788020879370/vote)?\nByłbym bardzo wdzięczny. :)"]

            self.onlyPremium = "Tylko użytkownicy premium mogą z tego skorzystać!"
            self.becomePremium = "Zostań jednym z nich [tutaj.](https://patreon.com/CommunityGamesBot/)"
            self.displaySet = "Czwórki oraz Kołko i Krzyżyk: widok dla {} zmieniony na {}".format(self.user, self.other)
            self.displaySetDesc = "Jeśli chcesz powrócić do domyślnego wyglądu, użyj \"wyczyść\" lub \"reset\" zamiast emotki"
            self.displayDefault = "Wygląd dla {} ustawiony do wartości domyślnej".format(self.user)
            self.noEmojiFound = "Przepraszam, nie mogłem znaleźć tej emotki na tym serwerze."
            self.enterEmoji = "Proszę podać emotkę, np."
            self.invalidRGB = "Niepoprawna wartość RGB."
            self.invalidRGBDesc = "Używaj tylko liczb całkowitych od 0 do 255.\nAlternatywnie, możesz użyć wartości hex (np. #f4acb1)"
            self.invalidHex = "Niepoprawna wartość hex."
            self.invalidHexDesc = "Używaj tylko cyfr 0-9 oraz liter a-f.\nAlternatywnie, możesz użyć wwartości RGB (np. 61, 26, 125)"
            self.invalidInput = "Niepoprawna wartość."
            self.invalidDesc = "Upewnij się, że wpisujesz prawidłową wartość RGB (np. 61, 26, 125) lub hex (np. #f42cb1)"
            self.colourSet = "Kolor dla {} ustawiony na {}".format(self.user, self.other)
            self.colourSetDesc = "Jeśli chcesz powrócić do domyślnego wyglądu, użyj \"wyczyść\" lub \"reset\"."
            self.colourDefault = "Kolor dla {} ustawiony do wartości domyślnej".format(self.user)
            self.enterColour = "Proszę podać kolor, np."
            self.notWhite = "Nie przejmuj się, to normalne, że nie wyświetla się jako idealnie biały. Discord traktuje to jako wartość domyślną.\nJeśli chcesz biały kolor, użyj #fefefe.\nJeśli chcesz zmienić kolor na domyślny, wpisz \"wyczyść\" lub \"reset\" zamiast koloru."
            self.colours = {"red":"czerwony", "orange":"pomarańczowy", "gold":"złoty", "yellow":"żółty", "green":"zielony", "aqua":"akwamaryna", "blue":"niebieski", "purple":"fioletowy", "violet":"fiołkowy", "magenta":"magenta", "pink":"różowy", "white":"biały", "gray":"szary", "black":"czarny", "reset":"reset", "clear":"wyczyść"}	


            
            
    def update(self, user="", game="", user2="", permission="", mode="", shipType="", prefix="", commands="", number=0, wordPhrase="", other="", other2=""):
        self.__init__(self.lang, user, game, user2, permission, mode, shipType, prefix, commands, number, wordPhrase, other, other2)
