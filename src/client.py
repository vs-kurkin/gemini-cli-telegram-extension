"""
Refactored client for interacting with the Telegram Bot API.

This version incorporates best practices for performance, readability,
error handling, and testability.
"""

import asyncio
import json
import os
import sys
from typing import Any, Awaitable, Callable, Coroutine, Dict, Optional

import telegram
from dotenv import load_dotenv
from telegram.error import TelegramError


class TelegramBotError(Exception):
    """Base exception for Telegram bot errors."""


class TelegramBotAuthError(TelegramBotError):
    """Raised when the bot token is invalid."""


class TelegramBotRequestError(TelegramBotError):
    """Raised when a request to the Telegram API fails."""


class TelegramBot:
    """A wrapper around the python-telegram-bot library."""

    def __init__(self, token: str):
        """
        Initializes the TelegramBot.

        Args:
            token: The Telegram bot token.
        """
        if not token:
            raise TelegramBotAuthError("Bot token not found.")
        self.bot = telegram.Bot(token=token)

    async def send_message(self, chat_id: str, text: str) -> Dict[str, Any]:
        """Sends a message to a Telegram chat."""
        if not chat_id or not text:
            raise TelegramBotRequestError("Missing required parameters 'chat_id' or 'text'.")
        try:
            message = await self.bot.send_message(chat_id=chat_id, text=text)
            return {"status": f"Message successfully sent to chat {chat_id}.", "message_id": message.message_id}
        except TelegramError as e:
            raise TelegramBotRequestError(f"Error sending message: {e}") from e

    async def read_messages(self, timeout: int, chat_id: Optional[str] = None, offset: int = 0) -> Dict[str, Any]:
        """Reads new messages from Telegram."""
        try:
            updates = await self.bot.get_updates(offset=offset, timeout=timeout)
            messages = []
            new_offset = offset
            if updates:
                for update in updates:
                    new_offset = update.update_id + 1
                    message = update.message or update.edited_message
                    if message and message.text and (chat_id is None or str(message.chat.id) == str(chat_id)):
                        messages.append(
                            {
                                "update_id": update.update_id,
                                "chat_id": message.chat.id,
                                "text": message.text,
                            }
                        )
            return {"messages": messages, "offset": new_offset}
        except TelegramError as e:
            raise TelegramBotRequestError(f"Error reading messages: {e}") from e

    async def get_me(self) -> Dict[str, Any]:
        """Gets information about the bot."""
        try:
            me = await self.bot.get_me()
            return me.to_dict()
        except TelegramError as e:
            raise TelegramBotRequestError(f"Error getting bot info: {e}") from e

    async def get_chat(self, chat_id: str) -> Dict[str, Any]:
        """Gets information about a chat."""
        if not chat_id:
            raise TelegramBotRequestError("Missing required parameter 'chat_id'.")
        try:
            chat = await self.bot.get_chat(chat_id=chat_id)
            return chat.to_dict()
        except TelegramError as e:
            raise TelegramBotRequestError(f"Error getting chat info: {e}") from e

    async def edit_message_text(self, chat_id: str, message_id: int, text: str) -> Dict[str, Any]:
        """Edits a text message."""
        if not chat_id or not message_id or not text:
            raise TelegramBotRequestError("Missing required parameters 'chat_id', 'message_id', or 'text'.")
        try:
            await self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)
            return {"status": "Message successfully edited."}
        except TelegramError as e:
            raise TelegramBotRequestError(f"Error editing message: {e}") from e

    async def delete_message(self, chat_id: str, message_id: int) -> Dict[str, Any]:
        """Deletes a message."""
        if not chat_id or not message_id:
            raise TelegramBotRequestError("Missing required parameters 'chat_id' or 'message_id'.")
        try:
            await self.bot.delete_message(chat_id=chat_id, message_id=message_id)
            return {"status": "Message successfully deleted."}
        except TelegramError as e:
            raise TelegramBotRequestError(f"Error deleting message: {e}") from e

    async def send_photo(self, chat_id: str, photo_path: str, caption: Optional[str] = None) -> Dict[str, Any]:
        """Sends a photo."""
        if not chat_id or not photo_path:
            raise TelegramBotRequestError("Missing required parameters 'chat_id' or 'photo_path'.")
        try:
            with open(photo_path, "rb") as photo:
                message = await self.bot.send_photo(chat_id=chat_id, photo=photo, caption=caption)
            return {"status": "Photo successfully sent.", "message_id": message.message_id}
        except FileNotFoundError:
            raise TelegramBotRequestError(f"File not found: {photo_path}")
        except TelegramError as e:
            raise TelegramBotRequestError(f"Error sending photo: {e}") from e

    async def send_document(self, chat_id: str, document_path: str, caption: Optional[str] = None) -> Dict[str, Any]:
        """Sends a document."""
        if not chat_id or not document_path:
            raise TelegramBotRequestError("Missing required parameters 'chat_id' or 'document_path'.")
        try:
            with open(document_path, "rb") as document:
                message = await self.bot.send_document(chat_id=chat_id, document=document, caption=caption)
            return {"status": "Document successfully sent.", "message_id": message.message_id}
        except FileNotFoundError:
            raise TelegramBotRequestError(f"File not found: {document_path}")
        except TelegramError as e:
            raise TelegramBotRequestError(f"Error sending document: {e}") from e

    async def get_chat_administrators(self, chat_id: str) -> Dict[str, Any]:
        """Gets a list of administrators in a chat."""
        if not chat_id:
            raise TelegramBotRequestError("Missing required parameter 'chat_id'.")
        try:
            admins = await self.bot.get_chat_administrators(chat_id=chat_id)
            return {"administrators": [admin.to_dict() for admin in admins]}
        except TelegramError as e:
            raise TelegramBotRequestError(f"Error getting chat administrators: {e}") from e

    async def answer_callback_query(self, callback_query_id: str, text: Optional[str] = None) -> Dict[str, Any]:
        """Answers a callback query."""
        if not callback_query_id:
            raise TelegramBotRequestError("Missing required parameter 'callback_query_id'.")
        try:
            await self.bot.answer_callback_query(callback_query_id=callback_query_id, text=text)
            return {"status": "Callback query answered successfully."}
        except TelegramError as e:
            raise TelegramBotRequestError(f"Error answering callback query: {e}") from e


