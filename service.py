import os
from enum import Enum

from pandas import read_csv as read_csv
from Models import Order, CommandLine, BillingOrDelivery


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
    return read_csv(f'{filepath}', delimiter=',')


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
        if formatted.get(i[OrderAttributes.order_id.name]) is None:
            billing = BillingOrDelivery(**i['billing'])
            delivery = BillingOrDelivery(**i['delivery'])
            formatted[i[OrderAttributes.order_id.name]] = Order(order_id=i['order_id'], subtotal=i['subtotal'],
                                                                date_payment=i['date_payment'], carriage=i['carriage'],
                                                                billing=billing, delivery=delivery)
        formatted[i[OrderAttributes.order_id.name]].command_lines.append(CommandLine(hs_code='',
                                                                                     description=i['command_lines'][0][
                                                                                         'description'],
                                                                                     price=i['command_lines'][0][
                                                                                         'price'],
                                                                                     quantity=i['command_lines'][0][
                                                                                         'quantity']))
    return formatted

