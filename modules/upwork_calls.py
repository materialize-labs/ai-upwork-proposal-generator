from pprint import pprint
from upwork.routers import auth
from upwork.routers.hr.freelancers import applications
import json

def get_job_applications(client):
    # Instantiate the applications API with your client
    app_api = applications.Api(client)

    # Define any optional parameters that you need
    optional_params = {
        "status": "active",
        "cursor_limit": 10,
    }

    # Make the API call and store the result
    result = app_api.get_list(optional_params)

    # Save the result to a JSON file
    with open('applications.json', 'w') as f:
        json.dump(result, f, indent=4)

    # Print the result
    print("Result saved to \"applications.json\".")

def get_user_info(client):
    # print("My info")
    # pprint(auth.Api(client).get_user_info())
    return