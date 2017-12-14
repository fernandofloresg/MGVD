from flask import Flask, render_template, request
import os
import subprocess
import re

app = Flask('Sensacionalismo')

@app.route("/" )
def hello():
    return render_template('index.html', name='index_template')

@app.route('/', methods=['POST'])
def turn_on():
    url = request.form['url']
    ret = subprocess.check_output(['python', 'porcentaje.py', url])
    ret = re.findall(r'\d+', str(ret))
    return str(ret[0]) + '%' 

if __name__ == "__main__":
    app.run()