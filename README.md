# AI-Powered Upwork Proposal Generator

An AI-driven Python application to fine-tune OpenAI models using your Upwork job applications and generate job proposals in response to Upwork job posts.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Setup](#setup)
5. [Running the App](#running-the-app)
    5.1 [Running the Flask web server](#running-the-flask-web-server)
    5.2 [Using command-line arguments](#using-command-line-arguments)
        5.2.1 [Scrape job applications and job details](#scrape-job-applications-and-job-details)
        5.2.2 [Generate training data](#generate-training-data)
        5.2.3 [Fine-tune OpenAI model](#fine-tune-openai-model)
        5.2.4 [List all fine-tuned models](#list-all-fine-tuned-models)
        5.2.5 [Delete a fine-tuned model](#delete-a-fine-tuned-model)
        5.2.6 [Generate a proposal for a single job](#generate-a-proposal-for-a-single-job)
6. [Customizing and Extending the Application](#customizing-and-extending-the-application)
    6.1 [Adding more API calls](#adding-more-api-calls)
    6.2 [Adding new fine-tuning tasks](#adding-new-fine-tuning-tasks)
7. [License](#license)

## Introduction

AI-Powered Upwork Proposal Generator is a Python application that leverages the power of OpenAI's GPT-3 models to help freelancers create tailored and professionally written proposals for Upwork job posts. By training the AI model on your past job applications, the tool learns your unique writing style and job preferences, enabling it to generate personalized and compelling proposals for new job posts. The application utilizes a SQLite database to store job applications, job details, fine-tuned models, and generated proposals.

Using this tool can save you time spent on crafting proposals and increase the chances of winning more jobs. It simplifies the proposal generation process, allowing you to focus more on delivering high-quality work to clients.

## Features

- Authenticate with your Upwork account to fetch your job application data
- Retrieve job application details and job post information
- Scrape job applications and job details and store them in a SQLite database
- Generate and save training data based on your past job applications
- Fine-tune an OpenAI model (GPT-3) using the generated training data
- List, create, and delete fine-tuned models
- Generate personalized job proposals for specific Upwork job posts using the fine-tuned model
- Store fine-tuned model details, model responses, and generated proposals in the SQLite database

## Prerequisites

Before you can use the AI-Powered Upwork Proposal Generator, ensure that you have the following prerequisites:

- Python 3.8 or higher
- `pip` package manager
- An Upwork Developer account with API key and secret
- An OpenAI API key
- A virtual environment tool, such as `virtualenv`

## Setup

Follow these steps to set up the AI-Powered Upwork Proposal Generator on your local machine:

1. Clone the repository:
  ```
  git clone https://github.com/yourusername/upwork_oauth2.git
  ```

2. Change to the project root directory:
  ```
  cd upwork_oauth2
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

## Running the App

1. In a terminal window, run the Flask web server:
  ```
  python3 app.py
  ```

2. In another terminal window, activate the virtual environment and run `main.py` with the desired command-line arguments:
  ```
  source venv/bin/activate
  python3 main.py --flag
  ```

  Replace `--flag` with the desired action(s):
  - `--scrape` - Scrape job applications and job details and save them to the database
  - `--generate-training` - Generate training data based on stored applications and job details
  - `--fine-tune` - Fine-tune a new OpenAI model based on the training data
  - `--list-fine-tunes` - List all fine-tuned models
  - `--delete-model` - Delete a fine-tuned model
  - `--generate-single-job-proposal` - Generate a proposal for a single Upwork job using a fine-tuned model

3. When prompted, copy and paste the authorization URL into your web browser to authorize the app.

4. After authorizing the app, copy the full callback URL (containing the authorization code) and paste it in the terminal window when prompted.

5. The app will now execute the specified action(s).

## Customizing and Extending the Application

The AI-Powered Upwork Proposal Generator can be customized and extended to meet your specific needs. Here's how you can add more functionality:

### 6.1 Adding more API calls

You can add more Upwork API calls to the `upwork_calls.py` module. Create new functions that use the `client` object to interact with Upwork APIs. This will allow you to fetch additional data or perform different actions on the platform.

### 6.2 Adding new fine-tuning tasks

You can also customize the `proposal_generator.py` module to fine-tune the OpenAI model for different tasks. Add new functions or modify existing ones to change the inputs, fine-tuning parameters, or training data generation process. This will help you create models that generate better proposals or work on other text generation tasks.

## License

This project is released under the [Apache License 2.0](LICENSE). By using the AI-Powered Upwork Proposal Generator, you agree to the terms and conditions stated in the license.
