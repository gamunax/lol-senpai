from flask import Flask, render_template, request, g, redirect, url_for, abort
from flask.ext.babel import Babel
from general import log

app = Flask(__name__)
babel = Babel(app)


@app.before_request
def before_request():
    if request.view_args and 'lang' in request.view_args:
        g.lang = request.view_args['lang']
        if g.lang not in ('en', 'fr'):
            return abort(404, {'message': "Language not found."})
        request.view_args.pop('lang')
    if request.view_args and 'region' in request.view_args:
        region = request.view_args['region']
        from library.api.constants import REGIONAL_ENDPOINTS
        if region not in REGIONAL_ENDPOINTS:
            return abort(404, {'message': "Region not found."})


@babel.localeselector
def get_locale():
    log.info("Language: " + g.get('lang', 'en'))
    return g.get('lang', 'en')


@app.route('/')
def root():
    return redirect(url_for('main', lang='en'))


@app.route('/<lang>')
def main():
    title = "Home"
    return render_template('main.html', **locals())


@app.route('/<lang>/game/<region>/<username>')
def match(region, username):
    title = username + "'s match"
    return render_template('match.html', **locals())


@app.errorhandler(404)
def page_not_found(error):
    title = "Not found"
    message = error.description['message'] if 'message' in error.description else "Not found"
    return render_template('404.html', **locals()), 404


if __name__ == '__main__':
    app.run(debug=True)
