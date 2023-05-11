import argparse
from modules.authentication import authenticate
from modules.upwork_calls import get_job_applications, get_job_details
from modules.proposal_generator import (fetch_job_application_data,
                                        prepare_training_data,
                                        save_training_data_to_jsonl,
                                        upload_training_data,
                                        create_fine_tuned_model,
                                        list_fine_tuned_models,
                                        delete_fine_tuned_model,
                                        generate_completions)

parser = argparse.ArgumentParser(description="Upwork API scraper and proposal generator")
parser.add_argument("--scrape", action="store_true", help="Scrape Upwork jobs data")
parser.add_argument("--generate-training", action="store_true", help="Generate training data from scraped job data")
parser.add_argument("--fine-tune", action="store_true", help="Create a fine-tuned model")
parser.add_argument("--list-fine-tunes", action="store_true", help="List all fine-tuned models")
parser.add_argument("--delete-model", metavar="MODEL_ID", help="Delete a fine-tuned model")
parser.add_argument("--generate-single-job-proposal", action="store_true", help="Generate proposal for a single Upwork job using a fine-tuned model")

args = parser.parse_args()

if __name__ == "__main__":
    client = authenticate()

    if args.scrape:
        get_job_applications(client)

    if args.generate_training:
        records = fetch_job_application_data()
        training_data = prepare_training_data(records)
        save_training_data_to_jsonl(training_data, "training_data.jsonl")

    if args.fine_tune:
        file_id = upload_training_data("training_data.jsonl")
        fine_tune_result = create_fine_tuned_model(file_id)
        print(fine_tune_result)

    if args.list_fine_tunes:
        fine_tunes = list_fine_tuned_models()
        print(fine_tunes)

    if args.delete_model:
        delete_result = delete_fine_tuned_model(args.delete_model)
        print(delete_result)

    if args.generate_single_job_proposal:
        job_id = input("Enter an Upwork job ID: ").strip()
        model_id = input("Enter the fine-tuned model ID: ").strip()
        
        job = get_job_details(client, job_id)
        
        input_text = f"{job['profile']['job_category_level_one']}\n{job['profile']['job_category_level_two']}\n{job['profile']['job_type']}\n{job['profile']['op_description']}\n{job['profile']['op_pref_location']}\n{job['profile']['op_pref_hourly_rate_min']}-{job['profile']['op_pref_hourly_rate_max']}\n{job['profile']['op_engagement']}\n\n###\n\n"
        completions = generate_completions(model_id, input_text)
        
        print("\nGenerated Proposal:\n")
        print(completions)