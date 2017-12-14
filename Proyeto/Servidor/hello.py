from flask import Flask, render_template, request
import os

app = Flask('Sensacionalismo')

@app.route("/" )
def hello():
    return render_template('index.html', name='index_template')

@app.route('/', methods=['POST'])
def turn_on():
    url = request.form['url']
    os.system('python consulta.py ' + url)
    return 'success'

if __name__ == "__main__":
    app.run()