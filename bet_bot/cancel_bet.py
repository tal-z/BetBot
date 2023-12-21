import sqlite3


async def _cancel_bet(self, ctx, bet_id):
    try:
        # Check if the user is part of the bet
        user_id = ctx.author.id
        bet_query = self.db.cursor.execute(
            'SELECT * FROM bets WHERE id = ? AND (yes_user_id = ? OR no_user_id = ?)',
            (bet_id, user_id, user_id)
        )
        bet = bet_query.fetchone()

        if not bet:
            await ctx.send(f'You are not part of the bet with ID {bet_id}. Cancellation request rejected.')

        else:
            yes_user = await self.fetch_user(int(bet[3]))
            no_user = await self.fetch_user(int(bet[4]))

            cancelling_user, other_user = (
                (yes_user, no_user)
                if user_id == yes_user.id
                else (no_user, yes_user)
            )

            # Check if bet cancellation has already been requested
            cancel_requested_by_id = bet[6]
            if not cancel_requested_by_id:
                # initial cancellation request
                self.db.cursor.execute('UPDATE bets SET cancel_requested = ? WHERE id = ?',
                                       (cancelling_user.id, bet_id,))
                self.db.conn.commit()
                await ctx.send(
                    f"{cancelling_user.mention} requested to cancel bet **'{bet[1]}'**. Hey {other_user.mention}! Do you want to cancel? If so, respond by typing `$cancel-bet {bet_id}`")
            elif str(cancelling_user.id) == cancel_requested_by_id:
                # duplicate cancellation request
                await ctx.send(
                    f"{cancelling_user.mention} requested to cancel bet **'{bet[1]}'** again. We heard you the first time!")
            elif str(other_user.id) == cancel_requested_by_id:
                # cancellation approval
                self.db.cursor.execute('DELETE FROM bets WHERE id = ?', (bet_id,))
                self.db.conn.commit()
                await ctx.send(
                    f'Bet {bet_id}: **"{bet[1]}"** has been successfully cancelled. {cancelling_user.mention} and {other_user.mention} are off the hook')

    except sqlite3.Error as e:
        await ctx.send(f'Error cancelling bet: {e}')
