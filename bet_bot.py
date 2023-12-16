"""import os
from datetime import datetime, timedelta

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv


load_dotenv()

CHANNEL_ID = os.getenv("CHANNEL_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Create a connection to SQLite database
conn = sqlite3.connect('bets.db')
cursor = conn.cursor()

# Create a table to store bets
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        expiration_date TEXT,
        yes_user TEXT,
        no_user TEXT,
        value INTEGER
    )
''')
conn.commit()

# Set up the Discord bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='place-bet')
async def place_bet(ctx, question, expiration_date, yes_user, no_user, value):
    # Store bet in the SQLite database
    cursor.execute('''
        INSERT INTO bets (question, expiration_date, yes_user, no_user, value)
        VALUES (?, ?, ?, ?, ?)
    ''', (question, expiration_date, yes_user, no_user, value))
    conn.commit()

    await ctx.send('Bet placed successfully!')

# Task to check for expired bets and send reminders
@tasks.loop(seconds=60)
async def check_expired_bets():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    expired_bets = cursor.execute('SELECT * FROM bets WHERE expiration_date <= ?', (current_time,)).fetchall()

    for bet in expired_bets:
        bet_id, question, _, _, _, _ = bet
        channel = bot.get_channel(CHANNEL_ID)  # Replace with your Discord channel ID
        await channel.send(f'Bet "{question}" has expired!')

# Start the task
check_expired_bets.start()

# Run the bot
bot.run(BOT_TOKEN)  # Replace with your Discord bot token
"""

import os
import sqlite3

from dotenv import load_dotenv
import discord
from discord.ext import commands



# Create a connection to SQLite database
conn = sqlite3.connect('bets.db')
cursor = conn.cursor()

# Create a table to store bets
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        expiration_date TEXT,
        yes_user TEXT,
        no_user TEXT,
        value INTEGER
    )
''')
conn.commit()

load_dotenv()

CHANNEL_ID = os.getenv("CHANNEL_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command(name='place-bet')
async def place_bet(ctx, question, expiration_date, yes_user, no_user, value):
    await ctx.send('Bet received successfully!')
    # Store bet in the SQLite database
    cursor.execute('''
        INSERT INTO bets (question, expiration_date, yes_user, no_user, value)
        VALUES (?, ?, ?, ?, ?)
    ''', (question, expiration_date, yes_user, no_user, value))
    conn.commit()
    await ctx.send('Bet placed successfully!')


def format_table(column_names, data):
    column_widths = {}
    for col_idx, column in enumerate(column_names):
        column_widths[col_idx] = len(column) + 2
        for row in data:
            column_value_len = len(str(row[col_idx]))
            column_widths[col_idx] = max(column_value_len + 2, column_widths[col_idx])

    table_str = ""

    header_str = ""
    for col_idx, col_name in enumerate(column_names):
        whitespace = column_widths[col_idx] - len(col_name)
        header_str += col_name + (" " * whitespace) + "|"

    table_str += header_str + "\n"

    for row in data:
        row_str = ""
        for col_idx, col_value in enumerate(row):
            col_value = str(col_value)
            whitespace = column_widths[col_idx] - len(col_value)
            row_str += col_value + (" " * whitespace) + "|"
        table_str += row_str + "\n"

    return f"`{table_str}`"


@bot.command(name='view-bets')
async def view_bets(ctx):
    # Store bet in the SQLite database
    bets_query = cursor.execute('''
        SELECT * from bets
    ''')
    bets = bets_query.fetchall()

    column_names = ["id", "question", "expiration_date", "yes_user", "no_user", "value"]
    table_str = format_table(column_names, bets)
    await ctx.send(table_str)



bot.run(BOT_TOKEN)
