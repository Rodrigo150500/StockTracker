import pandas as pd
from io import BytesIO, StringIO
from pandas import DataFrame

from src.model.repositories.interfaces.product_repository_interface import ProductRepositoryInterface

from src.main.http_types.http_response import HttpResponse
from src.errors.types.http_bad_request import HttpBadRequest
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntity
from src.errors.types.http_service_unvailable import HttpServiceUnvailable
from src.errors.types.http_internal_server_error import HttpInternalServerError

from werkzeug.datastructures import FileStorage

from zipfile import ZipFile

from .interfaces.generate_report_stock_service_interface import GenerateReportStockServiceInterface


class GenerateReportStockService(GenerateReportStockServiceInterface):

    def __init__(self, repository: ProductRepositoryInterface):
        
        self.__repository = repository


    def generate_report(self, xlsx_file: FileStorage) -> BytesIO:

        #Transform to csv file
        csv_file = self.__transform_to_csv_file(xlsx_file)
        
        #Filter columns
        csv_formatted = self.__format_csv_file(csv_file)
        
        #Comparer to database
        products_found, products_not_found = self.__compare_xlsx_with_database(csv_formatted)

        #Export to csv
        products_buffer = self.__export_csv_filtred(products_found, products_not_found)

        #Export to download
        files_to_download = self.__create_zip_file(products_buffer)

        return files_to_download

    def __transform_to_csv_file(self, xlsx_file) -> BytesIO:

        try:

            buffer = BytesIO()

            df_excel = pd.read_excel(xlsx_file)

            df_excel.to_csv(buffer, sep=";", encoding="utf-8", index=False)

            buffer.seek(0)

            return buffer  
        
        except Exception as exception:

            print(f"Error [GenerateReportService][__transform_to_csv_file]: {str(exception)} ")
    
            raise HttpBadRequest("Verifique o arquivo enviado")


    def __format_csv_file(self, csv_file: BytesIO) -> DataFrame:
        
        try:

            df = pd.read_csv(csv_file, sep=";", skiprows=[0,1,2,3,4,5,6,7,8,9,10,11])
            
            data = {
                "code": df["CÓDIGO"],
                "description": df['DESCRIÇÃO'],
                "amount": df["QUANTIDADE"],
            }
            csv_formatted = pd.DataFrame(data)

            #Getting products that has amount > 0
            csv_formatted.drop(df.tail(2).index, inplace=True)
            csv_formatted["amount"] = csv_formatted["amount"].str.replace(",", ".")
            csv_formatted["amount"] = csv_formatted["amount"].astype(float)
            csv_formatted = csv_formatted[csv_formatted["amount"] > 0]

            return csv_formatted

        except Exception as exception:

            print(f"Error [GenerateReportService][__format_csv_file]: {str(exception)} ")

            raise HttpBadRequest("Verifique o arquivo enviado")
    

    def __compare_xlsx_with_database(self, csv_filtered: DataFrame) -> tuple:
        
        try:

            code_list = csv_filtered['code']

            products_in_database = self.__format_products_from_database()

            key_list = list(products_in_database.keys())

            products_found = []
            products_not_found = []   
            
            for code in code_list:
        
                if code in key_list and int(products_in_database[code]["stock"]) > 0:

                    data = {
                        "code": code,
                        "description": products_in_database[code]["description"],
                        "replacement": csv_filtered.loc[csv_filtered['code'] == code, "amount"].item(),
                        "location": products_in_database[code]["location"] if "location" in products_in_database[code] else ""}

                    products_found.append(data)

                else:
                    data = {
                    "code": code,
                    "description": csv_filtered.loc[csv_filtered["code"] == code, "description"].item(),
                    "replacement": csv_filtered.loc[csv_filtered['code'] == code, "amount"].item()}

                    products_not_found.append(data)

            return(products_found, products_not_found)
        
        except Exception as exception:

            print(f"Error [GenerateReportService][__compare_xlsx_with_database]: {str(exception)} ")

            raise HttpUnprocessableEntity("Erro: Não foi possível comparar o XLSX com o banco de dados")


    def __format_products_from_database(self) -> dict:

        try:
            
            products = self.__repository.get_all_products()

            products_in_database = {}

            for document in products:

                document.pop("_id",None)

                location = []

                stock = 0

                location_result = ""

                for code, data in document.items():

                    products_in_database[code] = {"description": data[0].get("description", "")}

                    for item in data:

                        stock += item["stock"]

                        if "location" in item:

                            location.append(item["location"])
                        

                    if len(location) > 0:

                        location_with_no_duplicate_values = list(set(location))

                        for item_location in location_with_no_duplicate_values:

                            location_result += f"{item_location} "

                        products_in_database[code]["location"] = location_result
                        
                    products_in_database[code]["stock"] = stock

            return products_in_database
        
        except Exception as exception:

            print(f"Error [GenerateReportService][__format_products_from_database]: {str(exception)} ")

            raise HttpServiceUnvailable("Erro: Serviço interno no servidor indisponível")
        

    def __export_csv_filtred(self, products_found: list, products_not_found: list) -> dict:
        
        try:

            products_found_dict = {
            "CODIGO": [],
            "DESCRICAO": [],
            "LOCALIZACAO": [],
            "REPOSICAO": []
            }

            products_not_found_dict = {
            "CODIGO": [],
            "DESCRICAO": [],
            "REPOSICAO": []
            }

            for product in products_found:
                products_found_dict["CODIGO"].append(product["code"])
                products_found_dict["DESCRICAO"].append(product["description"])
                products_found_dict["REPOSICAO"].append(product["replacement"])
                products_found_dict["LOCALIZACAO"].append(product["location"])

            for product in products_not_found:
                products_not_found_dict["CODIGO"].append(product["code"])
                products_not_found_dict["DESCRICAO"].append(product["description"])
                products_not_found_dict["REPOSICAO"].append(product["replacement"])

            df_product_found = pd.DataFrame(products_found_dict)
            df_product_not_found = pd.DataFrame(products_not_found_dict)
            
            buffer = {
            "products_found": StringIO(),
            "products_not_found": StringIO()}

            df_product_found.to_csv(buffer["products_found"], sep=";", encoding="utf-8", index=False)
            df_product_not_found.to_csv(buffer["products_not_found"], sep=";", encoding="utf-8", index=False)
            
            buffer["products_found"].seek(0)
            buffer["products_not_found"].seek(0)

            return buffer 

        except Exception as exception:

            print(f"Error [GenerateReportService][__export_csv_filtred]: {str(exception)} ")

            raise HttpInternalServerError("Erro: Erro ao exportar o csv")


    def __create_zip_file(self, files: dict) -> BytesIO:

        try:

            products_found = files["products_found"]
            products_not_found = files["products_not_found"]

            zip_buffer = BytesIO()

            with ZipFile(zip_buffer, "w") as zip_file:
                zip_file.writestr("Produtos_encontrados.csv", products_found.getvalue())
                zip_file.writestr("Produtos_não_encontrados.csv", products_not_found.getvalue())

            zip_buffer.seek(0)

            return zip_buffer

        except Exception as exception:

            print(f"Error [GenerateReportService][__export_to_download]: {str(exception)} ")

            raise HttpInternalServerError("Erro: Erro ao fazer o download")









