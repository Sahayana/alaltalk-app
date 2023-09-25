import os

from dotenv import load_dotenv


def get_secret(env: str):

    env_file = f".env.{env}"

    try:
        load_dotenv(env_file)
    except Exception as e:
        raise e


def get_env_name():
    env = os.getenv("DJANGO_SETTINGS_MODULE")
    if env:
        return env.split(".")[-1]


def get_current_domain():

    env = get_env_name()

    if env == "dev":
        return "127.0.0.1"
    elif env == "prod":
        return "alaltalk.com"
