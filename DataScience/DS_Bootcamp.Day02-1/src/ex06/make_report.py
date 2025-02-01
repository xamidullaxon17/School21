import config
from analytics import Research, Analytics

def main():
    try:
        research = Research("data.csv")
        data = research.file_reader()

        analytics = Analytics(data)
        counts = analytics.counts()
        fractions = analytics.fractions(counts)
        predictions = analytics.predict_random(config.num_of_steps)
        last_prediction = analytics.predict_last()

        report = config.REPORT_TEMPLATE.format(
            len(data), counts[1], counts[0],
            fractions[1], fractions[0],
            3, predictions.count([0, 1]), predictions.count([1, 0])
        )

        analytics.save_file(report, "report", "txt")
        research.send_telegram_message("The report has been successfully created.")

    except Exception as e:
        research.send_telegram_message("The report hasn't been created due to an error.")
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
