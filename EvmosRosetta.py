import argparse
import logging
import threading
import time
import openai
import praw
import requests
import telebot
import numpy as np
import re
import string
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

logging.basicConfig(level=logging.INFO, filename="logfile.txt", filemode="a", format="%(asctime)s - %(levelname)s - %(message)s")

reddit_client_id = config.get("credentials", "reddit_client_id")
reddit_client_secret = config.get("credentials", "reddit_client_secret")
reddit_user_agent = config.get("credentials", "reddit_user_agent")
telegram_bot_token = config.get("credentials", "telegram_bot_token")
deepl_api_key = config.get("credentials", "deepl_api_key")
openai_api_key = config.get("credentials", "openai_api_key")

# Function to load prompts from file
def load_translation_methods(filename):
    translation_methods = {}
    telegram_chat_ids = {}
    with open(filename, "r") as f:
        for line in f:
            lang, method, translation_prompt, refinement_prompt, chat_id = line.strip().split(":", 4)
            translation_methods[lang] = {
                "method": method,
                "translation": translation_prompt,
                "refinement": refinement_prompt
            }
            telegram_chat_ids[lang] = chat_id
    return translation_methods, telegram_chat_ids

# Load prompts and Telegram Channel ID from the file when the script starts
filename = "translation_methods.txt"
translation_methods, telegram_chat_ids = load_translation_methods(filename)

reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent=reddit_user_agent
)

bot = telebot.TeleBot(telegram_bot_token)
openai.api_key = openai_api_key

def get_pinned_posts(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    pinned_posts = [post for post in subreddit.hot(limit=10) if post.stickied]
    return pinned_posts

def send_telegram_message(lang, message_text):
    try:
        chat_id = telegram_chat_ids[lang]
        message_parts = [message_text[i:i + 4090] for i in range(0, len(message_text), 4090)]

        for message_part in message_parts:
            bot.send_message(chat_id, message_part)
            time.sleep(1)
    except Exception as e:
        logging.error(f"Error sending Telegram message: {e}")

def count_tokens(text):
    tokenized_text = tokenizer.tokenize(text)
    return len(tokenized_text)

def estimate_tokens(text):
    words = text.split()
    tokens = 0
    for word in words:
        tokens += 1 + sum(c in string.punctuation for c in word)
    return tokens

def refine_translation(text, target_language):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a highly skilled language expert and a helpful assistant."},
                {"role": "user", "content": f"Improve the grammar and fluency of the following {target_language} text while maintaining its original meaning and formatting: {text}"}
            ],
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        refined_text = response.choices[0].text.strip()
        return refined_text
    except Exception as e:
        logging.error(f"Error refining translation: {e}")
        return text

def truncate_text_to_tokens(text, max_tokens):
    non_space_regex = re.compile(r'[^\s]+')
    tokens = list(non_space_regex.finditer(text))
    truncated_text = ""

    for i, token_match in enumerate(tokens):
        if i >= max_tokens:
            break
        token_value = token_match.group()
        truncated_text += token_value
        if i + 1 < len(tokens):
            token_end, next_token_start = token_match.end(), tokens[i + 1].start()
            truncated_text += text[token_end:next_token_start]

    return truncated_text

