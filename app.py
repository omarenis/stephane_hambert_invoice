from flask import Flask, render_template, make_response
from pdfkit import from_string

from service import get_formatted_orders, get_data

app = Flask(__name__)

data = get_formatted_orders(get_data())


@app.route('/orders', methods=['GET'])
def orders():
    return render_template('', orders=orders)


@app.route('/orders/generate_all', methods=['POST'])
def generate_pdf():
    for i in data:
        html = render_template(
            "invoice.html",
            order=i)
        pdf = from_string(html, False)
        with open(f'invoices/invoice{i.id}.pdf', 'wb') as f:
            f.write(pdf)
    return 'success.html'


@app.route('/get_invoice', methods=['GET'])
def get_invoices():
    order = list(data.values())[0]
    print(order.command_lines)
    return render_template('invoice.html', order=order)


@app.route('/orders/<order_id>/generatePdf', methods=['GET'])
def get_invoice(order_id):
    order = data[order_id]
    html = render_template(
        "invoice.html",
        order=order)
    pdf = from_string(html, False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return response


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
