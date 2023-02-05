import os
import zipfile
from flask import Flask, render_template, request, send_from_directory, jsonify
from pdfkit import from_string, configuration

from geberate_csv import generate_csv_file
from service import get_formatted_orders, get_data, read_file, upload_file, generate_result_trie_zip_file

PRODUCTION = True
Config = configuration(wkhtmltopdf=f'/usr/{"local/bin/" if PRODUCTION is True else "bin/"}wkhtmltopdf')
app = Flask(__name__)
DOWNLOAD_DIRECTORY = "files"
UPLOAD_FOLDER = 'files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/invoices', methods=['GET', 'POST'])
def invoices():
    """
    this api will generate the invoices based on the uploaded orders, after organizing the data into the appropriate format we parce each command into
    the invoice template then we convert the template into pdf file using the pdfkit package
    """
    if request.method == 'GET':
        return render_template('generate_invoices.html')
    else:
        uploaded_file, file_path = upload_file(request.files.get('file'))
        order_items = get_formatted_orders(get_data(read_file(file_path)))
        with zipfile.ZipFile('files/invoices.zip', 'w') as myzip:
            for i in order_items:
                print(order_items[i].command_lines[0].hs_code)
                html = render_template(
                    "invoice.html",
                    order=order_items[i])
                from_string(html, f'files/invoice{order_items[i].order_id}.pdf', configuration=Config)
                myzip.write(f'files/invoice{order_items[i].order_id}.pdf')
                os.remove(f'files/invoice{order_items[i].order_id}.pdf')
        return jsonify(success=True)


@app.route('/excel/generate_invoice_templates', methods=['GET', 'POST'])
def generate_excel_file():
    if request.method == 'GET':
        return render_template('generate_excels.html')
    else:
        uploaded_file, file_path = upload_file(request.files.get('file'))
        try:
            generate_csv_file(uploaded_file)
            return jsonify({'message': 'generated'}), 200
        except Exception as e:
            print(e)
            return jsonify({'message', str(e)}), 500


@app.route('/downloadZip/<name>')
def get_pdfs(name):
    return send_from_directory(DOWNLOAD_DIRECTORY, f'{name}.zip')


@app.route('/excel/generate_sorting_invoices_zip', methods=['GET', 'POST'])
def generate_sorted_products_zip():
    """
    
    """
    if request.method == 'GET':
        return render_template('generate_sorting_products.html')
    else:
        try:
            _, file_path = upload_file(request.files.get('file'))
            generate_result_trie_zip_file(products=read_file(file_path))
            return jsonify({'message': 'generated'}), 200
        except Exception as e:
            return jsonify({'message', str(e)}), 500


@app.route('/downloadExcel')
def get_excels():
    """ this function will make the csv file downloadable """
    return send_from_directory(DOWNLOAD_DIRECTORY, 'output.csv')


if __name__ == '__main__':
    app.run(debug=not PRODUCTION, host='0.0.0.0', port=5000)
