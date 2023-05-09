from pprint import pprint
from upwork.routers import auth
from upwork.routers.hr.freelancers import applications
from upwork.routers.jobs import profile
from datetime import datetime, timedelta
from modules.database import create_tables, insert_applications_and_questions
import json


def get_job_applications(client):
    # Uses this API:
    # https://developers.upwork.com/?lang=python#contracts-and-offers_list-job-applications-as-freelancer
    
    create_tables()

    # Instantiate the applications API with your client
    app_api = applications.Api(client)

    # Get the timestamp from 3 months ago
    timestamp_from = int((datetime.now() - timedelta(days=1)).timestamp())

    # Define any optional parameters that you need
    optional_params = {
        "status": "submitted",
        "cursor_limit": 20,
    }

    statuses_to_check = ["submitted", "archived"]

    for status in statuses_to_check:
        optional_params["status"] = status
        # Flag to check if there are applications to process
        has_applications = True

        while has_applications:
            # Make the API call and store the result
            result = app_api.get_list(optional_params)

            # Filter applications by timestamp
            recent_applications = list(filter(
                lambda x: int(datetime.fromisoformat(x["auditDetails"]["createdTs"].rstrip('Z')).timestamp()) >= timestamp_from,
                result["data"]["applications"]
            ))

            # Save the recent applications to a SQLite database
            insert_applications_and_questions(recent_applications, client, get_job_details)

            if not recent_applications:  # No recent applications in the current batch
                has_applications = False

            else:
                # Check if there's a next cursor
                if "paging" in result["data"]:
                    total_applications = int(result["data"]["paging"]["total"])
                    current_offset = int(result["data"]["paging"]["count"])  # current page size

                    if current_offset < total_applications:
                        # Update the cursor to the next offset value
                        encoded_offset = result["data"]["paging"]["offset"]
                        optional_params["cursor"] = encoded_offset
                    else:
                        # No more applications available
                        has_applications = False
                else:
                    # No more applications available
                    has_applications = False

    # Print the result
    print("Job Applications saved to database.")

def get_job_details(client, job_key):
    # Uses this API:
    # https://developers.upwork.com/?lang=python#jobs_get-job-profile

    # Instantiate the jobs API with your client
    profile_api = profile.Api(client)

    # Get the job details by key (sent as "opening_ciphertext")
    job_details = profile_api.get_specific(job_key)

    return job_details

def get_user_info(client):
    print("My info")
    pprint(auth.Api(client).get_user_info())
    return