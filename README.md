Here's the updated README file with the latest information about the app and a mention of the `.env.example` file:

# Upwork OAuth2 Python App

This is a Python app that demonstrates the authentication process with the Upwork API using OAuth 2.0, retrieves job applications for a freelancer, and stores the data in a SQLite database.

## Features

- Authenticate with the Upwork API
- Retrieve the user's information
- List job applications as a freelancer
- Store job applications and associated details in a SQLite database

## Prerequisites

- Python 3.8+
- `pip` package manager
- An Upwork API key and secret
- A virtual environment (`virtualenv`)

## Setup

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

6. Set up your client key (`UPWORK_CLIENT_KEY`) and client secret (`UPWORK_CLIENT_SECRET`) in the `.env` file:
  ```
  UPWORK_CLIENT_KEY=your_client_key
  UPWORK_CLIENT_SECRET=your_client_secret
  ```

## Running the App

1. In a terminal window, run the Flask web server:
  ```
  python3 app.py
  ```

2. In another terminal window, activate the virtual environment and run `main.py`:
  ```
  source venv/bin/activate
  python3 main.py
  ```

3. When prompted, copy and paste the authorization URL into your web browser to authorize the app.

4. After authorizing the app, copy the full callback URL (containing the authorization code) and paste it in the terminal window when prompted.

5. The app will now display the authenticated user's information and store the list of job applications and associated details in the SQLite database.

## Adding More API Calls

You can add more Upwork API calls to the `upwork_calls.py` module. Update the module with new functions that utilize the `client` object to interact with Upwork APIs.

## License

[Apache License 2.0](LICENSE)
