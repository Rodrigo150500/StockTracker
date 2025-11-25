from io import BytesIO

import pandas as pd


def generate_report_stock_data():

    dataframe = pd.DataFrame({
        "CÓDIGO": ["1"],
        "DESCRIÇÃO": ["Produto A"],
        "QUANTIDADE": [15]
    })

    buffer = BytesIO()

    xlsx_buffer =  dataframe.to_excel(buffer)

    data = {
        "buffer": xlsx_buffer
    }
    
    return data
