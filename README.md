# Community-Games-Bot
A Discord bot written using the discord.py library for simple tabletop games with friends in your server.

***NOTE: This project has been discontinued, and as such does not support the latest Discord API features such as threads, slash commands and other interactions.***

## Commands
### Game Commands
The most commonly used commands, with the main functions of the bot - games. Each game is contained in its own function inside the Game class.
The opponent argument can be passed with any information that points to a user - name, nickname, user ID or mention.

- **connect4 [opponent]**
  - Aliases: c4, connectfour
  - Two players take turns dropping counters onto a 7x6 grid and get four in a row horizontally, vertically or diagonally to win.
- **megaconnect4**
  - Aliases: mc4, megaconnectfour
  - Connect 4, but for 4 players. Includes a larger 11x10 grid.
- **tictactoe [opponent]**
  - Aliases: ttt, xo
  - Two players take turns claiming squares on a 3x3 grid and get three in a row horizontally, vertically or diagonally to win.
- **mastermind [opponent] (code type)**
  - Aliases: mm, codecracker, cc.
  - The 'code type' argument is optional. It defaults to colours if left empty (also accepts "colours", "colors", "colour", "color" and "c"), but number mode is also available when "numbers", "number" or "n" is entered, providing the players with 10 digits to put in their code, whereas colour mode only offers 9 colours.
  - Two players create a 6-digit code for each other to solve. They take turns at guessing and receive results of whether the input had the correct item in the correct position, a correct item in the wrong position, or an incorrect item. The results of each turn are available as reference in future turns. Play continues until both players have solved their codes
- **battleship [opponent]**
  - Aliases: battleships, bs, seabattle, sb
  - Two players hide ships on a 10x10 grid for each other to find. They take turns at guessing locations, and are shown whether their 'shot' was a hit or miss. Play continues until one player has sunk the other's entire fleet of 5 ships.
- **hangman (game mode)**
  - Alias: hm
  - The 'game mode' argument is optional, and only used if there are at least 2 players. Valid entries are: "co-op", "coop", "co-operation", "cooperation", "co-operate", "cooperate", "comp", "competitive", "compete" and "competition". When left empty, the players will vote on which mode to play.
  - A game for any number of players. Limits set by the bot are a max of 4 players, or 16 players in premium-enabled games. The players try to guess a word given to them (either by the bot or another user), one letter at a time. After a certain amount of incorrect attempts, they lose.
  - In Co-op mode, all players take turns to help solve the same word. In Competitive mode, all players select a word or phrase to be assigned to another random player to solve. The winner is (usually) the first to solve their word with the fewest incorrect attempts. A Scrabble-like scoring system applies, where incorrect guesses will subtract a certain number of points, and correct letters will be added (multiplied by the number of times the letter appears in the word/phrase) to the score, with a winner's bonus if they are the first to finish.

### Misc/Utility Commands
These commands are for those who want to customise their experience by setting the language, prefix, etc. and offers a couple of debug commands.

- **stop**
	- Aliases: end, quit, kill
	- Sends a request to stop the current game early. The bot will ask the other players for approval (as long as they are online), and then end the game.
- **leaderboard (game) (wins/rate) (global/local)**
	- Displays the leaderboard.
	- Arguments are all optional, and can be applied in any order. 'game' can be any game command or alias, defaults to total across all games. 'wins/rate' will default to wins, but will accept "rate", "winrate", "percent" and "percentage" to switch to sort by win rate. 'global/local' defaults to local, but will accept "server", "s", "l" and "local" to show only the members of the guild the command is run in.
- **statistics (user)**
	- Alias: stats
	- Displays the statistics of the selected user: wins, losses, draws, games played and win rate for each game. If no user is selected in the command invocation, the user that ran the command will be selected.
- **display [emoji]**
	- Aliases: disp, emoji, avatar, avi
	- Changes the emoji used for the user's pieces in Connect 4, Mega Connect 4 and Tic Tac Toe. Accepts both unicode emoji and custom emoji - even animated ones!
	- Can only be used by users with premium features enabled.
- **colour [value]**
	- Aliases: color, c
	- Changes the colour used to indicate the user's turn in all games. The 'value' argument will accept hex codes (e.g. #020bb7), RGB values (e.g. 2, 11, 183) and basic verbal colours (e.g. blue).
	- Can only be used by users with premium features enabled.
- **prefix [new prefix]**
	- Aliases: customprefix, setprefix
	- Changes the prefix the bot will respond to in the guild the command is run in. Maximum of 8 characters.
	- Can only be run by a member with the 'Manage Server' permission
- **language (language)**
	- Changes the language the bot uses in the guild the command is run in. Options are English, French, Spanish, Chinese, Polish, Russian and Italian. If the command is given no arguments, the bot will provide a reaction-based selection screen.
	- Can only be run by a member with the 'Manage Server' permission
- **ping**
	- Alias: p
	- Returns the latency of the bot, including info about processing delay
- **help (command)**
	- Alias: h
	- Gives a list of all the commands, or more info about a specific command.

### Dev-Only Commands
These commands are only accessible by users in the dev_user_ids list, no response will be given if a user does not have the permission to use it

- **shard**
  - States which shard the guild the command is run in, as well as the total number of shards
- **save**
  - Forces a save of player statistics to the windata.pkl file
- **killbot**
  - Allows current games to finish and prevents new games from starting, and once all games are complete will close the program
- **running**
  - Returns a list of the currently running games, stating the internal game ID, game type (e.g. Connect 4), players, guild name and channel name.
  - Also shows number of each game type being played currently in dictionary form (e.g. {"MasterMind":0, "Tic Tac Toe":1, "Connect 4":3} etc.)
- **servers**
  - Returns the full list of all the servers the bot is in, with server name, owner and ID.
  - Counts total number of members in each server and displays the total sum of members across all servers
- **forceremove [game ID]**
  - Aliases: fr, forcestop, fs
  - Used as a temporary fix for some games not being registered as finished, removes the game with the specified ID from the list of current games, allowing the players to start a new game
- **viewpremium**
  - Alias: vp
  - Returns the list of user/guild IDs and names that have premium features enabled
- **premiumadd [user or guild ID]**
  - Alias: padd
  - Adds the specified user or guild to the list of premium-enabled users and guilds
- **premiumremove [user or guild ID]**
  - Alias: premove
  - Removes the specified user or guild from the list of premium-enabled users and guilds
- **togglepremium**
  - Aliases: toggle, tp
  - Toggles the premium status of the guild the command is run in
- **addstatus [string]**
  - Alias: as
  - Adds the specified string to the playing status loop
- **viewstatus**
  - Aliases: vs, viewstatuses
  - Returns the list of statuses currently in the loop
- **removestatus [string or int]**
  - Aliases: rs, remstatus
  - Removes the specified status by matching the string entered, or by the index in the list of statuses

## Files
- **main.py**
  - The file with all the code in it. Yes, one file. Sorry.
- **languages.py**
  - Just kidding, there's this as well. It contains all the possible outputs for each language in one class, which is called in `main.py`
- **words.pkl**
  - The list of words used in Hangman. It is currently incomplete, but (this)[https://github.com/dwyl/english-words] might come in handy if you want to expand it.

## Dependencies
- (discord.py)[https://github.com/Rapptz/discord.py]
- (emoji)[https://github.com/carpedm20/emoji]
