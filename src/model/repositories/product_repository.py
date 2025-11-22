

from .interfaces.product_repository_interface import ProductRepositoryInterface

class ProductRepository(ProductRepositoryInterface):  

  def __init__(self, db_connection):

    self.__collection = db_connection.get_collection("estoque")


  def get_all_products(self) -> list:
    
    products = self.__collection.find({})

    products_list = [document for document in products]

    return products_list