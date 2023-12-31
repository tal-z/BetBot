# Discord BetBot

## Overview

BetBot is a discord bot for keeping track of casual bets between friends within a Discord server. 
Users can place bets by providing details such as the question, expiration date, involved users, and the bet value. 
When a bet expires, the bot sends a message to a specified channel to notify the participants so that they may settle up.
   
## Commands

- **Place Bet:**
  - Syntax: `$place-bet <predicate> <expiration_date> <challenged_user> <value>`
  - Example: `$place-bet "Will it rain tomorrow?" "2023-12-31" @user1 @user2 50`

- **Accept Bet:**
  - Syntax: `$accept-bet <bet_id>`
  - Example: `$accept-bet 1>`

- **View Bets:**
  - Syntax: `$view-bets`
  - Example: `$view-bets`

- **Cancel Bet:**
  - Syntax: `$cancel-bet <bet_id>`
  - Example: `$cancel-bet 1`

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
  - Syntax: `$place-bet <predicate> <expiration_date> <challenged_user> <value>`
  - Example: `$place-bet "Will it rain tomorrow?" "2023-12-31" @user1 @user2 50`

- **Accept Bet:**
  - Syntax: `$accept-bet <bet_id>`
  - Example: `$accept-bet 1>`

- **View Bets:**
  - Syntax: `$view-bets`
  - Example: `$view-bets`

- **Cancel Bet:**
  - Syntax: `$cancel-bet <bet_id>`
  - Example: `$cancel-bet 1`

## Running tests

From the project root, run `python -m unittest discover tests`

## Deployment
1. Spin up EC2 instance
2. Connect to EC2 instance from local: `ssh -i <path-to-pem-file> ec2-user@<public-ip-address>`
3. Update packages: `sudo yum update`
4. Install python: `sudo yum install python3-pip`
5. Install git: `sudo yum install git`
6. Clone repo: `git clone https://github.com/tal-z/BetBot.git`
7. cd into the repo: `cd BetBot`
8. Install pipenv: `pip3 install pipenv`
9. Install dependencies: `pipenv --python python3.9 install --dev`
10. Update environment variables 
11. Install tmux: `sudo yum install tmux` 
12. Active pipenv environment: `pipenv shell`
13. Start new tmux process: `tmux new -s BetBot`
14. Start the bot: `python3 bet_bot/bet_bot.py`
15. Exit the tmux shell by entering `ctrl+b` followed by `d` on your keyboard
16. To re-attach: `tmux attach` or `tmux attach -d -t BetBot` if there is more than one process running

## Contributions and Issues

Contributions to the project are welcome. 
If you encounter any issues or have suggestions for improvements, please open an issue in GitHub.

