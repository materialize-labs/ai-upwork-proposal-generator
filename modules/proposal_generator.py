import sqlite3
import json
import openai
from modules.database import create_tables, insert_fine_tuned_model

def fetch_job_application_data():
    conn = sqlite3.connect('applications.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    query = """
    SELECT jobs.job_category_level_one, jobs.job_category_level_two, jobs.job_type,
           jobs.description, jobs.location, jobs.min_hourly_rate, jobs.max_hourly_rate,
           jobs.engagement, applications.cover_letter
    FROM jobs
    JOIN applications ON jobs.id = applications.job_id;
    """
    cur.execute(query)
    records = cur.fetchall()
    conn.close()

    return records

def prepare_training_data(records):
    training_data = []

    for record in records:
        input_text = f"{record['job_category_level_one']}\n{record['job_category_level_two']}\n{record['job_type']}\n{record['description']}\n{record['location']}\n{record['min_hourly_rate']}-{record['max_hourly_rate']}\n{record['engagement']}"
        output_text = f" {record['cover_letter']}"
        training_example = {"prompt": input_text + "\n\n###\n\n", "completion": output_text + "\n"}
        training_data.append(training_example)

    return training_data

def save_training_data_to_jsonl(training_data, file_path):
    with open(file_path, 'w') as f:
        for example in training_data:
            f.write(json.dumps(example) + '\n')

def upload_training_data(file_path):
    with open(file_path, "rb") as f:
        response = openai.File.create(purpose="fine-tune", file=f)
    return response["id"]

def create_fine_tuned_model(training_file_id, model="davinci"):
    create_tables()

    result = openai.FineTune.create(
        training_file=training_file_id,
        model=model)

    # Insert the newly created fine tuned model details into the database
    insert_fine_tuned_model(result)

    return result

def list_fine_tuned_models():
    return openai.FineTune.list()

def delete_fine_tuned_model(model_id):
    result = openai.Model.delete(model_id)
    return result

def generate_completions(model, prompt):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=100
    )

    # Save the response to a JSON file
    with open("completions.json", "w") as f:
        json.dump(response, f, ensure_ascii=False, indent=4)

    return response