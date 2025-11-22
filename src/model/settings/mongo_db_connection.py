import os
from pymongo import MongoClient

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
IP_ADDRESS = os.getenv("IP_ADDRESS")
PORT = os.getenv("MONGO_PORT")

DATABASE_NAME = os.getenv("DATABASE_NAME_MONGO_DB")


class MongoDBConnetion:
  def __init__(self):
    self.__connection_string = "mongodb://{}:{}@{}:{}/?authSource=admin".format(
      USER,
      PASSWORD,
      IP_ADDRESS,
      PORT
    )

    self.__database_name = DATABASE_NAME
    self.__client = None
    self.__db_connection = None

  def connect(self):

    self.__client = MongoClient(self.__connection_string)

    self.__db_connection = self.__client[self.__database_name]

  def get_db_connection(self):
    return self.__db_connection

mongo_db_connection = MongoDBConnetion()
