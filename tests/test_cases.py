import unittest
from unittest.mock import AsyncMock

from bet_bot.database_connection import DatabaseConnection
from bet_bot.place_bet import _place_bet
from bet_bot.accept_bet import _accept_bet


class BetBotTestCase(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.bot = AsyncMock()
        self.bot.db = DatabaseConnection(db_name="test_bets.db")

        self.challenging_user = AsyncMock()
        self.challenging_user.id = "1"
        self.challenging_user.mention = "<@ChallengingUser>"

        self.challenged_user = AsyncMock()
        self.challenged_user.id = "2"
        self.challenged_user.mention = "<@ChallengedUser>"

        self.date_str = "2023-12-21"

    async def asyncTearDown(self):
        # Clean up any resources or objects here
        self.clear_database()

    def clear_database(self):
        # Open a new connection to the database
        self.bot.db.cursor.execute("""DELETE FROM bets""")
        self.bot.db.conn.commit()

    async def _place_bet_challenge(self, predicate, value):
        mock_ctx = AsyncMock()
        mock_ctx.author = self.challenging_user

        await _place_bet(
            self.bot,
            mock_ctx,
            predicate,
            self.date_str,
            self.challenged_user,
            value
        )
        bet_id = self.bot.db.cursor.lastrowid
        return bet_id


    async def _accept_bet_challenge(self, bet_id):
        mock_ctx = AsyncMock()
        mock_ctx.author = self.challenged_user
        mock_ctx.send = AsyncMock()

        self.bot.fetch_user.side_effect = [self.challenging_user, self.challenged_user]

        await _accept_bet(
            self.bot,
            mock_ctx,
            bet_id,
        )
