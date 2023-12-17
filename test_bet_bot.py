import tracemalloc
tracemalloc.start()

import unittest
from unittest.mock import AsyncMock

from bet_bot import place_bet


class TestPlaceBetCommand(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Mock the necessary objects
        self.ctx = AsyncMock()
        self.ctx.send = AsyncMock()

    async def test_place_bet_success(self):
        # Prepare test data
        question = "Test question"
        expiration_date = "2023-12-31 12:00:00"
        yes_user = "user1"
        no_user = "user2"
        value = 100

        # Call the function with the test data
        await place_bet(self.ctx, question, expiration_date, yes_user, no_user, value)

        # Assert that the send method was called with the correct message
        self.ctx.send.assert_called_once_with('Bet placed successfully!')

    async def test_place_bet_missing_arguments(self):
        # Call the function without providing all required arguments
        await place_bet(self.ctx, "", "", "", "", "")

        # Assert that the send method was called with the correct error message
        self.ctx.send.assert_called_once_with('Please provide all required arguments.')


if __name__ == '__main__':
    unittest.main()

