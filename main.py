from modules.authentication import get_desktop_client
from modules.upwork_calls import get_job_applications, get_user_info

if __name__ == "__main__":
    client = get_desktop_client()

    try:
        get_user_info(client)
        get_job_applications(client)

    except Exception as e:
        raise e