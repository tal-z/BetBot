import unittest
from unittest.mock import AsyncMock

from test_cases import BetBotTestCase

from bet_bot.place_bet import _place_bet


class TestPlaceBetFunction(BetBotTestCase):

    async def asyncSetUp(self):
        await super().asyncSetUp()

    async def test_place_bet_success(self):
        mock_ctx = AsyncMock()
        mock_ctx.author = self.challenging_user
        mock_ctx.send = AsyncMock()

        predicate = "Cats will take over the world"
        value = "50 doubloons"

        await _place_bet(
            self.bot,
            mock_ctx,
            predicate,
            self.date_str,
            self.challenged_user,
            value
        )
        # Assert that the message was sent successfully
        mock_ctx.send.assert_called_once_with(
            f'Hey {self.challenged_user.mention}! {self.challenging_user.mention} challenged you to a bet. '
            f'{self.challenging_user.mention} thinks that **"{predicate}"**, and wants to wager {value} over it. '
            f'If you want to accept the bet, please respond by sending `$accept-bet {self.bot.db.cursor.lastrowid}`')

    async def test_place_bet_missing_arguments(self):
        mock_ctx = AsyncMock()
        mock_ctx.send = AsyncMock()

        # Missing one or more arguments
        await _place_bet(self.bot, mock_ctx, None, None, None, None)

        # Assert that the message about missing arguments was sent
        mock_ctx.send.assert_called_once_with('Please provide all required arguments.')


if __name__ == '__main__':
    unittest.main()
