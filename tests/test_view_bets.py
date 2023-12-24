import unittest
from unittest.mock import AsyncMock

from bet_bot.view_bets import _view_bets, format_table

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

        table_name = "Placed Bets"
        header_row = [
            "id",
            "predicate",
            "expiration_date",
            "challenging_user",
            "challenged_user",
            "value",
            "challenge_accepted",
            "cancellation_requested",
        ]
        data_rows = [(
                bet_id,
                predicate,
                self.date_str,
                "ChallengingUser",
                "ChallengedUser",
                "$10",
                None,
                None,
        )]
        expected_table_str = format_table(table_name, header_row, data_rows)
        mock_ctx.send.assert_called_once_with(expected_table_str)


if __name__ == '__main__':
    unittest.main()
