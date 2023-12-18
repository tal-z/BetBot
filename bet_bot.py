import os
import sqlite3
from datetime import datetime

from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks

from utils import format_table
from converters import DateConverter
from database_connection import Database


load_dotenv()

CHANNEL_ID = os.getenv("TEST_CHANNEL_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)
db = Database()


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    daily_check.start()


@bot.event
async def on_disconnect():
    db.conn.close()
    print(f'{bot.user} disconnected. Database connection closed.')


@bot.command(name='place-bet')
async def place_bet(ctx, question: str, expiration_date: DateConverter, yes_user: discord.User, no_user: discord.User, value: str):
    if not all([question, expiration_date, yes_user, no_user, value]):
        await ctx.send('Please provide all required arguments.')
        return

    try:
        db.cursor.execute('''
            INSERT INTO bets (question, expiration_date, yes_user_id, no_user_id, value)
            VALUES (?, ?, ?, ?, ?)
        ''', (question, expiration_date, yes_user.id, no_user.id, value))
        db.conn.commit()
        await ctx.send(f'Bet placed successfully for {yes_user.mention} and {no_user.mention}!')
    except (discord.errors.NotFound, sqlite3.Error) as e:
        await ctx.send(f'Error placing bet: {e}')


@bot.command(name='view-bets')
async def view_bets(ctx):
    # Store bet in the SQLite database
    today = datetime.utcnow().strftime('%Y-%m-%d')

    bets_query = db.cursor.execute('''
        SELECT * FROM bets
    ''')
    bets = bets_query.fetchall()

    formatted_bets = []
    for bet in bets:
        formatted_bet = list(bet)
        # Get the actual User objects from the mentions or IDs
        yes_user = await bot.fetch_user(int(formatted_bet[3]))
        no_user = await bot.fetch_user(int(formatted_bet[4]))
        formatted_bet[3] = str(yes_user.display_name)
        formatted_bet[4] = str(no_user.display_name)
        formatted_bets.append(formatted_bet)

    column_names = ["id", "question", "expiration_date", "yes_user", "no_user", "value"]
    table_str = format_table("Placed Bets", column_names, formatted_bets)
    await ctx.send(table_str)

@tasks.loop(hours=24)
async def daily_check():
    print(f'Checking for bets expiring today')
    channel = bot.get_channel(int(CHANNEL_ID))
    if channel is not None:
        today = datetime.utcnow().strftime('%Y-%m-%d')
        bets_query = db.cursor.execute('''
            SELECT * FROM bets WHERE expiration_date = ?
        ''', (today,))
        expired_bets = bets_query.fetchall()

        formatted_bets = []
        for bet in expired_bets:
            formatted_bet = list(bet)
            # Get the actual User objects from the mentions or IDs
            yes_user = await bot.fetch_user(int(formatted_bet[3]))
            no_user = await bot.fetch_user(int(formatted_bet[4]))
            formatted_bet[3] = str(yes_user.display_name)
            formatted_bet[4] = str(no_user.display_name)
            formatted_bets.append(formatted_bet)

        if formatted_bets:
            column_names = ["id", "question", "expiration_date", "yes_user", "no_user", "value"]
            table_str = format_table("Bets Expiring Today", column_names, formatted_bets)
            await channel.send(table_str)

            for id, question, expiration_date, yes_user_id, no_user_id, value in expired_bets:
                # Get the actual User objects from the mentions or IDs
                yes_user = await bot.fetch_user(int(yes_user_id))
                no_user = await bot.fetch_user(int(no_user_id))
                message_str = f"Hey {yes_user.mention} and {no_user.mention}! Your bet on the question **'{question}'** expires today. Somebody owes somebody else {value}'"
                await channel.send(message_str)


@daily_check.before_loop
async def before_daily_check():
    await bot.wait_until_ready()

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
