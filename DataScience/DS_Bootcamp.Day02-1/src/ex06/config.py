import os

LOG_FILE = "analytics.log"
LOG_FORMAT = "%(asctime)s %(message)s"
LOG_DATEFMT = "%Y-%m-%d %H:%M:%S"

TELEGRAM_WEBHOOK_URL = "https://api.telegram.org/bot7645697946:AAFAdQPyhVe4IE1pI8hKR0sZ969oBjabtzA/sendMessage"
TELEGRAM_CHAT_ID = "359310632"

num_of_steps = 3
REPORT_TEMPLATE = """\
Report

We have made {} observations from tossing a coin: {} of them were tails and {} of them were heads.
The probabilities are {:.2f}% and {:.2f}%, respectively.
Our forecast is that in the next {} observations we will have: {} tails and {} heads.
"""
