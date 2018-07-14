from flask import Flask, render_template, request
from engine import search, filter_results

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        address = request.form['q']
        res = search(address)
        results = filter_results(res)
        return render_template("results.html", results=results)
    return render_template('index.html')

if __name__ == '__main__':
    import os
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), processes=2)
