from asyncio.windows_events import NULL
from os import times
import random
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
version_num = "1.54" # helps to keep track of updates while running program and in discord
emptyBoard = [['-','-','-','-','-','-','-'], ['-','-','-','-','-','-','-'], ['-','-','-','-','-','-','-'], ['-','-','-','-','-','-','-'], ['-','-','-','-','-','-','-'], ['-','-','-','-','-','-','-']]

@bot.command(name="idea", help="Get idea from preset ideas to add to this robot")
async def idea(ctx):
    lines = open("Discord Bot.txt", "r").read().split("\n")
    await ctx.send("Add a feature to me: " + random.choice(lines))


@bot.command(name="echo", help="Repeats what is said after the command")
async def echo(ctx, *, args=""):
    if args:
        await ctx.send(args)
    else:
        await ctx.send("I can't copy nothing")


@bot.command(name="ligma", help="Secret command that no one should call")
async def ligma(ctx):
    if random.randint(1,3) // 3:    # True == 1 in python. If the number is a 3, do next line
        await ctx.send("Ligma dragon!")
    else:
        await ctx.send("!dragon")


@bot.command(name="dragon", hidden=True)    # hidden=True means that the command doesn't show up in !help
async def dragon(ctx):
    if random.randint(1,3) // 3:    # True == 1 in python. If the number is a 3, do next line
        await ctx.send("Dragon this ligma!")
    else:
        await ctx.send("!ligma")


@bot.command(name="version", help="Tells version of bot (mostly for dubugging) which is version " + version_num)    # helps test to see if I remembered to update the bot
async def version(ctx):
    await ctx.send("Version " + version_num)


@bot.command(name="calc", help="Accepts operations '+','-','*','/', and '**' with numbers on either side seperated with a space")
async def calc(ctx, *args):  # calculation made for inputs
    if len(args) != 3:
        await ctx.send("Invalid Input. There should be 3 arguments afte !calc. Ex: !calc -3 + 5.7")
    try:
        float(args[0])
    except Exception as e:
        await ctx.send("Invalid Number. First number is invalid")
        return
    try:
        float(args[2])
    except Exception as e:
        await ctx.send("Invalid Number. Second number is invalid")
        return
    if args[1] == "+":
        await ctx.send(args[0] + " + " + args[2] + " = " + str(float(args[0]) + float(args[2])))
    elif args[1] == "-":
        await ctx.send(args[0] + " - " + args[2] + " = " + str(float(args[0]) - float(args[2])))
    elif args[1] == "*":
        await ctx.send(args[0] + " * " + args[2] + " = " + str(float(args[0]) * float(args[2])))
    elif args[1] == "/":
        await ctx.send(args[0] + " / " + args[2] + " = " + str(float(args[0]) / float(args[2])))
    elif args[1] == "**":
        await ctx.send(args[0] + " ** " + args[2] + " = " + str(float(args[0]) ** float(args[2])))
    else:
        await ctx.send("Invalid Operation. Accpeted operations are '+','-','*','/', and '**' with numbers on either side seperated with a space")


connect4Dict = {}
@bot.command(name="play", help="Play connect 4 with me")
async def play(ctx, column: int = 0):  # column chosen to drop
    global connect4Dict
    userID = ctx.author
    board = connect4Dict.get(userID, emptyBoard)
    if connect4Dict.get(userID):    # if board is set, continues game
        if column < 1 or column > 7:
            await ctx.send("Invalid Column. Chose a column 1-7")
            return
        await updateBoard(ctx, board, column)
        await computerTurn(ctx, board, 1)
    else:   # if board is empty, new game logic
        await ctx.send("Starting new game")
        connect4Dict[userID] = emptyBoard
        if column < 1 or column > 7:
            await ctx.send("I'll go first")    # if bad/no input is given, computer starts first
            await computerTurn(ctx, emptyBoard, random.randint(1,7))
        else:
            await ctx.send("You go first")
            await updateBoard(ctx, emptyBoard, column)
            await computerTurn(ctx, connect4Dict.get(userID), random.randint(1,7))


async def updateBoard(ctx, board, column):
    global connect4Dict
    newBoard = board    # test if variable newBoard is needed later
    depth = 6
    try:
        while newBoard[depth - 1][column - 1]!='-':
            depth-=1
    except Exception as IndexError:
        await ctx.send("Column is full. Pick another column")
    newBoard[depth - 1][column - 1] = 'o'
    connect4Dict[ctx.author] = newBoard     # updates board
    if depth == 0:  # checks if all spots are full
        if '-' not in newBoard[0]:
            await ctx.send("The game is a draw")
            await printBoard(ctx, newBoard)
            times.sleep(3)
            await ctx.send("Use !play to play again")
            connect4Dict[ctx.author] = NULL
            return
    y = depth - 1   # win logic variables
    x = column - 1
    if await isWon(ctx, newBoard, x, y):    # calls win logic
        await ctx.send("You win!")
        connect4Dict[ctx.author] = NULL       
    # updates board
    await printBoard(ctx, newBoard)
    print("board updated on player turn")


