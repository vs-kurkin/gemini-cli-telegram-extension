# Gemini Telegram Extension

This extension provides a set of tools to interact with the Telegram Bot API directly from the Gemini CLI.

## Features

- Send messages
- Read messages
- Get bot information
- Get chat information
- Edit messages
- Delete messages
- Send photos
- Send documents
- Get chat administrators
- Answer callback queries

## Installation

To install the extension, run the following command in your Gemini CLI:

```bash
/extension install https://github.com/vs-kurkin/gemini-cli-telegram-extension.git
```

## Configuration

1.  **Set your Telegram Bot Token:**
    - Create a file named `.env` in the root of the project.
    - Add the following line to the `.env` file:
      ```
      TELEGRAM_BOT_TOKEN="your-bot-token"
      ```

## Usage

You can use the provided tools in your Gemini CLI prompts. For example, to send a message, you can use the `telegram:send_message` tool:

```
/prompt telegram:send_message chat_id="your-chat-id" text="Hello from Gemini!"
```

## Available Tools

This section provides a detailed description of each tool and its parameters.

### `telegram:send_message`

Sends a text message to a specified chat.

**Parameters:**

| Name      | Type     | Description                  |
| :-------- | :------- | :--------------------------- |
| `chat_id` | `string` | The ID of the chat to send the message to. |
| `text`    | `string` | The text of the message to send.    |

### `telegram:read`

Reads new messages from your bot's updates.

**Parameters:**

| Name      | Type      | Description                               |
| :-------- | :-------- | :---------------------------------------- |
| `timeout` | `integer` | The timeout in seconds for long polling.  |
| `chat_id` | `string`  | The ID of the chat to filter messages from. |
| `offset`  | `integer` | The offset for getting updates.            |

### `telegram:get_me`

Gets information about the bot.

**Parameters:**

*This tool does not take any parameters.*

## Development

To develop and test the extension, you can use the following commands:

- **Run tests:**
  ```bash
  python extensions/telegram/tests/test_client.py
  ```

- **Run the linter:**
  ```bash
  pnpm lint
  ```
