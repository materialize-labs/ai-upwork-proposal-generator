# AI-Powered Upwork Proposal Generator

An AI-driven Python application to fine-tune OpenAI models using your Upwork job applications and generate job proposals in response to Upwork job posts.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Setup](#setup)
5. [Running the App](#running-the-app)
    - [5.1 Running the Flask web server](#running-the-flask-web-server)
    - [5.2 Using command-line arguments](#using-command-line-arguments)
        - [5.2.1 Scrape job applications and job details](#scrape-job-applications-and-job-details)
        - [5.2.2 Generate training data](#generate-training-data)
        - [5.2.3 Fine-tune OpenAI model](#fine-tune-openai-model)
        - [5.2.4 List all fine-tuned models](#list-all-fine-tuned-models)
        - [5.2.5 Delete a fine-tuned model](#delete-a-fine-tuned-model)
        - [5.2.6 Generate a proposal for a single job](#generate-a-proposal-for-a-single-job)
6. [Customizing and Extending the Application](#customizing-and-extending-the-application)
    - [6.1 Adding more API calls](#adding-more-api-calls)
    - [6.2 Adding new fine-tuning tasks](#adding-new-fine-tuning-tasks)
7. [License](#license)

## 1. Introduction

AI-Powered Upwork Proposal Generator is a Python application that leverages the power of OpenAI's GPT-3 models to help freelancers create tailored and professionally written proposals for Upwork job posts. By training the AI model on your past job applications, the tool learns your unique writing style and job preferences, enabling it to generate personalized and compelling proposals for new job posts. The application utilizes a SQLite database to store job applications, job details, fine-tuned models, and generated proposals.

Using this tool can save you time spent on crafting proposals and increase the chances of winning more jobs. It simplifies the proposal generation process, allowing you to focus more on delivering high-quality work to clients.

## 2. Features

- Authenticate with your Upwork account to fetch your job application data
- Retrieve job application details and job post information
- Scrape job applications and job details and store them in a SQLite database
- Generate and save training data based on your past job applications
- Fine-tune an OpenAI model (GPT-3) using the generated training data
- List, create, and delete fine-tuned models
- Generate personalized job proposals for specific Upwork job posts using the fine-tuned model
- Store fine-tuned model details, model responses, and generated proposals in the SQLite database

## 3. Prerequisites

Before you can use the AI-Powered Upwork Proposal Generator, ensure that you have the following prerequisites:

- Python 3.8 or higher
- `pip` package manager
- An Upwork Developer account with API key and secret
- An OpenAI API key
- A virtual environment tool, such as `virtualenv`

## 4. Setup

Follow these steps to set up the AI-Powered Upwork Proposal Generator on your local machine:

1. Clone the repository:
  ```
  git clone git@github.com:materialize-labs/ai-upwork-proposal-generator.git
  ```

2. Change to the project root directory:
  ```
  cd ai-upwork-proposal-generator
  ```

3. Create a virtual environment and activate it:
  ```
  python3 -m venv venv
  source venv/bin/activate
  ```

4. Install the required packages using `pip`:
  ```
  pip3 install -r requirements.txt
  ```

5. Copy the `.env.example` file to a `.env` in the project root directory:
  ```
  cp .env.example .env
  ```

6. Set up your Upwork client key (`UPWORK_CLIENT_KEY`), client secret (`UPWORK_CLIENT_SECRET`), and OpenAI API key (`OPENAI_API_KEY`) in the `.env` file:
  ```
  UPWORK_CLIENT_KEY=your_client_key
  UPWORK_CLIENT_SECRET=your_client_secret
  OPENAI_API_KEY=your_openai_api_key
  ```

## 5. Running the App

To run the AI-Powered Upwork Proposal Generator, you will first need to start the Flask web server, which handles authentication. Afterward, you can use various command-line arguments to execute different actions within the application like scraping data, fine-tuning models, or generating proposals. The following subsections will guide you through these steps.

### 5.1 Running the Flask web server

The application uses the Flask web server to handle the authentication callback from Upwork. Before executing any command-line actions from `main.py`, you need to start the Flask web server by following these steps:

1. Open a terminal window and navigate to the project root directory.
2. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```
3. Run the Flask web server:
   ```
   python3 app.py
   ```
The Flask web server will now be running and ready to process the authentication callback when you run `main.py` with the desired command-line arguments.

### 5.2 Using command-line arguments

The `main.py` script supports several command-line arguments that allow you to perform different actions within the application, such as scraping job data, fine-tuning models, and generating proposals. To use these arguments, follow these steps:

1. Open a new terminal window, navigate to the project root directory, and activate the virtual environment:
   ```
   source venv/bin/activate
   ```

2. Run `main.py` with the desired command-line argument by replacing `--flag` with the corresponding action flag:
   ```
   python3 main.py --flag
   ```

The available command-line arguments and their corresponding actions are described in the following subsections (5.2.1 - 5.2.6).

### 5.2.1 Scrape job applications and job details

To scrape job applications and job details and save them in the SQLite database, use the `--scrape` flag:

```
python3 main.py --scrape
```

The script will fetch job application data for your Upwork account and store it in the database.

### 5.2.2 Generate training data

To generate training data based on your stored job applications and job details, use the `--generate-training` flag:

```
python3 main.py --generate-training
```

This will process your job application data and create a training dataset for fine-tuning the OpenAI model.

### 5.2.3 Fine-tune OpenAI model

To fine-tune a new OpenAI model based on the generated training data, use the `--fine-tune` flag:

```
python3 main.py --fine-tune
```

The script will use the training dataset to fine-tune the GPT-3 model, creating a model customized to your job applications.

### 5.2.4 List all fine-tuned models

To list all the fine-tuned models you have created, use the `--list-fine-tunes` flag:

```
python3 main.py --list-fine-tunes
```

The script will display a list of your fine-tuned models and their details.

### 5.2.5 Delete a fine-tuned model

To delete a specific fine-tuned model from the database, use the `--delete-model` flag followed by the model ID:

```
python3 main.py --delete-model <model_id>
```

Replace `<model_id>` with the actual ID of the model you want to delete.

### 5.2.6 Generate a proposal for a single job

To generate a proposal for a single Upwork job using a fine-tuned model, use the `--generate-single-job-proposal` flag followed by the `--model-id` and `--job-url` flags:

```
python3 main.py --generate-single-job-proposal --model-id <model_id> --job-url <job_url>
```

Replace `<model_id>` with the ID of the fine-tuned model you want to use and `<job_url>` with the URL of the Upwork job post you want to create a proposal for. The script will generate a personalized proposal for the specified job post and display it in the terminal.

## 6. Customizing and Extending the Application

The AI-Powered Upwork Proposal Generator can be customized and extended to meet your specific needs. Here's how you can add more functionality:

### 6.1 Adding more API calls

You can add more Upwork API calls to the `upwork_calls.py` module. Create new functions that use the `client` object to interact with Upwork APIs. This will allow you to fetch additional data or perform different actions on the platform.

### 6.2 Adding new fine-tuning tasks

You can also customize the `proposal_generator.py` module to fine-tune the OpenAI model for different tasks. Add new functions or modify existing ones to change the inputs, fine-tuning parameters, or training data generation process. This will help you create models that generate better proposals or work on other text generation tasks.

## 7. License

This project is released under the [Apache License 2.0](LICENSE). By using the AI-Powered Upwork Proposal Generator, you agree to the terms and conditions stated in the license.
