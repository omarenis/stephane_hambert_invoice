from flask import Flask, render_template, make_response
from pdfkit import from_string

from service import get_formatted_orders, get_data

app = Flask(__name__)

data = list(get_formatted_orders(get_data()))


@app.route('/orders', methods=['GET'])
def orders():
    return render_template('', orders=orders)


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
