# EvmosRosetta
Translate Reddit posts and re-post on Telegram

This repository contains a Python script for a Telegram bot that monitors a specified subreddit for pinned posts, translates them into multiple languages using OpenAI's GPT-3 and DeepL API, and sends the translated content to corresponding Telegram channels.

## Features
- Monitors a specified subreddit for new pinned posts
- Translates pinned posts into multiple languages using GPT-3 or DeepL API, depending on the specified translation method for each language
- Refines translations using GPT-3, if desired
- Sends translated posts to Telegram channels in different languages
- Supports error handling and logging

## Libraries and API Integrations
- **PRAW** (Python Reddit API Wrapper): 
  Allows the bot to access and extract information from the specified subreddit. For more information on usage, please visit [PRAW Documentation](https://praw.readthedocs.io/).

- **Telebot** (pyTelegramBotAPI): 
  Facilitates interactions with the Telegram Bot API for sending messages and handling bot commands. For more information, please visit the [pyTelegramBotAPI GitHub repository](https://github.com/eternnoir/pyTelegramBotAPI).

- **OpenAI** for interacting with GPT-3 models: 
  This project uses the OpenAI API for GPT-3 translations, refining translations, and language-specific prompts. For more information on usage and terms of service, please visit [OpenAI API Documentation](https://beta.openai.com/docs/).

- **Requests** for interacting with the DeepL API: 
  This library enables sending HTTP requests to the DeepL API for obtaining translations. For more information on usage, please visit [Requests Documentation](https://docs.python-requests.org/) and the [DeepL API Documentation](https://www.deepl.com/en/docs-api/).


## Setup
**1.** Install the required Python libraries using the following command:
    ```bash
    pip install praw openai pytelegrambotapi requests numpy configparser
    ```
**2.** Create a `config.ini` file with the required API credentials for Reddit, Telegram, OpenAI, and DeepL. Use the provided `config.ini.example` as a template.
**3.** Update the `translation_methods.txt` file with the desired language codes, translation methods, translation/refinement prompts, and Telegram chat IDs for each language.

The main function of the script runs in a loop, checking for new pinned posts every 5 minutes (configurable) and translating them if not already processed. The script also starts a Telebot instance for polling and responding to Telegram bot commands, like `/start` for retrieving the chat ID.

## Usage

**1.** To start the bot, run the following command:
```bash
python EvmosRosetta.py --subreddit <subreddit_name>
```

Replace `<subreddit_name>` with the name of the subreddit you want to monitor for pinned posts.

**2.** Alternatively, you can use the provided `start_bot.sh` (for Linux) or `start_bot.bat` (for Windows) file to start the bot. Update the `<subreddit_name>` in the `start_bot.sh` or `start_bot.bat` file with the desired subreddit name.

### For Linux:

Give the `start_bot.sh` file executable permissions by running:
```bash
chmod +x start_bot.sh
```
Then start the bot by running:
```bash
./start_bot.sh
```
### For Windows:

Double-click the start_bot.bat file, or open a Command Prompt window, navigate to the directory containing the start_bot.bat file, and run:
```bash
start_bot.bat
```
## Contributing
We invite users to contribute and enhance the project. Here are some suggestions to improve and extend the functionality of EvmosRosetta:

- **Support more translation services:** Currently, the script supports GPT-3 and DeepL API for translation. You can add support for other translation services like Google Translate, Microsoft Translator, or Amazon Translate.

- **Configurable polling interval:** Allow users to configure the polling interval for checking new pinned posts in the subreddit through command-line arguments or a configuration file.

- **Add more bot commands:** Implement additional commands for the Telegram bot, such as `/set_language` for users to select their preferred language, or `/set_subreddit` to change the monitored subreddit.

- **Refactor code for better modularity:** Break down the main function into smaller functions to improve readability and maintainability. For example, create separate functions for handling each API integration, error handling, or translation steps.
  - **Modularize social channel support:** Refactor the code to abstract the social channel interactions into separate classes or modules. This will make it easier to add or modify support for different social channels in the future.

- **Twitter integration using Tweepy library:** Use the Tweepy library to interact with the Twitter API. You can create functions to post translated content as tweets or threads on a Twitter account. For example, you could use `tweepy.API.update_status()` for posting tweets and `tweepy.API.update_status()` with the `in_reply_to_status_id parameter` for creating threads. 

- **Discord integration using Discord.py library:** Use the `Discord.py` library to interact with the Discord API. You can create a Discord bot that posts translated content to specific channels in a Discord server. For example, you could use `discord.TextChannel.send()` for posting messages.

- **Configuration for social channels:** Update the configuration file and command-line arguments to allow users to specify which social channels to pull from and post to. You can use the configparser library to manage the configuration for each social channel.

- **Support for cross-posting:** Implement cross-posting functionality, allowing the bot to pull content from one social channel and post it to another. For example, you can pull content from Reddit and post it to both Telegram and Twitter.

- **Implement a database for tracking sent posts:** Use a database (e.g., SQLite) to store the processed post IDs instead of a set in memory. This will help maintain a persistent record of sent posts across multiple runs of the script.

- **Support for Markdown and rich text formatting:** Enhance the translation process to handle and preserve Markdown or rich text formatting in the original Reddit post.

- **Automatic language detection:** Implement automatic language detection for the original posts using GPT-3 or external libraries like `langdetect`, so the script can better handle subreddits with posts in multiple languages.

- **Error handling and logging:** Add error handling and logging for each social channel integration to ensure the bot runs smoothly and provides useful information in case of issues.

- **Unit tests:** Add unit tests for each social channel integration to verify that the bot functions correctly and can handle various situations and edge cases.

- **Rate limiting and API usage optimization:** Different social channels have different rate limits and usage restrictions. Ensure that the bot respects these limits by implementing rate limiting and optimizing API calls.

By implementing these features, EvmosRosetta will become more versatile and useful for a broader audience, catering to their specific preferences and needs for content consumption and sharing on different platforms.

Fork the repository, make improvements, and submit pull requests. Your contributions will help make this tool more useful and powerful for the community!

## License
This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
