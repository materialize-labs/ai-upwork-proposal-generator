from modules.authentication import authenticate
from modules.upwork_calls import get_job_applications, get_user_info

if __name__ == "__main__":
    client = authenticate()

    try:
        # get_user_info(client)
        get_job_applications(client)

    except Exception as e:
        raise e