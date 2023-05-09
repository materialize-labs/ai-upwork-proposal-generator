import upwork
from pprint import pprint
from upwork.routers import auth
import json
import os.path
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

consumer_key = os.getenv("UPWORK_CLIENT_KEY")
consumer_secret = os.getenv("UPWORK_CLIENT_SECRET")

def authenticate():
    print("Emulating desktop app")

    # Check if token file exists
    if os.path.isfile('token.json'):
        with open('token.json', 'r') as f:
            token_data = json.load(f)

        # Use the stored token data to initialize the upwork.Client
        config = upwork.Config(
            {
                "client_id": consumer_key,
                "client_secret": consumer_secret,
                "token": token_data
            }
        )
    else:
        config = upwork.Config(
            {
                "client_id": consumer_key,
                "client_secret": consumer_secret,
                "redirect_uri": "http://localhost:3000/callback",
            }
        )

    client = upwork.Client(config)

    try:
        config.token
    except AttributeError:
        authorization_url, state = client.get_authorization_url()
        # cover "state" flow if needed
        authz_code = input(
            "Please enter the full callback URL you get "
            "following this link:\n{0}\n\n> ".format(authorization_url)
        )

        print("Retrieving access and refresh tokens.... ")
        token = client.get_access_token(authz_code)
        
        # WARNING: the access token will be refreshed automatically for you
        # in case it's expired, i.e. expires_at < time(). Make sure you replace the
        # old token accordingly in your security storage. Call client.get_actual_config
        # periodically to sync-up the data

        pprint(token)
        print("OK")


        with open('token.json', 'w') as f:
            json.dump(token, f)

    return client