from flask import Flask,render_template,redirect, url_for,request,jsonify
import json,sys
sys.path.append("py")
import swe

app = Flask(__name__, template_folder="")
@app.route('/')
def home():
    return render_template('menu/home/base.html')
@app.route('/spam')
def spam():
    return render_template('menu/spam/index.html')
@app.route('/spam/send_otp', methods=['POST'])
def send_otp():
    nomor = request.form['phone_number']
    method = request.form['method']
    if method == 'SMS':
        result = swe.SMS(nomor)
    elif method == 'WA':
        result = swe.WA(nomor)
    else:
        result = 'Metode tidak Tersedia'
    return result
def xdoa():
    with open('json/doa.json', encoding='utf-8') as file:
        data = json.load(file)
    return data
@app.route('/doa')
def index():
    data = xdoa()
    return render_template('menu/doa/index.html', doas=data)
@app.route('/doa/search')
def search():
    query = request.args.get('query', '')
    data = xdoa()
    if query:
        data = [doa for doa in data if query.lower() in doa['judul'].lower() or query.lower() in doa['indo'].lower()]
    return render_template('menu/doa/index.html', doas=data, query=query)
@app.route('/doa/<int:doa_id>')
def detail(doa_id):
    data = xdoa()
    doa = data[doa_id - 1]
    return render_template('menu/doa/detail.html', doa=doa, doa_id=doa_id)
with open('json/dzikir.json') as f:
    dzikir_data = json.load(f)
@app.route('/dzikir')
def dzikir():
    return render_template('menu/dzikir/index.html', dzikir_data=dzikir_data)
@app.route('/dzikir/<kategori>')
def dzikir_kategori(kategori):
    data = [dzikir for dzikir in dzikir_data if dzikir['type'] == kategori]
    return render_template('menu/dzikir/index.html', dzikir_data=dzikir_data, selected_data=data, kategori=kategori)
    

if __name__ == '__main__':
    app.run(debug=True)
