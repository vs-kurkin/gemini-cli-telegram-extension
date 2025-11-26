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
/extension install https://github.com/VSKurkin/gemini-cli-telegram-extension.git
```

**Note:** Your Gemini CLI must be configured to allow installing third-party extensions.

## Configuration

This extension requires a Telegram Bot API token. You can provide it in one of two ways:

1.  **Environment Variable (Recommended):**
    Set the `TELEGRAM_BOT_TOKEN` environment variable in your system. This is the most secure and flexible method.

    -   **Linux/macOS:**
        ```bash
        export TELEGRAM_BOT_TOKEN="your-bot-token"
        ```
    -   **Windows:**
        ```powershell
        $env:TELEGRAM_BOT_TOKEN="your-bot-token"
        ```

2.  **`.env` File:**
    Create a file named `.env` in the directory where you run the `gemini` command. Add the following line to it:
    ```
    TELEGRAM_BOT_TOKEN="your-bot-token"
    ```

## Usage

To use the tools provided by this extension, you need to make a tool call in your prompt. The Gemini CLI will execute the tool call and return the result.

**Example 1: Send a message**

To send a message, make a tool call to `telegram:send_message` with the `chat_id` and `text` parameters.

> telegram:send_message(chat_id="your-chat-id", text="Hello from Gemini!")

**Example 2: Read new messages**

To read new messages, make a tool call to `telegram:read`.

> telegram:read()

**Example 3: Send a photo**

To send a photo, make a tool call to `telegram:send_photo`.

> telegram:send_photo(chat_id="your-chat-id", photo_path="/path/to/your/photo.jpg")

## Available Tools

This section provides a detailed description of each tool and its parameters.

### `telegram:send_message`

Sends a text message.

| Parameter | Type   | Description            |
| :-------- | :----- | :--------------------- |
| `chat_id` | string | Chat ID.               |
| `text`    | string | The text of the message. |

### `telegram:read`

Reads new messages.

| Parameter | Type    | Description                       |
| :-------- | :------ | :-------------------------------- |
| `timeout` | integer | Timeout for waiting for updates.  |
| `chat_id` | string  | Chat ID to filter messages from.  |
| `offset`  | integer | Offset for get_updates.           |

### `telegram:get_me`

Gets information about the bot. (No parameters)

### `telegram:get_chat`

Gets information about a chat.

| Parameter | Type   | Description |
| :-------- | :----- | :---------- |
| `chat_id` | string | Chat ID.    |

### `telegram:edit_message_text`

Edits a text message.

| Parameter    | Type    | Description                   |
| :----------- | :------ | :---------------------------- |
| `chat_id`    | string  | Chat ID.                      |
| `message_id` | integer | Message ID.                   |
| `text`       | string  | The new text of the message. |

### `telegram:delete_message`

Deletes a message.

| Parameter    | Type    | Description |
| :----------- | :------ | :---------- |
| `chat_id`    | string  | Chat ID.    |
| `message_id` | integer | Message ID. |

### `telegram:send_photo`

Sends a photo.

| Parameter    | Type   | Description              |
| :----------- | :----- | :----------------------- |
| `chat_id`    | string | Chat ID.                 |
| `photo_path` | string | Path to the photo file.  |
| `caption`    | string | Caption for the photo.   |

### `telegram:send_document`

Sends a document.

| Parameter       | Type   | Description                |
| :-------------- | :----- | :------------------------- |
| `chat_id`       | string | Chat ID.                   |
| `document_path` | string | Path to the document file. |
| `caption`       | string | Caption for the document.  |

### `telegram:get_chat_administrators`

Gets a list of chat administrators.

| Parameter | Type   | Description |
| :-------- | :----- | :---------- |
| `chat_id` | string | Chat ID.    |

### `telegram:answer_callback_query`

Answers a callback query.

| Parameter           | Type   | Description              |
| :------------------ | :----- | :----------------------- |
| `callback_query_id` | string | Callback query ID.       |
| `text`              | string | Text of the notification.|

## Development

To set up the development environment, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/VSKurkin/gemini-cli-telegram-extension.git
    cd gemini-cli-telegram-extension
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    pip install ruff # Or add it to a requirements-dev.txt
    ```

### Running Tests

To run the tests, execute the following command from the root of the repository:

```bash
python -m unittest discover tests
```

### Linting

To lint the code, use `ruff`:

```bash
ruff check .
```

To format the code, use `ruff`:

```bash
ruff format .
```