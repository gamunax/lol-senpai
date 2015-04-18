__author__ = 'Dewep'

from flask import render_template, redirect, url_for, Flask

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html', **locals())


if __name__ == '__main__':
    app.run(debug=True)
