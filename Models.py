class Discount(object):

    def __init__(self, code, percentage):
        self.code = code
        self.percentage = percentage


class BillingOrDelivery(object):
    def __init__(self, customer_name, _zip, province, city, phone, country, address1, address2):
        self.customer_name = customer_name
        self.zip = _zip
        self.province = province
        self.city = city
        self.phone = phone
        self.country = country
        self.address1 = address1
        self.address2 = address2


class Customer(object):

    def __init__(self, name, email):
        self.name = name
        self.email = email


class Order(object):

    def __init__(self, order_id, subtotal, date_payment, billing, delivery, carriage=5000, command_lines=None):
        self.order_id = order_id
        self.subtotal = subtotal
        self.carriage = carriage
        self.total = subtotal + carriage
        self.date_payment = date_payment
        self.billing = billing
        self.delivery = delivery
        self.command_lines = [] if command_lines is None else command_lines

    def calculate_subtotal(self):
        subtotal = 0
        for i in self.command_lines:
            subtotal += i.price * i.quantity
        self.subtotal = subtotal
        return subtotal


class CommandLine(object):

    def __init__(self, hs_code, description, price, quantity):
        self.hs_code = hs_code
        self.description = description
        self.price = price
        self.quantity = quantity
