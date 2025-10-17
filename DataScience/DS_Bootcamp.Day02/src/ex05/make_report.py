from analytics import Analytics
import config

def main():
    filepath = "data.csv"

    analytics = Analytics(filepath)

    counts = analytics.counts()
    fractions = analytics.fractions(counts)
    predictions = analytics.predict_random(config.num_of_steps)
    last_prediction = analytics.predict_last()

    report = config.report_template.format(
        total_observations=len(analytics.data),
        tails=counts[1],
        heads=counts[0],
        tails_percentage=fractions[1],
        heads_percentage=fractions[0],
        num_steps=config.num_of_steps,
        predicted_tails=sum(pred[1] for pred in predictions),
        predicted_heads=sum(pred[0] for pred in predictions)
    )

    analytics.save_file(report, "report", "txt")

    print(report)

if __name__ == "__main__":
    main()
