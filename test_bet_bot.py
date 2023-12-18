import tracemalloc

import bet_bot

tracemalloc.start()

import unittest
from unittest.mock import AsyncMock, patch

from bet_bot import place_bet
from database_connection import Database


@patch("bet_bot.Database", return_value=Database(db_name='test_bets.db'))
class TestPlaceBetCommand(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Mock the necessary objects
        self.ctx = AsyncMock()
        self.ctx.send = AsyncMock()

    async def test_place_bet_success(self, test_db):
        # Prepare test data
        question = "Test question"
        expiration_date = "2023-12-31 12:00:00"
        yes_user = AsyncMock()
        yes_user.id = "1234"
        yes_user.mention = "@yes_user_mock_mention"
        no_user = AsyncMock()
        no_user.id = "5678"
        no_user.mention = "@no_user_mock_mention"
        value = "$100"

        # Call the function with the test data
        await place_bet(self.ctx, question, expiration_date, yes_user, no_user, value)

        # Assert that the send method was called with the correct message
        self.ctx.send.assert_called_once_with('Bet placed successfully for @yes_user_mock_mention and @no_user_mock_mention!')

    async def test_place_bet_missing_arguments(self, test_db):
        # Prepare test data
        question = ""
        expiration_date = ""
        yes_user = ""
        no_user = ""
        value = ""

        # Call the function without providing all required arguments
        await place_bet(self.ctx, question, expiration_date, yes_user, no_user, value)

        # Assert that the send method was called with the correct error message
        self.ctx.send.assert_called_once_with('Please provide all required arguments.')

    async def test_place_bet_missing_individual_arguments(self, test_db):
        arguments = ["question", "expiration_date", "yes_user", "no_user", "value"]
        for missing_argument in arguments:
            # Prepare test data with one missing argument
            test_data = dict(
                question="Test question",
                expiration_date="2023-12-31 12:00:00",
                yes_user=AsyncMock(),
                no_user=AsyncMock(),
                value="$100"
            )

            # Set the missing argument to an empty string
            test_data[missing_argument] = ""

            # Call the function with the test data
            await place_bet(self.ctx, **test_data)

            # Assert that the send method was called with the correct error message
            expected_error_message = 'Please provide all required arguments.'
            self.ctx.send.assert_called_once_with(expected_error_message)

            # Reset the mock for the next iteration
            self.ctx.send.reset_mock()

    async def test_place_bet_invalid_date_format(self, test_db):
        # Test case for an invalid date format
        await place_bet(self.ctx, "Test question", "invalid_date_format", AsyncMock(), AsyncMock(), "$100")
        self.ctx.send.assert_called_with('Error placing bet: Error binding parameter 2 - probably unsupported type.')


if __name__ == '__main__':
    unittest.main()
