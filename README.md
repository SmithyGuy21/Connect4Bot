# Connect 4 Discord Bot

## Overview

Welcome to the Connect 4 Discord Bot! This bot allows users to play the classic game of Connect 4 against an AI directly within your Discord server. Challenge yourself and see if you can beat the AI by connecting four discs in a row!

## Features

- **Interactive Gameplay:** Play Connect 4 against an AI in real-time.
- **Easy-to-Use Commands:** Simple commands make it easy to start a game, make a move, and more.
- **Customizable Prefix:** Set a custom prefix for the bot to respond to, ensuring it integrates seamlessly with your server.

## Commands

- `!idea`: Get an idea from preset ideas to add to this robot.
- `!echo [text]`: Repeats what is said after the command.
- `!version`: Tells the version of the bot (mostly for debugging).
- `!calc [number] [operation] [number]`: Accepts operations '+', '-', '*', '/', and '**' with numbers on either side separated by a space.
- `!play [column]`: Play Connect 4 against the AI.
- `!resetBoard`: Resets the Connect 4 board for the current player.
- `!help`: Display the list of available commands.

## Installation

1. **Clone the Repository:**
   - Clone this repository to your local machine.

2. **Install Dependencies:**
   - Install the required dependencies using `pip install discord.py`.

3. **Set up the Bot:**
   - Obtain a Discord bot token and replace the placeholder in the code with your token.

4. **Run the Bot:**
   - Run the bot script to start the Connect 4 Discord Bot on your server.

## Example Usage

1. **Starting a Game:**
   - Use the command `!play [column]` to initiate a new Connect 4 game against the AI.

2. **Making a Move:**
   - After starting a game, use the command `!play [column]` to place your disc in the specified column.

3. **Checking the Board:**
   - Use `!resetBoard` to reset the Connect 4 board if needed.

4. **Ending a Game:**
   - If you want to end the game prematurely, use `!resetBoard`.

## License

This Connect 4 Discord Bot is provided under the [CC BY 4.0 International](https://creativecommons.org/licenses/by/4.0/) license. Feel free to replicate and modify the code for your own use while crediting me. The bot is available for educational and personal purposes.

Enjoy playing Connect 4 against the AI on your Discord server!
