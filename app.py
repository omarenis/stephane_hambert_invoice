import os
import zipfile
from flask import Flask, render_template, request, send_from_directory, jsonify
from pdfkit import from_string, configuration
from service import get_formatted_orders, get_data, read_file
Config = configuration(wkhtmltopdf=' /usr/bin/wkhtmltopdf')
app = Flask(__name__)
DOWNLOAD_DIRECTORY = "files"
UPLOAD_FOLDER = 'files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/orders', methods=['GET'])
def orders():
    return render_template('', orders=orders)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')



@app.route('/orders/generate_all', methods=['POST'])
def generate_pdf():
    upload_file = request.files.get('file')
    file_path  = f'/home/ubuntu/stephane_hambert_invoice/files/{upload_file.filename}'
    upload_file.save(file_path)
    orders = get_formatted_orders(get_data(read_file(file_path)))
    with zipfile.ZipFile('files/invoices.zip', 'w') as myzip:
        for i in orders:
            print(orders[i].command_lines[0].hs_code)
            html = render_template(
                "invoice.html",
                order=orders[i])
            from_string(html, f'files/invoice{orders[i].order_id}.pdf', configuration=Config)
            myzip.write(f'files/invoice{orders[i].order_id}.pdf')
            os.remove(f'files/invoice{orders[i].order_id}.pdf')
    return jsonify(success=True)


@app.route('/downloadZip')
def get_pdfs():
    return send_from_directory(DOWNLOAD_DIRECTORY, 'invoices.zip')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
