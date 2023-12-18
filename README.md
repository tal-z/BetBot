# Discord BetBot

## Overview

BetBot is a discord bot for keeping track of casual bets between friends within a Discord server. 
Users can place bets by providing details such as the question, expiration date, involved users, and the bet value. 
When a bet expires, the bot sends a message to a specified channel to notify the participants.

## Features

- **Place Bet:** Users can place bets using the `$place-bet` command, providing details like the question, expiration date, involved users, and the bet value.

- **View Bets:** The `$view-bets` command allows users to see a list of bets that are still active, i.e., those whose expiration date is on or after the current date.

- **Daily Check:** The bot automatically checks for bets expiring on the current day and notifies a specified channel about the details of these expiring bets.

## Setup

1. **Dependencies:**
   - Ensure you have [Pipenv](https://pipenv.pypa.io/en/latest/) installed.
   - Install required Python packages by running: `pipenv install`

2. **Database Setup:**
   - The bot uses SQLite for storing bet information. The database file (`bets.db`) is created automatically if it does not exist.

3. **Discord Bot Token:**
   - Create a new Discord bot on the [Discord Developer Portal](https://discord.com/developers/applications).
   - Copy the bot token and set it as the value for the `BOT_TOKEN` variable in the `.env` file.

4. **Channel Configuration:**
   - Set the channel ID for the channel where daily bet expiration notifications will be sent as the value for the `TEST_CHANNEL_ID` variable in the `.env` file.

5. **Run the Bot:**
   - Activate the virtual environment: `pipenv shell`
   - Execute the bot script using: `python bet_bot.py`

## Commands

- **Place Bet:**
  - Syntax: `$place-bet <question> <expiration_date> <yes_user> <no_user> <value>`
  - Example: `$place-bet "Will it rain tomorrow?" "2023-12-31" @user1 @user2 50`

- **View Bets:**
  - Syntax: `$view-bets`
  - Example: `$view-bets`

## Contributions and Issues

Contributions to the project are welcome. 
If you encounter any issues or have suggestions for improvements, please open an issue in GitHub.