async def computerTurn(ctx, board, column):
    global connect4Dict
    print("Start computer turn")
    if connect4Dict[ctx.author] == NULL:
        return
    newBoard = board    # test if variable newBoard is needed later
    depth = 6
    try:
        while newBoard[depth - 1][column - 1]!='-':
            depth-=1
    except Exception as IndexError:
        await computerTurn(ctx, board, random.randint(1,7))   # if computer move is invalid, try again
        return
    newBoard[depth - 1][column - 1] = 'x'    
    connect4Dict[ctx.author] = newBoard     # updates board
    if depth == 0:  # checks if all spots are full
        if '-' not in newBoard[0]:
            await ctx.send("The game is a draw")
            await printBoard(ctx, newBoard)
            times.sleep(3)
            await ctx.send("Use !play to play again")
            connect4Dict[ctx.author] = NULL
            return
    await ctx.send("Computer turn")
    y = depth - 1   # win logic variables
    x = column - 1
    if await isWon(ctx, newBoard, x, y):    # calls win logic
        await ctx.send("Computer wins!")
        connect4Dict[ctx.author] = NULL        
    await printBoard(ctx, newBoard)
    print("board updated on comptuer turn")


async def isWon(ctx, newBoard, x, y):   # win logic is hard to explain without visuals. Only 13 ways to win because you can't drop below your own pieces
    try:
        if newBoard[y][x] == newBoard[y - 1][x - 1] and newBoard[y - 1][x - 1] == newBoard[y - 2][x - 2] and newBoard[y - 2][x - 2] == newBoard[y - 3][x - 3]:            
            return True
    except Exception as IndexError:
        pass
    try:
        if newBoard[y][x] == newBoard[y - 1][x + 1] and newBoard[y - 1][x + 1] == newBoard[y - 2][x + 2] and newBoard[y - 2][x + 2] == newBoard[y - 3][x + 3]:
            return True
    except Exception as IndexError:
        pass
    if y < 5:
        try:
            if newBoard[y + 1][x - 1] == newBoard[y][x] and newBoard[y][x] == newBoard[y - 1][x + 1] and newBoard[y - 1][x + 1] == newBoard[y - 2][x + 2]:
                return True
        except Exception as IndexError:
            pass
        try:
            if newBoard[y + 1][x + 1] == newBoard[y][x] and newBoard[y][x] == newBoard[y - 1][x - 1] and newBoard[y - 1][x - 1] == newBoard[y - 2][x - 2]:
                return True
        except Exception as IndexError:
            pass
    if y < 4:
        try:
            if newBoard[y + 2][x - 2] == newBoard[y + 1][x - 1] and newBoard[y + 1][x - 1] == newBoard[y][x] and newBoard[y][x] == newBoard[y - 1][x + 1]:
                return True
        except Exception as IndexError:
            pass
        try:
            if newBoard[y + 2][x + 2] == newBoard[y + 1][x + 1] and newBoard[y + 1][x + 1] == newBoard[y][x] and newBoard[y][x] == newBoard[y - 1][x - 1]:
                return True
        except Exception as IndexError:
            pass
    if y < 3:
        if newBoard[y + 3][x] == newBoard[y + 2][x] and newBoard[y + 2][x] == newBoard[y + 1][x] and newBoard[y + 1][x] == newBoard[y][x]:
            return True
        try:
            if newBoard[y + 3][x - 3] == newBoard[y + 2][x - 2] and newBoard[y + 2][x - 2] == newBoard[y + 1][x - 1] and newBoard[y + 1][x - 1] == newBoard[y][x]:
                return True
        except Exception as IndexError:
            pass 
        try:
            if newBoard[y + 3][x + 3] == newBoard[y + 2][x + 2] and newBoard[y + 2][x + 2] == newBoard[y + 1][x + 1] and newBoard[y + 1][x + 1] == newBoard[y][x]:
                return True
        except Exception as IndexError:
            pass 
    try:
        if newBoard[y][x - 3] == newBoard[y][x - 2] and newBoard[y][x - 2] == newBoard[y][x - 1] and newBoard[y][x - 1] == newBoard[y][x]:
            return True
    except Exception as IndexError:
        pass 
    try:
        if newBoard[y][x + 3] == newBoard[y][x + 2] and newBoard[y][x + 2] == newBoard[y][x + 1] and newBoard[y][x + 1] == newBoard[y][x]:
            return True
    except Exception as IndexError:
        pass 
    try:
        if newBoard[y][x + 2] == newBoard[y][x + 1] and newBoard[y][x + 1] == newBoard[y][x] and newBoard[y][x] == newBoard[y][x - 1]:
            return True
    except Exception as IndexError:
        pass 
    try:
        if newBoard[y][x - 2] == newBoard[y][x - 1] and newBoard[y][x - 1] == newBoard[y][x] and newBoard[y][x] == newBoard[y][x + 1]:
            return True
    except Exception as IndexError:
        pass
    return False

    
async def printBoard(ctx, board):
    for row in board:
        toSend = "|     "
        for item in row:
            toSend+= item + "     "
        toSend += "|"
        await ctx.send(toSend)


@bot.command(name="resetBoard", help="Resets connect4 board")
async def play(ctx):  # column chosen to drop
    connect4Dict[ctx.author] = NULL
    await ctx.send("Board reset")


with open("BOT_TOKEN.txt", "r") as token_file:
    TOKEN = token_file.read()
    print("Read token file")
    print("Version " + version_num)
    bot.run(TOKEN)
