# EvmosRosetta
Translate Reddit posts and re-post on Telegram

This repository contains a Python script for a Telegram bot that monitors a specified subreddit for pinned posts, translates them into multiple languages using OpenAI's GPT-3 and DeepL API, and sends the translated content to corresponding Telegram channels.

## Features
- Monitors a specified subreddit for new pinned posts
- Translates pinned posts into multiple languages using GPT-3 or DeepL API, depending on the specified translation method for each language
- Refines translations using GPT-3, if needed
- Sends translated posts to Telegram channels in different languages
- Supports error handling and logging

## Libraries and API Integrations
- PRAW (Python Reddit API Wrapper) for interacting with the Reddit API
- Telebot (pyTelegramBotAPI) for interacting with the Telegram Bot API
- OpenAI for interacting with GPT-3 models
- Requests for interacting with the DeepL API

## Setup
1. Install the required Python libraries using the following command:
    ```bash
    pip install praw openai pytelegrambotapi requests numpy configparser
    ```
2. Create a `config.ini` file with the required API credentials for Reddit, Telegram, OpenAI, and DeepL. Use the provided `config.ini.example` as a template.
3. Update the `translation_methods.txt` file with the desired language codes, translation methods, translation/refinement prompts, and Telegram chat IDs for each language.

The main function of the script runs in a loop, checking for new pinned posts every 5 minutes (configurable) and translating them if not already processed. The script also starts a Telebot instance for polling and responding to Telegram bot commands, like `/start` for retrieving the chat ID.

## Contributing
We invite users to contribute and enhance the project. Here are some suggestions to improve or modify the script:

- Support more translation services
- Configurable polling interval
- Add more bot commands
- Refactor code for better modularity
- Implement a database for tracking sent posts
- Support for Markdown and rich text formatting
- Automatic language detection
- Unit tests and error handling

Fork the repository, make improvements, and submit pull requests. Your contributions will help make this tool more useful and powerful for the community!

## Extending Functionality
### Support for Other Social Channels
Adding support for other social channels like Twitter and Discord is an excellent idea to extend the functionality of the bot. Below are some suggestions on how to implement this feature:

- Twitter integration using Tweepy library
- Discord integration using Discord.py library
- Modularize social channel support
- Configuration for social channels
- Support for cross-posting
- Rate limiting and API usage optimization
- Error handling and logging
- Unit tests

By implementing these features, you can make the bot more versatile and useful for a broader audience, catering to their specific preferences and needs for content consumption and sharing on different platforms.

## License
This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
