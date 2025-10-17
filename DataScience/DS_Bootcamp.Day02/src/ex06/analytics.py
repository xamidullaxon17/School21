import logging
import config
import requests
import json
from random import randint

logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format=config.LOG_FORMAT,
    datefmt=config.LOG_DATEFMT
)

class Research:
    def __init__(self, file_path):
        self.file_path = file_path
        logging.info("Research initialized with file: %s", file_path)

    def file_reader(self):
        try:
            with open(self.file_path, "r") as file:
                data = [line.strip().split(",") for line in file.readlines()]
                header = data.pop(0)
                if len(header) != 2 or not all(item in {"0", "1"} for row in data for item in row):
                    raise ValueError("File format is incorrect")
                logging.info("File successfully read: %s", self.file_path)
                return [[int(x) for x in row] for row in data]
        except Exception as e:
            logging.error("Error reading file: %s", e)
            raise

    def send_telegram_message(self, message):
        payload = {
            "chat_id": config.TELEGRAM_CHAT_ID,
            "text": message
        }
        try:
            response = requests.post(config.TELEGRAM_WEBHOOK_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                logging.info("Telegram message sent successfully.")
            else:
                logging.error("Failed to send Telegram message: %s", response.text)
        except Exception as e:
            logging.error("Error while sending Telegram message: %s", e)

class Calculations:
    def __init__(self, data):
        self.data = data
        logging.info("Calculations initialized with data.")

    def counts(self):
        heads = sum(row[0] for row in self.data)
        tails = sum(row[1] for row in self.data)
        logging.info("Counts calculated: %d heads, %d tails", heads, tails)
        return [heads, tails]

    def fractions(self, counts):
        total = sum(counts)
        fractions = [(count / total) * 100 for count in counts]
        logging.info("Fractions calculated: %.2f%% heads, %.2f%% tails", fractions[0], fractions[1])
        return fractions

class Analytics(Calculations):
    def predict_random(self, num_predictions):
        predictions = [[randint(0, 1), randint(0, 1)] for _ in range(num_predictions)]
        logging.info("Random predictions generated: %s", predictions)
        return predictions

    def predict_last(self):
        last = self.data[-1]
        logging.info("Last prediction returned: %s", last)
        return last

    def save_file(self, data, filename, extension):
        full_path = f"{filename}.{extension}"
        try:
            with open(full_path, "w") as file:
                file.write(data)
            logging.info("File saved: %s", full_path)
        except Exception as e:
            logging.error("Error saving file: %s", e)
