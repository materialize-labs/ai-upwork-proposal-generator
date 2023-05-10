import sqlite3
import json

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
        output_text = record['cover_letter']
        training_example = f"{input_text}\n<|start|>\n{output_text}\n<|end|>"
        training_data.append(training_example)

    return training_data

def save_training_data_to_json(training_data, file_path):
    with open(file_path, 'w') as f:
        json.dump(training_data, f)