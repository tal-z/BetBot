from datetime import datetime
from zoneinfo import ZoneInfo

from view_bets import format_table


async def _daily_expiring_bets_check(self, CHANNEL_ID):
    print(f'Checking for bets expiring today')
    channel = self.get_channel(int(CHANNEL_ID))
    if channel is not None:
        today = datetime.now(tz=ZoneInfo("US/Eastern")).strftime('%Y-%m-%d')
        bets_query = self.db.cursor.execute('''
                    SELECT 
                        id,
                        predicate,
                        expiration_date,
                        challenging_user_id,
                        challenged_user_id,
                        value,
                        challenge_accepted 
                    FROM bets 
                    WHERE expiration_date = ? AND challenge_accepted = TRUE
                ''', (today,))
        expired_bets = bets_query.fetchall()

        formatted_bets = []
        for bet in expired_bets:
            formatted_bet = list(bet)
            # Get the actual User objects from the mentions or IDs
            yes_user = await self.fetch_user(int(formatted_bet[3]))
            no_user = await self.fetch_user(int(formatted_bet[4]))
            formatted_bet[3] = str(yes_user.display_name)
            formatted_bet[4] = str(no_user.display_name)
            formatted_bets.append(formatted_bet)

        if formatted_bets:
            column_names = ["id", "predicate", "expires_on", "challenging_user", "challenged_user", "value", "active"]
            table_str = format_table("Bets Expiring Today", column_names, formatted_bets)
            await channel.send(table_str)

            for id, question, expiration_date, yes_user_id, no_user_id, value, cancel_requested_by_id in expired_bets:
                # Get the actual User objects from the mentions or IDs
                yes_user = await self.fetch_user(int(yes_user_id))
                no_user = await self.fetch_user(int(no_user_id))
                message_str = (
                    f"Hey {yes_user.mention} and {no_user.mention}! "
                    f"Your bet on the question **'{question}'** expires today. "
                    f"Somebody owes somebody else {value}'"
                )
                await channel.send(message_str)