import sqlite3
import discord

from bet_bot.converters import DateConverter


async def _place_bet(self, ctx, question: str, expiration_date: DateConverter, yes_user: discord.User, no_user: discord.User, value: str):
    if not all([question, expiration_date, yes_user, no_user, value]):
        await ctx.send('Please provide all required arguments.')
        return

    try:
        self.db.cursor.execute('''
            INSERT INTO bets (question, expiration_date, yes_user_id, no_user_id, value, cancel_requested)
            VALUES (?, ?, ?, ?, ?, NULL)
        ''', (question, expiration_date, yes_user.id, no_user.id, value))
        self.db.conn.commit()
        await ctx.send(f'Bet placed successfully for {yes_user.mention} and {no_user.mention}!')
    except (discord.errors.NotFound, sqlite3.Error) as e:
        await ctx.send(f'Error placing bet: {e}')
