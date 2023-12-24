
def format_table(table_name, column_names, data):
    column_widths = {}
    for col_idx, column in enumerate(column_names):
        column_widths[col_idx] = len(column) + 2
        for row in data:
            column_value_len = len(str(row[col_idx]))
            column_widths[col_idx] = max(column_value_len + 2, column_widths[col_idx])

    divider = (
            "_" * (sum(column_widths.values()) + len(column_names)*2)
            + "\n"
    )
    table_str = f"{table_name}\n{divider}"

    header_str = ""
    for col_idx, col_name in enumerate(column_names):
        whitespace = column_widths[col_idx] - len(col_name)
        header_str += f"{col_name}" + (" " * whitespace) + "| "

    table_str += f"{header_str}" + "\n" + divider

    for row in data:
        row_str = ""
        for col_idx, col_value in enumerate(row):
            col_value = str(col_value)
            whitespace = column_widths[col_idx] - len(col_value)
            row_str += col_value + (" " * whitespace) + "| "
        table_str += row_str + "\n" + divider

    return f"```{table_str}```"

async def _view_bets(self, ctx):
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
                ''')
    bets = bets_query.fetchall()

    print(bets)

    formatted_bets = []
    for bet in bets:
        formatted_bet = list(bet)
        # Get the actual User objects from the mentions or IDs
        yes_user = await self.fetch_user(int(formatted_bet[3]))
        no_user = await self.fetch_user(int(formatted_bet[4]))
        formatted_bet[3] = str(yes_user.display_name)
        formatted_bet[4] = str(no_user.display_name)
        formatted_bets.append(formatted_bet)

    column_names = [
        "id",
        "predicate",
        "expiration_date",
        "challenging_user",
        "challenged_user",
        "value",
        "active",
    ]
    table_str = format_table("Placed Bets", column_names, formatted_bets)
    await ctx.send(table_str)
