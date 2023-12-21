from datetime import datetime
from utils import format_table


async def _view_bets(self, ctx):
    bets_query = self.db.cursor.execute('''
                    SELECT * FROM bets
                ''')
    bets = bets_query.fetchall()

    formatted_bets = []
    for bet in bets:
        formatted_bet = list(bet)
        # Get the actual User objects from the mentions or IDs
        yes_user = await self.fetch_user(int(formatted_bet[3]))
        no_user = await self.fetch_user(int(formatted_bet[4]))
        formatted_bet[3] = str(yes_user.display_name)
        formatted_bet[4] = str(no_user.display_name)
        formatted_bets.append(formatted_bet)

    column_names = ["id", "question", "expiration_date", "yes_user", "no_user", "value",
                    "cancellation_requested"]
    table_str = format_table("Placed Bets", column_names, formatted_bets)
    await ctx.send(table_str)
