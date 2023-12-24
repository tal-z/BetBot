import unittest
from unittest.mock import AsyncMock

from bet_bot.place_bet import _place_bet
from bet_bot.accept_bet import _accept_bet

from test_cases import BetBotTestCase


class TestPlaceBetFunction(BetBotTestCase):

    async def asyncSetUp(self):
        await super().asyncSetUp()

    async def test_accept_bet_success(self):
        predicate = "The sky will be blue"
        value = "$10"
        bet_id = await self._place_bet_challenge(predicate=predicate, value=value)

        mock_ctx = AsyncMock()
        mock_ctx.author = self.challenged_user
        mock_ctx.send = AsyncMock()

        self.bot.fetch_user.return_value = self.challenging_user

        await _accept_bet(
            self.bot,
            mock_ctx,
            bet_id,
        )

        mock_ctx.send.assert_called_once_with(
            f'Woohoo! {self.challenged_user.mention} accepted {self.challenging_user.mention}\'s bet '
            f'**"{predicate}"** for {value}. It\'s on!')

    async def test_accept_bet_not_issued_to_user(self):
        predicate = "The sky will be blue"
        value = "$10"
        bet_id = await self._place_bet_challenge(predicate=predicate, value=value)

        mock_ctx = AsyncMock()
        mock_ctx.author = AsyncMock(id="3")  # Another user
        mock_ctx.send = AsyncMock()

        await _accept_bet(
            self.bot,
            mock_ctx,
            bet_id,
        )

        mock_ctx.send.assert_called_once_with(
            "You tried to accept a bet, but we couldn't find the bet you are looking for! "
            "Or, maybe it was meant for somebody else. Perhaps try placing a bet of your own."
        )

    async def test_accept_bet_not_found(self):
        bet_id = 999  # Non-existent bet ID

        mock_ctx = AsyncMock()
        mock_ctx.author = self.challenged_user
        mock_ctx.send = AsyncMock()

        await _accept_bet(
            self.bot,
            mock_ctx,
            bet_id,
        )

        mock_ctx.send.assert_called_once_with(
            "You tried to accept a bet, but we couldn't find the bet you are looking for! "
            "Or, maybe it was meant for somebody else. Perhaps try placing a bet of your own."
        )


if __name__ == '__main__':
    unittest.main()
