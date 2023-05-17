import sqlite3
import json
import openai
import time
from tiktoken import get_encoding
from modules.database import insert_fine_tuned_model, insert_model_response
from modules import openai_client
from rich.console import Console

console = Console()

encoding = get_encoding("cl100k_base")

def count_tokens(text):
    return len(encoding.encode(text))

def fetch_job_application_data():
    conn = sqlite3.connect('applications.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    query = """
    SELECT jobs.job_category_level_one, jobs.job_category_level_two, jobs.description,
           jobs.engagement, applications.cover_letter
    FROM jobs
    JOIN applications ON jobs.id = applications.job_id
    LIMIT 10;
    """
    cur.execute(query)
    records = cur.fetchall()
    conn.close()

    return records

def prepare_prompt_data(records):
    json_data = []

    for record in records:
        node = {
            'job_description': record['description'],
            'cover_letter': record['cover_letter']
        }
        json_data.append(node)

    return json_data

def prepare_training_data(records):
    # Convert records to a list of dictionaries
    records_list = [dict(record) for record in records]

    # Convert records into required training format
    formatted_records = []
    for record in records_list:
        prompt_input = f'Job Category Level One: {record["job_category_level_one"]}\n'
        prompt_input += f'Job Category Level Two: {record["job_category_level_two"]}\n'
        prompt_input += f'Description: {record["description"]}\n'
        prompt_input += f'Engagement: {record["engagement"]}\n\n###\n\n'

        formatted_records.append({"prompt": prompt_input, "completion": f' {record["cover_letter"]} END'})

    # Convert list of formatted records into JSONL
    jsonl_data = "\n".join(json.dumps(formatted_record) for formatted_record in formatted_records)
    
    return jsonl_data

def save_data_to_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json_string = json.dumps(data, ensure_ascii=False, indent=2)
        f.write(json_string)

def upload_training_data(file_path):
    with open(file_path, "rb") as f:
        response = openai.File.create(purpose="fine-tune", file=f)
    return response["id"]

def create_fine_tuned_model(training_file_id, model="davinci"):
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

def generate_completions(model, prompt, max_tokens, stop, n, temperature):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        stop=stop,
        n=n,
        temperature=temperature
    )

    # Save the response to a JSON file
    with open('completions.json', 'w') as f:
        json.dump(response, f, ensure_ascii=False, indent=4)

    insert_model_response(prompt, model, max_tokens, stop, n, temperature, response)

    return response

def generate_cover_letter(new_job_description):
    
    console.print("[cyan]Loading prompt data...[/cyan]")
    # Load prompt data
    with open("prompt_data.json", "r") as f:
        prompt_data = json.load(f)
    console.print("[green]Prompt data loaded successfully.[/green]")

    # Set up a message history for the conversation
    messages = [{"role": "system", "content": "You are an assistant that helps in generating cover letters based on previous job descriptions and cover letters."}]

    # Token limit for GPT-4
    token_limit = 4096

    # Add examples, staying within the token limit
    total_tokens = 0
    console.print("[cyan]Preparing messages...[/cyan]")
    for example in prompt_data:
        job_message = f"Job description: {example['job_description']}"
        cover_message = f"Cover letter: {example['cover_letter']}"
        
        new_tokens = count_tokens(job_message) + count_tokens(cover_message) + 4  # Adding tokens for user and assistant roles, and some formatting tokens
        if total_tokens + new_tokens + 60 < token_limit:  # Saving 50 tokens for new instruction and response
            messages.append({"role": "user", "content": job_message})
            messages.append({"role": "assistant", "content": cover_message})
            total_tokens += new_tokens
        else:
            break
    console.print("[green]Messages prepared successfully.[/green]")

    messages.append({"role": "user", "content": f"Based on previous cover letters, generate a cover letter for this job description: {new_job_description}. Do not make up any projects that we haven't built in the past."})

    console.print("[cyan]Making the API call...[/cyan]")
    # Make the API call
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Assuming this is the model you want to use
        messages=messages,
        temperature=0.8
    )
    console.print("[green]API call completed successfully.[/green]")

    # Extract the generated cover letter
    generated_cover_letter = response['choices'][0]['message']['content']

    # Save the response to a JSON file
    console.print("[cyan]Saving response to JSON file...[/cyan]")
    with open('cover_letter.json', 'w') as f:
        json.dump(response, f, ensure_ascii=False, indent=4)
    console.print("[green]Response saved successfully in 'cover_letter.json'.[/green]")

    return generated_cover_letter