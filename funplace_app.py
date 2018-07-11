from flask import Flask, render_template
from .engine import search

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods = ['GET',])
def result():
   if request.method == 'GET':
      querry = request.form
      address = querry['search']
      result = search(address)
      return render_template("result.html",result = result)
	

if __name__=='__main__':
    app.run(dubug=True, host='0.0.0.0')
