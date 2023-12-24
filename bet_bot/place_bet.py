import sqlite3
from datetime import datetime

import discord
from discord.ext.commands import Converter, BadArgument
#from bet_bot.converters import DateConverter


class DateConverter(Converter):
    """
    Convert a string to a Python date object.

    Parameters:
    - date_string (str): Input date string in various formats.

    Returns:
    - date_object (datetime.date): Python date object.
    - If the conversion fails, returns None.
    """
    supported_formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y%m%d",
        "%d-%m-%Y",
        "%m-%d-%Y",
        "%d/%m/%Y",
        "%m/%d/%Y",
    ]

    @classmethod
    async def convert(cls, ctx, date_string):

        for date_format in cls.supported_formats:
            try:
                date_object = datetime.strptime(date_string, date_format).date()
                return date_object
            except ValueError:
                pass

        # If none of the formats matched
        await ctx.send(f'Error placing bet: Unable to parse the date string.')
        raise BadArgument


async def _place_bet(self, ctx, predicate: str, expiration_date: DateConverter, challenged_user: discord.User, value: str):
    if not all([predicate, expiration_date, challenged_user, value]):
        await ctx.send('Please provide all required arguments.')
        return

    try:
        challenging_user = ctx.author
        self.db.cursor.execute('''
            INSERT INTO bets (predicate, expiration_date, challenging_user_id, challenged_user_id, value, challenge_accepted, cancel_requested)
            VALUES (?, ?, ?, ?, ?, NULL, NULL)
        ''', (predicate, expiration_date, challenging_user.id, challenged_user.id, value))
        self.db.conn.commit()

        bet_id = self.db.cursor.lastrowid

        await ctx.send(f'Hey {challenged_user.mention}! {challenging_user.mention} challenged you to a bet. '
                       f'{challenging_user.mention} thinks that **"{predicate}"**, and wants to wager {value} over it. '
                       f'If you want to accept the bet, please respond by sending `$accept-bet {bet_id}`')
    except (discord.errors.NotFound, sqlite3.Error) as e:
        await ctx.send(f'Error placing bet: {e}')
