"""
Unit tests for the refactored Telegram bot client.
"""

import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from src.client import (
    CommandDispatcher,
    TelegramBot,
    TelegramBotAuthError,
    TelegramBotRequestError,
)


class TestTelegramBot(unittest.TestCase):
    """Tests for the TelegramBot class."""

    def test_init_with_no_token_raises_auth_error(self):
        """Tests that an auth error is raised when no token is provided."""
        with self.assertRaises(TelegramBotAuthError):
            TelegramBot(token="")

    @patch("telegram.Bot")
    def test_send_message_with_no_chat_id_raises_request_error(self, mock_bot):
        """Tests that a request error is raised when no chat_id is provided."""
        bot = TelegramBot(token="test_token")
        with self.assertRaises(TelegramBotRequestError):
            asyncio.run(bot.send_message(chat_id="", text="test_text"))

    @patch("telegram.Bot")
    def test_send_message_with_no_text_raises_request_error(self, mock_bot):
        """Tests that a request error is raised when no text is provided."""
        bot = TelegramBot(token="test_token")
        with self.assertRaises(TelegramBotRequestError):
            asyncio.run(bot.send_message(chat_id="test_chat_id", text=""))

    @patch("telegram.Bot")
    def test_send_message_successful(self, mock_bot):
        """Tests that a message is sent successfully."""
        mock_bot.return_value.send_message = AsyncMock(return_value=MagicMock(message_id=123))
        bot = TelegramBot(token="test_token")
        result = asyncio.run(bot.send_message(chat_id="test_chat_id", text="test_text"))
        self.assertEqual(result["message_id"], 123)

    @patch("telegram.Bot")
    def test_get_chat_successful(self, mock_bot):
        """Tests that chat info is retrieved successfully."""
        mock_bot.return_value.get_chat = AsyncMock(return_value=MagicMock(to_dict=lambda: {"id": "123"}))
        bot = TelegramBot(token="test_token")
        result = asyncio.run(bot.get_chat(chat_id="123"))
        self.assertEqual(result["id"], "123")

    @patch("telegram.Bot")
    def test_edit_message_text_successful(self, mock_bot):
        """Tests that a message is edited successfully."""
        mock_bot.return_value.edit_message_text = AsyncMock()
        bot = TelegramBot(token="test_token")
        result = asyncio.run(bot.edit_message_text(chat_id="123", message_id=456, text="new text"))
        self.assertEqual(result["status"], "Message successfully edited.")

    @patch("telegram.Bot")
    def test_delete_message_successful(self, mock_bot):
        """Tests that a message is deleted successfully."""
        mock_bot.return_value.delete_message = AsyncMock()
        bot = TelegramBot(token="test_token")
        result = asyncio.run(bot.delete_message(chat_id="123", message_id=456))
        self.assertEqual(result["status"], "Message successfully deleted.")

    @patch("src.client.open", new_callable=unittest.mock.mock_open, read_data=b"photodata")
    @patch("telegram.Bot")
    def test_send_photo_successful(self, mock_bot, mock_open):
        """Tests that a photo is sent successfully."""
        mock_bot.return_value.send_photo = AsyncMock(return_value=MagicMock(message_id=123))
        bot = TelegramBot(token="test_token")
        result = asyncio.run(bot.send_photo(chat_id="123", photo_path="photo.jpg"))
        self.assertEqual(result["message_id"], 123)

    @patch("src.client.open", new_callable=unittest.mock.mock_open, read_data=b"docdata")
    @patch("telegram.Bot")
    def test_send_document_successful(self, mock_bot, mock_open):
        """Tests that a document is sent successfully."""
        mock_bot.return_value.send_document = AsyncMock(return_value=MagicMock(message_id=123))
        bot = TelegramBot(token="test_token")
        result = asyncio.run(bot.send_document(chat_id="123", document_path="doc.txt"))
        self.assertEqual(result["message_id"], 123)


class TestCommandDispatcher(unittest.TestCase):
    """Tests for the CommandDispatcher class."""

    def setUp(self):
        self.bot_mock = MagicMock(spec=TelegramBot)
        # Since methods are async, the spec will create AsyncMocks for them
        self.dispatcher = CommandDispatcher(self.bot_mock)

    def test_dispatch_unknown_command_raises_request_error(self):
        """Tests that a request error is raised for an unknown command."""
        with self.assertRaises(TelegramBotRequestError):
            asyncio.run(self.dispatcher.dispatch("unknown_command", {}))

    def test_dispatch_send_message_successful(self):
        """Tests that the send_message command is dispatched successfully."""
        self.bot_mock.send_message.return_value = {"status": "success"}
        result = asyncio.run(
            self.dispatcher.dispatch("send_message", {"chat_id": "test_chat_id", "text": "test_text"})
        )
        self.bot_mock.send_message.assert_called_once_with(chat_id="test_chat_id", text="test_text")
        self.assertEqual(result["status"], "success")

    def test_dispatch_get_me_successful(self):
        """Tests that the get_me command is dispatched successfully."""
        self.bot_mock.get_me.return_value = {"id": 123, "is_bot": True}
        result = asyncio.run(self.dispatcher.dispatch("get_me", {}))
        self.bot_mock.get_me.assert_called_once()
        self.assertEqual(result["id"], 123)

    def test_dispatch_edit_message_text_successful(self):
        """Tests that the edit_message_text command is dispatched successfully."""
        self.bot_mock.edit_message_text.return_value = {"status": "success"}
        args = {"chat_id": "123", "message_id": 456, "text": "new"}
        result = asyncio.run(self.dispatcher.dispatch("edit_message_text", args))
        self.bot_mock.edit_message_text.assert_called_once_with(**args)
        self.assertEqual(result["status"], "success")


if __name__ == "__main__":
    unittest.main()
