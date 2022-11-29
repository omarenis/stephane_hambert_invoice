import os

from flask import Flask, render_template, make_response, request, send_file
from pdfkit import from_string

from service import get_formatted_orders, get_data, read_file

app = Flask(__name__)

UPLOAD_FOLDER = 'files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/orders', methods=['GET'])
def orders():
    return render_template('', orders=orders)


@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/orders/generate_all', methods=['POST'])
def generate_pdf():
    upload_file = request.files.get('file')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], upload_file.filename)
    upload_file.save(file_path)
    orders = get_formatted_orders(get_data(read_file(file_path)))
    for i in orders:
        html = render_template(
            "invoice.html",
            order=orders[i])
        pdf = from_string(html, False)
        with open(f'files/invoice{orders[i].order_id}.pdf', 'wb') as f:
            f.write(pdf)
    return render_template('success.html')


@app.route('/orders/<_id>/generatePdf')
def get_pdf(_id):
    with open(f'files/invoice{id}.pdf', 'rb') as static_file:
        return send_file(static_file)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