def translate_text(text, target_language="en"):
    print("Translating text...")
    translation_method = translation_methods[target_language]["method"]
    print(f"Translation method: {translation_method}")
    translation_prompt = translation_methods[target_language]["translation"].format(text=text)

    try:
        if translation_method == "gpt":
            # GPT-3 translation
            prompt_tokens = estimate_tokens(translation_prompt)

            max_tokens = 4096 - prompt_tokens - 100 - 1024

            text = truncate_text_to_tokens(text, max_tokens)

            # Use the text-davinci-003 model to compute logprobs
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=translation_prompt,
                max_tokens=1024,
                n=3,
                temperature=0.5,
                logprobs=10
            )

            log_probabilities = [sum(choice['logprobs']['top_logprobs'][0].values()) for choice in response.choices]
            best_translation_index = np.argmax(log_probabilities)

            translated_text = response.choices[best_translation_index].text.strip()

        elif translation_method == "deepl" or translation_method == "deepl_gpt":
            # DeepL translation
            if target_language == "zh-CN":
                deepL_language_code = "ZH"
            else:
                deepL_language_code = target_language

            url = f"https://api-free.deepl.com/v2/translate"
            payload = {
                "auth_key": deepl_api_key,
                "text": text,
                "target_lang": deepL_language_code
            }
            response = requests.post(url, data=payload)
            translated_text = response.json()["translations"][0]["text"]

            if translation_method == "deepl_gpt":
                # GPT-3 refinement
                refinement_prompt = translation_methods[target_language]["refinement"].format(text=translated_text)
                prompt_tokens = estimate_tokens(refinement_prompt)

                max_tokens = 4096 - prompt_tokens - 100 - 1024

                text = truncate_text_to_tokens(translated_text, max_tokens)

                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=refinement_prompt,
                    max_tokens=1024,
                    n=3,
                    temperature=0.5,
                    logprobs=10
                )

                log_probabilities = [sum(choice['logprobs']['top_logprobs'][0].values()) for choice in response.choices]
                best_refinement_index = np.argmax(log_probabilities)

                refined_text = response.choices[best_refinement_index].text.strip()
                translated_text = refined_text

        else:
            raise ValueError(f"Invalid translation method: {translation_method}")

        print("Translation completed.")
        return translated_text

    except Exception as e:
        logging.error(f"Error translating text: {e}")
        return text

@bot.message_handler(commands=["start"])
def handle_start(message):
    chat_id = message.chat.id
    logging.info(f"Your chat ID is: {chat_id}")

def main(subreddit_name, languages):
    sent_post_ids = set()

    while True:
        try:
            logging.info("Checking for new pinned posts...")
            pinned_posts = get_pinned_posts(subreddit_name)
            logging.info(f"Found {len(pinned_posts)} pinned posts")

            for post in pinned_posts:
                if post.id not in sent_post_ids:
                    for lang in languages:
                        try:
                            logging.info(f"Processing post {post.id} in {lang}")
                            translated_title = translate_text(post.title, target_language=lang)
                            translated_selftext = translate_text(post.selftext, target_language=lang)
                            message = f"Title: {translated_title}\n\nURL: {post.url}\n\n{translated_selftext}"
                                    
                            if lang == "zh-CN":
                                lang = "ZH"
                                    
                            send_telegram_message(lang, message)
                            logging.info(f"Sent post {post.id} in {lang}")
                            time.sleep(1)

                        except Exception as e:
                            logging.error(f"An error occurred processing post {post.id} in {lang}: {e}")

                    sent_post_ids.add(post.id)

            time.sleep(300)

        except praw.exceptions.PRAWException as e:
            logging.error(f"An error occurred with the Reddit API: {e}")
            time.sleep(60)  # Wait for 1 minute before retrying

        except telebot.apihelper.ApiException as e:
            logging.error(f"An error occurred with the Telegram API: {e}")
            time.sleep(60)  # Wait for 1 minute before retrying

        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred with the DeepL API: {e}")
            time.sleep(60)  # Wait for 1 minute before retrying

        except openai.Error as e:
            logging.error(f"An error occurred with the OpenAI API: {e}")
            time.sleep(60)  # Wait for 1 minute before retrying

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            time.sleep(60)  # Wait for 1 minute before retrying

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Telegram bot for monitoring and translating pinned Reddit posts.")
    parser.add_argument("--subreddit", default="evmos", help="Subreddit name to monitor for pinned posts")
    args = parser.parse_args()

    # Get the list of languages from the translation_methods dictionary
    languages = list(translation_methods.keys())

    main_thread = threading.Thread(target=main, args=(args.subreddit, languages))
    main_thread.start()
    bot.polling()  # Start listening for incoming messages