from dotenv import load_dotenv
load_dotenv(".env")

from .product_repository import ProductRepository
from src.model.settings.mongo_db_connection import mongo_db_connection

def test_get_all_product():

    mongo_db_connection.connect()

    connection = mongo_db_connection.get_db_connection()

    repository = ProductRepository(connection)

    products = repository.get_all_products()

    assert isinstance(products, list)
