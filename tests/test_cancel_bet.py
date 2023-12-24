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

    async def test_cancel_bet_initial_bet_not_yet_accepted(self):

        bet_id = await self._place_bet_challenge(predicate="The sky will be blue", value="$20")

        mock_ctx = AsyncMock()
        mock_ctx.author = self.challenging_user
        mock_ctx.send = AsyncMock()

        self.bot.fetch_user.side_effect = [self.challenging_user, self.challenged_user]

        await _cancel_bet(
            self.bot,
            mock_ctx,
            bet_id,
        )
        mock_ctx.send.assert_called_once_with(
            f'Bet {bet_id}: **"The sky will be blue"** was never accepted, and has now been successfully cancelled. '
            f'<@ChallengingUser> and <@ChallengedUser> are off the hook'
        )

    async def test_cancel_bet_initial_bet_was_accepted(self):

        bet_id = await self._place_bet_challenge(predicate="The sky will be blue", value="$20")

        mock_ctx = AsyncMock()
        mock_ctx.author = self.challenging_user
        mock_ctx.send = AsyncMock()

        self.bot.fetch_user.side_effect = [self.challenging_user, self.challenged_user]

        await _cancel_bet(
            self.bot,
            mock_ctx,
            bet_id,
        )
        mock_ctx.send.assert_called_once_with(
            f'Bet {bet_id}: **"The sky will be blue"** was never accepted, and has now been successfully cancelled. '
            f'<@ChallengingUser> and <@ChallengedUser> are off the hook'
        )
        bet_id = await self._place_bet_challenge(predicate="The sky will be blue", value="$20")

        await self._accept_bet_challenge(bet_id)

        mock_ctx = AsyncMock()
        mock_ctx.author = self.challenging_user
        mock_ctx.send = AsyncMock()

        self.bot.fetch_user.side_effect = [self.challenging_user, self.challenged_user, self.challenging_user, self.challenged_user]

        # First cancellation request
        await _cancel_bet(self.bot, mock_ctx, bet_id)
        mock_ctx.send.assert_called_once_with(
            "<@ChallengingUser> requested to cancel bet **'The sky will be blue'**. Hey <@ChallengedUser>! "
            f"Do you want to cancel? If so, respond by typing `$cancel-bet {bet_id}`"
        )

    async def test_cancel_bet_additional_request(self):
        bet_id = await self._place_bet_challenge(predicate="The sky will be blue", value="$20")

        await self._accept_bet_challenge(bet_id)

        mock_ctx = AsyncMock()
        mock_ctx.author = self.challenging_user
        mock_ctx.send = AsyncMock()

        self.bot.fetch_user.side_effect = [self.challenging_user, self.challenged_user, self.challenging_user, self.challenged_user]

        # First cancellation request
        await _cancel_bet(self.bot, mock_ctx, bet_id)

        # Subsequent cancellation request
        await _cancel_bet(self.bot, mock_ctx, bet_id)

        mock_ctx.send.assert_called_with(
            "<@ChallengingUser> requested to cancel bet **'The sky will be blue'** again. We heard you the first time!"
        )

    async def test_cancel_bet_confirmation(self):
        bet_id = await self._place_bet_challenge(predicate="The sky will be blue", value="$20")

        await self._accept_bet_challenge(bet_id)

        mock_ctx = AsyncMock()
        mock_ctx.author = self.challenging_user
        mock_ctx.send = AsyncMock()

        self.bot.fetch_user.side_effect = [self.challenging_user, self.challenged_user, self.challenging_user, self.challenged_user]

        # First cancellation request
        await _cancel_bet(self.bot, mock_ctx, bet_id)

        mock_ctx.author = self.challenged_user


        # Subsequent cancellation request
        await _cancel_bet(self.bot, mock_ctx, bet_id)

        mock_ctx.send.assert_called_with(
            f'Bet {bet_id}: **"The sky will be blue"** has been successfully cancelled. '
            '<@ChallengedUser> and <@ChallengingUser> are off the hook'
        )

if __name__ == '__main__':
    unittest.main()
