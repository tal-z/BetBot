import os

from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
from discord.ext.commands import MissingRequiredArgument

from database_connection import Database
from place_bet import _place_bet, DateConverter
from accept_bet import _accept_bet
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

        @self.command(
            name='place-bet',
            help=(
                'Challenge another person to a bet. '
                'Syntax: `$place-bet <predicate> <expiration_date> <challenged_user> <value>`'
            )
        )
        async def place_bet(ctx, predicate: str, expiration_date: DateConverter, challenged_user: discord.User, value: str):
            await _place_bet(self, ctx, predicate, expiration_date, challenged_user, value)

        @self.command(
            name='accept-bet',
            help=(
                'Accept a bet from another person who challenged you. '
                'Syntax: `$accept-bet <bet_id>`'
            )
        )
        async def accept_bet(ctx, bet_id: int):
            await _accept_bet(self, ctx, bet_id)

        @self.command(
            name='view-bets',
            help=(
                    'View all active bets and open challenges.'
                    'Syntax: `$view-bets`'
            )
        )
        async def view_bets(ctx):
            await _view_bets(self, ctx)

        @self.command(
            name='cancel-bet',
            help=(
                    "Submit a request to cancel a bet, or confirm another person's request to cancel your bet."
                    "Syntax: `$cancel-bet <bet_id>`"
            )
        )
        async def cancel_bet(ctx, bet_id: int):
            await _cancel_bet(self, ctx, bet_id)

    async def on_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send(f"Error: {error}")
        else:
            print(error)

    @tasks.loop(hours=24)
    async def daily_expiring_bets_check(self):
        await _daily_expiring_bets_check(self, CHANNEL_ID)


if __name__ == "__main__":
    bot = BetBot()
    bot.run(BOT_TOKEN)
