import argparse
from modules.authentication import authenticate
from modules.upwork_calls import get_job_applications
from modules.proposal_generator import fetch_job_application_data, prepare_training_data, save_training_data_to_json

# Set up command-line argument parser
parser = argparse.ArgumentParser(description="Upwork API scraper and proposal generator")
parser.add_argument("--scrape", action="store_true", help="Scrape Upwork jobs data")
parser.add_argument("--generate-training", action="store_true", help="Generate training data from scraped job data")

args = parser.parse_args()

if __name__ == "__main__":
    client = authenticate()

    if args.scrape:
        get_job_applications(client)

    if args.generate_training:
        records = fetch_job_application_data()
        training_data = prepare_training_data(records)
        save_training_data_to_json(training_data, "training_data.json")