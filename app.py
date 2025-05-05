from flask import Flask, jsonify, render_template
from analysis.pda import (get_shape, get_info, get_describe)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pda')
def pda():
    shape_data = get_shape()
    describe_data = get_describe()
    return render_template('pda.html',
                           shape_data=shape_data,
                           describe_data=describe_data)

@app.route('/info')
def info():
    info_data = get_info()
    return render_template('info.html', info_data=info_data)


if __name__ == '__main__':
    app.run(debug=True)
