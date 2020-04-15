from flask import Flask, render_template, request, jsonify
from data import get_data

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('icd_autocomplete.html')

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        data_to_send = get_data()
        return render_template('icd_search.html', posts=data_to_send)

    return render_template('icd_search.html')

@app.route('/icd', methods=['GET', 'POST'])
def icd():
    if request.method == 'POST':
        data_to_send = get_data()
        return jsonify(data_to_send)

    return render_template('icd.html')

@app.route('/api-doc')
def documentation():
    return render_template('api_doc.html')


if __name__ == "__main__":
    app.run(debug=True)
