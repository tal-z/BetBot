import unittest
from unittest.mock import AsyncMock

from bet_bot.cancel_bet import _cancel_bet

from test_cases import BetBotTestCase


class TestCancelBetFunction(BetBotTestCase):

    async def asyncSetUp(self):
        await super().asyncSetUp()

    async def test_cancel_bet_no_bet(self):
        bet_id = 99

        mock_ctx = AsyncMock()
        mock_ctx.author = self.challenging_user
        mock_ctx.send = AsyncMock()

        self.bot.fetch_user.side_effect = [self.challenging_user, self.challenged_user]

        await _cancel_bet(
            self.bot,
            mock_ctx,
            bet_id,
        )
        mock_ctx.send.assert_called_once_with('You are not part of the bet with ID 99. Cancellation request rejected.')


if __name__ == '__main__':
    unittest.main()
