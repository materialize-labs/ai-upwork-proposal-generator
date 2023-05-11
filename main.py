import argparse
import re
from rich.console import Console
from modules.authentication import authenticate
from modules.database import create_tables, get_last_fine_tuned_model
from modules.upwork_calls import get_job_applications, get_job_details
from modules.proposal_generator import (fetch_job_application_data,
                                        prepare_training_data,
                                        save_training_data_to_jsonl,
                                        upload_training_data,
                                        create_fine_tuned_model,
                                        list_fine_tuned_models,
                                        delete_fine_tuned_model,
                                        generate_completions)

console = Console()
create_tables()

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

    # Command to scrape previously written applications and the assocaited job details and insert them into the DB
    if args.scrape:
        get_job_applications(client)

    # Command to generate the training data based on the application and job details in the DB
    if args.generate_training:
        records = fetch_job_application_data()
        training_data = prepare_training_data(records)
        save_training_data_to_jsonl(training_data, "training_data.jsonl")

    # Fine tune a new model
    if args.fine_tune:
        file_id = upload_training_data("training_data.jsonl")
        fine_tune_result = create_fine_tuned_model(file_id)
        print(fine_tune_result)

    # List all of your fine tuned models
    if args.list_fine_tunes:
        fine_tunes = list_fine_tuned_models()
        print(fine_tunes)

    # Delete a fine tuned model
    if args.delete_model:
        delete_result = delete_fine_tuned_model(args.delete_model)
        print(delete_result)

    # Command to generate a proposal in resopnse to a provided job post
    if args.generate_single_job_proposal:
        job_url = input("Enter the Upwork job post URL: ").strip()
        model_id = input("Enter the fine-tuned model name (press Enter to use the last created model): ").strip()

        # Extract the job ID from the URL using a regular expression
        match = re.search(r'~[0-9a-zA-Z]{18}', job_url)
        if match:
            job_id = match.group()
        else:
            console.print("[red]Invalid Upwork job URL[/red]")
            exit()

        if not model_id:
            model_id = get_last_fine_tuned_model()
        if not model_id:
            console.print("[red]No model found in the database.[/red]")
            exit()

        job = get_job_details(client, job_id)

        input_text = f"Job Category Level One: {job['profile']['job_category_level_one']}\n"
        input_text += f"Job Category Level Two: {job['profile']['job_category_level_two']}\n"
        input_text += f"Description: {job['profile']['op_description']}\n"
        input_text += f"Engagement: {job['profile']['op_engagement']}\n\n###\n\n"

        completions = generate_completions(model_id, input_text, 1024, " END", 1, 0.8)

        print("\nGenerated Proposal:\n")
        print(completions)