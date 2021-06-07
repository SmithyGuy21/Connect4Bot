from os import times
import random
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
version_num = "1.4" # helps to keep track of updates while running program and in discord
emptyBoard = [['-','-','-','-','-','-'], ['-','-','-','-','-','-'], ['-','-','-','-','-','-'], ['-','-','-','-','-','-'], ['-','-','-','-','-','-'], ['-','-','-','-','-','-'], ['-','-','-','-','-','-']]

@bot.command(name="idea", help="Get idea from preset ideas to add to this robot")
async def idea(ctx):
    lines = open("Discord Bot.txt", "r").read().split("\n")
    await ctx.send("Add a feature to me: " + random.choice(lines))


@bot.command(name="copyMe", help="Repeats what is said after the command")
async def copyMe(ctx, *, args=""):
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


@bot.command(name="dragon", hidden=True)
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
    if connect4Dict.get(userID):
        await updateBoard(ctx, board, column)
        connect4Dict[userID] = computerTurn(ctx, board, random.randint(1,7))
    else:
        await ctx.send("Starting new game")
        connect4Dict[userID] = emptyBoard
        #if random.getrandbits(1):
        if False:
            await ctx.send("I'll go first")
            connect4Dict[userID] = computerTurn(ctx, emptyBoard, random.randint(1,7))
        else:
            await ctx.send("You go first")
            if column == 0:
                await printBoard(ctx, emptyBoard)
            else:
                await updateBoard(ctx, emptyBoard, column)
                connect4Dict[userID] = computerTurn(ctx, emptyBoard, random.randint(1,7))



async def updateBoard(ctx, board, column):
    newBoard = board    # test if variable newBoard is needed later
    depth = 7
    try:
        while newBoard[depth - 1][column - 1]!='-':
            depth-=1
    except Exception as IndexError:
        await ctx.send("depth:" + depth)
        await ctx.send("Column:" + column)       
        await ctx.send("newBoard:" + newBoard)       
        await ctx.send("Column is full. Pick another column")
    newBoard[depth - 1][column - 1] = 'o'
    if depth == 0:
        if '-' not in newBoard[0]:
            await ctx.send("The game is a draw")
            await printBoard(ctx, newBoard)
            times.sleep(3)
            await ctx.send("Use !play to play again")
            connect4Dict[ctx.author] = emptyBoard
            return
    connect4Dict[ctx.author] = newBoard
    await printBoard(ctx, newBoard)
    print("board updated")


async def computerTurn(ctx, board, column):
    newBoard = board    # test if variable newBoard is needed later
    depth = 7
    try:
        while newBoard[depth - 1][column - 1]!='-':
            depth-=1
    except Exception as IndexError:
        await ctx.send("Column is full. Pick another column")
    newBoard[depth - 1][column - 1] = 'x'
    if depth == 0:
        if '-' not in newBoard[0]:
            await ctx.send("The game is a draw")
            await printBoard(ctx, newBoard)
            times.sleep(3)
            await ctx.send("Use !play to play again")
            connect4Dict[ctx.author] = emptyBoard
            return
    connect4Dict[ctx.author] = newBoard
    await printBoard(ctx, newBoard)
    print("board updated")


async def printBoard(ctx, board):
    for row in board:
        toSend = "|     "
        for item in row:
            toSend+= item + "     "
        toSend += "|"
        await ctx.send(toSend)
    


with open("BOT_TOKEN.txt", "r") as token_file:
    TOKEN = token_file.read()
    print("Read token file")
    print("Version " + version_num)
    bot.run(TOKEN)
