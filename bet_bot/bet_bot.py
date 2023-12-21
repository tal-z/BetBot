import os

from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks

from converters import DateConverter
from database_connection import Database
from place_bet import _place_bet
from view_bets import _view_bets
from cancel_bet import _cancel_bet
from daily_expiring_bets_check import _daily_expiring_bets_check

load_dotenv()

CHANNEL_ID = os.getenv("TEST_CHANNEL_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True


class BetBot(commands.Bot):
    def __init__(self, db_name='bets.db'):
        super().__init__(command_prefix='$', intents=intents)
        self.db = Database(db_name=db_name)

        @self.event
        async def on_ready():
            print(f'We have logged in as {self.user}')
            self.daily_expiring_bets_check.start()

        @self.event
        async def on_disconnect():
            self.db.conn.close()
            print(f'{self.user} disconnected. Database connection closed.')

        @self.command(name='place-bet')
        async def place_bet(ctx, question: str, expiration_date: DateConverter, yes_user: discord.User, no_user: discord.User, value: str):
            await _place_bet(self, ctx, question, expiration_date, yes_user, no_user, value)

        @self.command(name='view-bets')
        async def view_bets(ctx):
            await _view_bets(self, ctx)

        @self.command(name='cancel-bet')
        async def cancel_bet(ctx, bet_id: int):
            await _cancel_bet(self, ctx, bet_id)

    @tasks.loop(hours=24)
    async def daily_expiring_bets_check(self):
        await _daily_expiring_bets_check(self, CHANNEL_ID)



if __name__ == "__main__":
    bot = BetBot()
    bot.run(BOT_TOKEN)
