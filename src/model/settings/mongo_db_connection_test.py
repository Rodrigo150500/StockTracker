from dotenv import load_dotenv
load_dotenv("dev.env")

from .mongo_db_connection import mongo_db_connection

def test_connection():

    mongo_db_connection.connect()

    assert mongo_db_connection.get_db_connection() is not None