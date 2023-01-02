import os
import pprint
import zipfile
from enum import Enum

import pandas
import pandas as pd
from pandas import read_csv as read_csv, read_excel as read_excel
from Models import Order, CommandLine, BillingOrDelivery


def format_data(items, filtered_data):
    if items.shape[0] != 0:
        data = items.to_dict()
        for i in data:
            for value in list(data[i].values()):
                filtered_data[i].append(value)
    return filtered_data


def upload_file(PRODUCTION, upload_file):
    file_path = f'{"/home/ubuntu" if PRODUCTION == False else "/root"}/stephane_hambert_invoice/files/{upload_file.filename}'
    upload_file.save(file_path)
    return upload_file, file_path


def filter_products(products_dataframe, product_filter_dataframe: pandas.DataFrame):
    for i in product_filter_dataframe.columns:
        print()


def get_billing_or_delivery_data(data, attributes, index):
    return {
        'customer_name': data[attributes.customer_name.value][index],
        'city': data[attributes.city.value][index],
        '_zip': data[attributes.zip.value][index],
        'province': data[attributes.province.value][index],
        'country': data[attributes.country.value][index],
        'phone': data[attributes.phone.value][index],
        'address1': data[attributes.address1.value][index],
        'address2': data[attributes.address2.value][index]
    }


class OrderAttributes(Enum):
    order_id = 'Order ID'
    total = 'Total'
    date_payment = 'Paid at'
    carriage = 'Shipping'


class ItemAttributes(Enum):
    brand = 'Brand'
    hs_code = ''
    product_code = 'Lineitem sku'
    description = 'Lineitem name'
    price = 'Lineitem price'
    quantity = 'Lineitem quantity'
    total = 0


class BillingAttributes(Enum):
    customer_name = 'Billing Name'
    zip = 'Billing Zip'
    province = 'Billing Province'
    city = 'Billing City'
    phone = 'Billing Phone'
    country = 'Billing Country'
    address1 = 'Billing Address1'
    address2 = 'Billing Address2'


class DiscountAttributes(Enum):
    discount_code = 'Discount Code'
    discount_amount = 'Discount Amount'


class ShippingMethodAttributes(Enum):
    method = 'Shipping Method'
    phone = 'Shipping Phone'
    zip = 'Shipping Zip'
    province = 'Shipping Province'
    city = 'Shipping City'
    country = 'Shipping Country'
    address1 = 'Shipping Address1'
    address2 = 'Shipping Address2'
    customer_name = 'Shipping Name'


def read_file(filepath):
    if filepath.endswith('.csv'):
        return read_csv(f'{filepath}', delimiter=',')
    return read_excel(f'{filepath}')


def get_data(dataframe):
    data = dataframe.to_dict()
    formatted = []
    for i in data[OrderAttributes.order_id.value]:
        formatted.append({
            'order_id': data[OrderAttributes.order_id.value][i],
            'subtotal': data[OrderAttributes.total.value][i],
            'carriage': data[OrderAttributes.carriage.value][i],
            'date_payment': data[OrderAttributes.date_payment.value][i],
            'billing': get_billing_or_delivery_data(data, BillingAttributes, i),
            'delivery': get_billing_or_delivery_data(data, ShippingMethodAttributes, i),
            'command_lines': [
                {
                    'quantity': int(data[ItemAttributes.quantity.value][i]),
                    'hs_code': data[ItemAttributes.product_code.value][i],
                    'price': float(data[ItemAttributes.price.value][i]),
                    'description': data[ItemAttributes.description.value][i]
                }
            ]
        })
    return formatted


def get_formatted_orders(list_orders):
    formatted = {}
    for i in list_orders:
        print(i['command_lines'])
        if formatted.get(i[OrderAttributes.order_id.name]) is None:
            billing = BillingOrDelivery(**i['billing'])
            delivery = BillingOrDelivery(**i['delivery'])
            formatted[i[OrderAttributes.order_id.name]] = Order(order_id=i['order_id'], subtotal=i['subtotal'],
                                                                date_payment=i['date_payment'], carriage=i['carriage'],
                                                                billing=billing, delivery=delivery)
        formatted[i[OrderAttributes.order_id.name]].command_lines.append(
            CommandLine(hs_code=i['command_lines'][0]['hs_code'],
                        description=i['command_lines'][0][
                            'description'],
                        price=i['command_lines'][0][
                            'price'],
                        quantity=i['command_lines'][0][
                            'quantity']))
        formatted[i[OrderAttributes.order_id.name]].calculate_subtotal()
    return formatted


def initialize_filtered_data(products):
    filtered_data = dict()
    for i in products.columns:
        filtered_data[i] = []
    return filtered_data


def generate_resultat_trie_zip_file(PRODUCTION, products):
    files_path = f'{"/root" if PRODUCTION is True else "/home/ubuntu"}/stephane_hambert_invoice/files'
    filterings = pd.read_excel(f'{files_path}/Trier-produit.xlsx')
    zipFile = zipfile.ZipFile(f'{files_path}/resultat_trie.zip', 'w')
    filtered_data = dict()
    for i in products.columns:
        filtered_data[i] = []
    for filtering in filterings:
        product_codes = list(filterings[filtering].values)
        print(filtering)
        for product_code in product_codes:
            if product_code is not None and products[products['Product Code'] == product_code].shape[0] != 0:
                products_items = products[products['Product Code'] == product_code]
                filtered_data = format_data(products_items, filtered_data)
        pprint.pprint(filtered_data)
        dataframe = pd.DataFrame(filtered_data, columns=products.columns)
        dataframe.to_csv(f'{files_path}/{filtering}.csv', index=False)
        zipFile.write(f'{files_path}/{filtering}.csv', f'{filtering}.csv')
        os.remove(f'{files_path}/{filtering}.csv')
        filtered_data = initialize_filtered_data(products=products)
    return None