class CommandDispatcher:
    """Dispatches commands to the appropriate handler."""

    def __init__(self, bot: TelegramBot):
        """
        Initializes the CommandDispatcher.

        Args:
            bot: An instance of the TelegramBot class.
        """
        self.bot = bot
        self.commands: Dict[str, Callable[..., Awaitable[Dict[str, Any]]]] = {
            "send_message": self.bot.send_message,
            "read": self.bot.read_messages,
            "get_me": self.bot.get_me,
            "get_chat": self.bot.get_chat,
            "edit_message_text": self.bot.edit_message_text,
            "delete_message": self.bot.delete_message,
            "send_photo": self.bot.send_photo,
            "send_document": self.bot.send_document,
            "get_chat_administrators": self.bot.get_chat_administrators,
            "answer_callback_query": self.bot.answer_callback_query,
        }

    async def dispatch(self, command_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dispatches a command to the appropriate handler.

        Args:
            command_name: The name of the command to dispatch.
            args: A dictionary of arguments for the command.

        Returns:
            The result of the command.
        """
        if command_name not in self.commands:
            raise TelegramBotRequestError(f"Unknown command: {command_name}")
        handler = self.commands[command_name]
        return await handler(**args)


def run_async_function(func: Coroutine[Any, Any, Any]) -> Any:
    """Runs an async function from a synchronous context."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(func)


def main():
    """Main function that processes command-line arguments."""
    load_dotenv()

    if len(sys.argv) < 2:
        print(json.dumps({"error": "Command not specified."}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    command_name = sys.argv[1]
    token = sys.argv[2] if len(sys.argv) > 2 else os.getenv("TELEGRAM_BOT_TOKEN")

    try:
        input_data: Dict[str, Any] = json.load(sys.stdin)
    except json.JSONDecodeError:
        input_data = {}

    try:
        bot = TelegramBot(token)
        dispatcher = CommandDispatcher(bot)
        result = run_async_function(dispatcher.dispatch(command_name, input_data))
        print(json.dumps(result, ensure_ascii=False))
    except TelegramBotError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
