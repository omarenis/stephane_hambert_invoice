import pandas as pd
import openpyxl

data = {}


def get_formatted_data(filepath):
    book = openpyxl.load_workbook(filepath)
    sheet = book[book.sheetnames[0]]
    cols = []
    for cell in list(sheet.rows)[1]:
        data[cell.value] = []
        cols.append(cell.value)

    for row in list(sheet.rows)[2:]:
        for cell, key in zip(row, list(data.keys())):
            data[key].append(cell.value)
    return pd.DataFrame(data), cols


# See PyCharm help at https://www.jetbrains.com/help/pycharm/


def read_list_clients():
    dataframe = pd.read_excel('Liste-clients.xlsx')
    return list(dataframe['Liste Clients'])


def generate_csv_file(filepath):
    data, cols = get_formatted_data(filepath)
    clients = read_list_clients()
    rslt_df = data[data['SalesOrder.AccountReference'].isin(clients)]
    print(rslt_df)
    rslt_df.to_csv('files/output.csv')

