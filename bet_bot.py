import os
import sqlite3
from datetime import datetime

from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks

from utils import format_table


load_dotenv()

# Create a connection to SQLite database
with sqlite3.connect('bets.db') as conn:
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


CHANNEL_ID = os.getenv("TEST_CHANNEL_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    daily_check.start()


@bot.event
async def on_disconnect():
    conn.close()
    print(f'{bot.user} disconnected. Database connection closed.')


@bot.command(name='place-bet')
async def place_bet(ctx, question, expiration_date, yes_user, no_user, value):
    if not all([question, expiration_date, yes_user, no_user, value]):
        await ctx.send('Please provide all required arguments.')
        return

    try:
        cursor.execute('''
            INSERT INTO bets (question, expiration_date, yes_user, no_user, value)
            VALUES (?, ?, ?, ?, ?)
        ''', (question, expiration_date, yes_user, no_user, value))
        conn.commit()
        await ctx.send('Bet placed successfully!')
    except sqlite3.Error as e:
        await ctx.send(f'Error placing bet: {e}')


@bot.command(name='view-bets')
async def view_bets(ctx):
    # Store bet in the SQLite database
    today = datetime.utcnow().strftime('%Y-%m-%d')

    bets_query = cursor.execute('''
        SELECT * FROM bets WHERE expiration_date >= ?
    ''', (today,))
    bets = bets_query.fetchall()

    column_names = ["id", "question", "expiration_date", "yes_user", "no_user", "value"]
    table_str = format_table("Placed Bets", column_names, bets)
    await ctx.send(table_str)

@tasks.loop(hours=24)
async def daily_check():
    channel = bot.get_channel(int(CHANNEL_ID))
    if channel is not None:
        today = datetime.utcnow().strftime('%Y-%m-%d')
        bets_query = cursor.execute('''
            SELECT * FROM bets WHERE expiration_date = ?
        ''', (today,))
        expired_bets = bets_query.fetchall()

        if expired_bets:
            column_names = ["id", "question", "expiration_date", "yes_user", "no_user", "value"]
            table_str = format_table("Bets Expiring Today", column_names, expired_bets)
            await channel.send(table_str)


@daily_check.before_loop
async def before_daily_check():
    await bot.wait_until_ready()

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
