from dotenv import dotenv_values

config = dotenv_values(".env")

BACKEND_URL = config['BACKEND_URL']