import unittest
from unittest.mock import AsyncMock

from bet_bot.view_bets import _view_bets

from test_cases import BetBotTestCase


class TestViewBetsFunction(BetBotTestCase):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.challenging_user.display_name = "ChallengingUser"
        self.challenged_user.display_name = "ChallengedUser"

    async def test_view_bets_success(self):
        predicate = "The sky will be blue"
        value = "$10"
        bet_id = await self._place_bet_challenge(predicate=predicate, value=value)

        mock_ctx = AsyncMock()
        mock_ctx.send = AsyncMock()

        self.bot.fetch_user.side_effect = [self.challenging_user, self.challenged_user]

        await _view_bets(
            self.bot,
            mock_ctx,
        )

        expected_table_str = (
            '```Placed Bets\n'
            '_________________________________________________________________________________________________________________________________________________\n'
            'id  | predicate             | expiration_date  | challenging_user  | challenged_user  | value  | challenge_accepted  | cancellation_requested  | \n'
            '_________________________________________________________________________________________________________________________________________________\n'
            f'{bet_id}  | The sky will be blue  | 2023-12-21       | ChallengingUser   | ChallengedUser   | $10    | None                | None                    | \n'
            '_________________________________________________________________________________________________________________________________________________\n```')
        mock_ctx.send.assert_called_once_with(expected_table_str)

    # Additional test cases can be added for different scenarios, such as empty bets, etc.


if __name__ == '__main__':
    unittest.main()
