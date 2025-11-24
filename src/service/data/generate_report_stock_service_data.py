import pandas as pd
import string
from io import BytesIO

def generate_report_stock_service_data():
    
    alphabet = string.ascii_uppercase

    products = []
    codes = []

    for i in range(len(alphabet)):
        products.append(f"Product {alphabet[i]}")
        codes.append(f"{i},0")
    
    amount = codes.copy()

    dataframe = pd.DataFrame({
        "CÓDIGO":codes,
        "DESCRIÇÃO":products,
        "QUANTIDADE":amount
    })

    buffer = BytesIO()


    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        workbook  = writer.book
        worksheet = workbook.add_worksheet("Sheet1")
        writer.sheets["Sheet1"] = worksheet
        
        # Escrever 12 linhas vazias
        for row in range(12):
            worksheet.write_row(row, 0, ["", "", ""])
        
        # Agora escrever o dataframe a partir da linha 13 (index 12)
        dataframe.to_excel(writer, sheet_name="Sheet1", index=False, startrow=12)
        
    get_all_products = [
        {
            "_id": "algo",
            "1": [
                {
                    "description": "Produto Teste",
                    "stock": 5,
                    "location": "P3"
                }
            ],
            "2": [
                {
                    "description": "Produto 1",
                    "stock": 6,
                    "location": "P3"
                },
                {
                    "description": "Produto 2",
                    "stock": 8,
                    "location": "P4"
                }
            ]
        },
        {
            "_id": "13",
            "3": [
                {
                    "description": "Produto Teste",
                    "stock": 5,
                    "location": "P3"
                }
            ],
            "4": [
                {
                    "description": "Produto 3",
                    "stock": 7,
                    "location": "P5"
                },
                {
                    "description": "Produto 4",
                    "stock": 8,
                    "location": "CX01"
                }
            ]
        }
    ]

    data = {
        "buffer": buffer,
        "get_all_products": get_all_products
    }

    return data