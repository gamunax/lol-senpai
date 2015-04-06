from flask import Flask, render_template, request, g, redirect, url_for, abort
from flask.ext.babel import Babel

app = Flask(__name__)
babel = Babel(app)


@app.before_request
def before_request():
    if request.view_args and 'lang' in request.view_args:
        g.lang = request.view_args['lang']
        if g.lang not in ('en', 'fr'):
            return abort(404, "Language not found.")
        request.view_args.pop('lang')


@babel.localeselector
def get_locale():
    print(g.get('lang', 'en'))
    return g.get('lang', 'en')


@app.route('/')
def root():
    return redirect(url_for('main', lang='en'))


@app.route('/<lang>')
def main():
    title = "Home"
    return render_template('main.html', **locals())


@app.route('/<lang>/match/<username>')
def match(username):
    title = username + "'s match"
    return render_template('match.html', **locals())


if __name__ == '__main__':
    app.run(debug=True)
