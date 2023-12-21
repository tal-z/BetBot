import unittest
from unittest.mock import AsyncMock

from bet_bot.place_bet import _place_bet
from bet_bot.database_connection import Database


class TestPlaceBetFunction(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.bot = AsyncMock()
        self.bot.db = Database(db_name="test_bets.db")

        self.yes_user = AsyncMock()
        self.yes_user.id = "1"
        self.yes_user.mention = "<@YesUser>"

        self.no_user = AsyncMock()
        self.no_user.id = "2"
        self.no_user.mention = "<@NoUser>"

        self.date_str = "2023-12-21"

    async def asyncTearDown(self):
        # Clean up any resources or objects here
        self.clear_database()

    def clear_database(self):
        # Open a new connection to the database
        self.bot.db.cursor.execute("""DELETE FROM bets""")
        self.bot.db.conn.commit()

    async def test_place_bet_success(self):
        mock_ctx = AsyncMock()
        mock_ctx.send = AsyncMock()

        await _place_bet(
            self.bot,
            mock_ctx,
            "Is this a test?",
            self.date_str,
            self.yes_user,
            self.no_user,
            "Some value"
        )
        # Assert that the message was sent successfully
        mock_ctx.send.assert_called_once_with(
            f'Bet placed successfully for {self.yes_user.mention} and {self.no_user.mention}!'
        )


if __name__ == '__main__':
    unittest.main()
