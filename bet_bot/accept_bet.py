import sqlite3
import discord


async def _accept_bet(self, ctx, bet_id: int):
    try:
        accepting_user = ctx.author
        bet_query = self.db.cursor.execute(
            'SELECT * FROM bets WHERE id = ? AND (challenged_user_id = ?)',
            (bet_id, accepting_user.id)
        )
        bet = bet_query.fetchone()
        if not bet:
            await ctx.send(
                "You tried to accept a bet, but we couldn't find the bet you are looking for! "
                "Or, maybe it was meant for somebody else. Perhaps try placing a bet of your own."
            )
            return

        self.db.cursor.execute(
            'UPDATE bets SET challenge_accepted = TRUE WHERE id = ?',
            (bet_id,)
        )
        self.db.conn.commit()

        challenging_user = await self.fetch_user(int(bet[3]))
        bet_value = bet[5]

        await ctx.send(
            f'Woohoo! {accepting_user.mention} accepted {challenging_user.mention}\'s bet '
            f'**"{bet[1]}"** for {bet_value}. It\'s on!'
        )

    except (discord.errors.NotFound, sqlite3.Error) as e:
        await ctx.send(f'Error accepting bet: {e}')
