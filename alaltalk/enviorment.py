from dotenv import load_dotenv


def get_secret(env: str):

    env_file = f".env.{env}"

    try:
        load_dotenv(env_file)
    except Exception as e:
        raise e
