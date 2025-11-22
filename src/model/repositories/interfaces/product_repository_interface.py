from abc import ABC, abstractmethod

class ProductRepositoryInterface(ABC):

  def get_all_products(self) -> list:
    pass